from ultralytics import YOLO
import numpy as np
from PIL import Image
import io

# Load model
import os
MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
try:
    model = YOLO(MODEL_PATH)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def predict_image_bytes(image_bytes):
    if model is None:
        return {"error": "Model not loaded"}

    # Load image from bytes
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_np = np.array(image)

    # CRITICAL: Convert RGB to BGR for YOLO
    image_bgr = image_np[..., ::-1]

    import base64

    # Inference
    results = model.predict(image_bgr, conf=0.25)
    
    # Process results
    detections = []
    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        conf = float(box.conf[0])
        detections.append({"class": cls_name, "confidence": round(conf, 2)})

    # Generate annotated image
    result_img_bgr = results[0].plot()
    result_img_rgb = result_img_bgr[..., ::-1] # Convert back to RGB
    result_pil = Image.fromarray(result_img_rgb)
    
    # Convert to base64
    buffered = io.BytesIO()
    result_pil.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return {"detections": detections, "image_base64": img_str}
