from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import shutil
import os
import json
from typing import List

from . import database, auth, inference

# Initialize DB
database.init_db()

app = FastAPI(title="Dental Clinic AI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static Files (Frontend)
# Ensure directory exists
os.makedirs("interfaz/static", exist_ok=True)
os.makedirs("interfaz/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="interfaz/static"), name="static")

@app.on_event("startup")
async def startup_event():
    print("\n" + "="*50)
    print("🦷 DENTAL AI CLINIC IS RUNNING!")
    print("👉 Access here: http://127.0.0.1:8000/static/index.html")
    print("="*50 + "\n")

# --- Auth Routes ---

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)):
    user = db.query(database.User).filter(database.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/register")
def register_user(username: str = Form(...), password: str = Form(...), db: Session = Depends(auth.get_db)):
    db_user = db.query(database.User).filter(database.User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth.get_password_hash(password)
    new_user = database.User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username}

# --- Application Routes ---

@app.get("/users/me")
async def read_users_me(current_user: database.User = Depends(auth.get_current_user)):
    return {"username": current_user.username, "id": current_user.id}

@app.post("/predict")
async def predict(file: UploadFile = File(...), current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    # 1. Save file locally
    file_location = f"interfaz/uploads/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Run Inference
    with open(file_location, "rb") as f:
        image_bytes = f.read()
    result = inference.predict_image_bytes(image_bytes)
    
    # 3. Save to History
    detections_json = json.dumps(result["detections"])
    history_item = database.History(
        user_id=current_user.id,
        image_path=file_location,
        detections=detections_json
    )
    db.add(history_item)
    db.commit()
    
    return result

@app.get("/history")
def get_history(current_user: database.User = Depends(auth.get_current_user), db: Session = Depends(auth.get_db)):
    history = db.query(database.History).filter(database.History.user_id == current_user.id).all()
    # Parse JSON for frontend
    parsed_history = []
    for h in history:
        parsed_history.append({
            "id": h.id,
            "image_path": h.image_path,
            "detections": json.loads(h.detections),
            "timestamp": h.timestamp
        })
    return parsed_history
