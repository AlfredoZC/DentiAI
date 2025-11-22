const API_URL = "http://127.0.0.1:8000";

// --- Login / Register ---
async function login(username, password) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/token`, {
            method: "POST",
            body: formData,
        });
        if (!response.ok) throw new Error("Login failed");
        const data = await response.json();
        localStorage.setItem("token", data.access_token);
        window.location.href = "/static/dashboard.html";
    } catch (error) {
        alert(error.message);
    }
}

async function register(username, password) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/register`, {
            method: "POST",
            body: formData,
        });
        if (!response.ok) throw new Error("Registration failed");
        alert("Registered successfully! Please login.");
    } catch (error) {
        alert(error.message);
    }
}

// --- Dashboard Logic ---
async function loadHistory() {
    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/static/index.html";
        return;
    }

    try {
        const response = await fetch(`${API_URL}/history`, {
            headers: { "Authorization": `Bearer ${token}` }
        });

        if (response.status === 401) {
            localStorage.removeItem("token");
            window.location.href = "/static/index.html";
            return;
        }

        if (!response.ok) throw new Error("Failed to load history");

        const history = await response.json();
        const historyList = document.getElementById("history-list");

        if (history.length === 0) {
            historyList.innerHTML = "<p>No history yet.</p>";
            return;
        }

        historyList.innerHTML = "";
        history.forEach(item => {
            const div = document.createElement("div");
            div.className = "history-item";
            div.innerHTML = `
                <span>${new Date(item.timestamp).toLocaleDateString()}</span>
                <span>${item.detections.length} Detections</span>
            `;
            historyList.appendChild(div);
        });
    } catch (error) {
        console.error("History error:", error);
        const historyList = document.getElementById("history-list");
        if (historyList) {
            historyList.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    }
}

async function predictImage(file) {
    const token = localStorage.getItem("token");
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData
    });
    const result = await response.json();
    displayResult(result);
    loadHistory(); // Refresh history
}

function displayResult(result) {
    const resultDiv = document.getElementById("result");
    resultDiv.innerHTML = "<h3>Analysis Result:</h3>";

    // Create container for side-by-side view
    const container = document.createElement("div");
    container.style.display = "flex";
    container.style.gap = "1rem";
    container.style.justifyContent = "center";
    container.style.flexWrap = "wrap";
    container.style.alignItems = "flex-start";

    // 1. Raw Image (Clone from preview if exists, or create new if from camera)
    const rawPreview = document.getElementById("raw-preview");
    if (rawPreview && rawPreview.src && !document.getElementById("raw-preview-container").classList.contains("hidden")) {
        const rawImgClone = rawPreview.cloneNode();
        rawImgClone.style.maxHeight = "400px";
        rawImgClone.style.border = "2px solid #ccc";

        const rawWrapper = document.createElement("div");
        rawWrapper.innerHTML = "<h4>Original</h4>";
        rawWrapper.appendChild(rawImgClone);
        container.appendChild(rawWrapper);

        // Hide the standalone preview to avoid duplication
        document.getElementById("raw-preview-container").classList.add("hidden");
    }

    // 2. Annotated Image
    if (result.image_base64) {
        const img = document.createElement("img");
        img.src = `data:image/jpeg;base64,${result.image_base64}`;
        img.style.maxWidth = "100%";
        img.style.maxHeight = "400px";
        img.style.border = "2px solid var(--primary-color)";
        img.style.borderRadius = "8px";

        const annWrapper = document.createElement("div");
        annWrapper.innerHTML = "<h4>AI Analysis</h4>";
        annWrapper.appendChild(img);
        container.appendChild(annWrapper);
    }

    resultDiv.appendChild(container);

    // Detections List
    const listContainer = document.createElement("div");
    listContainer.style.marginTop = "1rem";

    if (result.detections.length === 0) {
        listContainer.innerHTML += "<p><strong>No affections detected.</strong></p>";
    } else {
        listContainer.innerHTML += "<h4>Detected Affections:</h4>";
        const ul = document.createElement("ul");
        result.detections.forEach(d => {
            const li = document.createElement("li");
            li.textContent = `${d.class} (${(d.confidence * 100).toFixed(0)}%)`;
            li.style.color = "var(--text-color)";
            li.style.fontWeight = "bold";
            ul.appendChild(li);
        });
        listContainer.appendChild(ul);
    }
    resultDiv.appendChild(listContainer);

    resultDiv.classList.remove("hidden");
}

// --- Camera Logic ---
let stream;
async function startCamera() {
    const video = document.getElementById("camera-feed");
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.classList.remove("hidden");
        document.getElementById("capture-btn").classList.remove("hidden");
        document.getElementById("stop-btn").classList.remove("hidden");

        // Hide other elements
        document.getElementById("raw-preview-container").classList.add("hidden");
        document.getElementById("result").classList.add("hidden");
    } catch (err) {
        alert("Error accessing camera: " + err.message);
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    document.getElementById("camera-feed").classList.add("hidden");
    document.getElementById("capture-btn").classList.add("hidden");
    document.getElementById("stop-btn").classList.add("hidden");
}

function captureImage() {
    const video = document.getElementById("camera-feed");
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    // Show captured image as raw preview
    const rawPreview = document.getElementById("raw-preview");
    rawPreview.src = canvas.toDataURL("image/jpeg");
    document.getElementById("raw-preview-container").classList.remove("hidden");

    // Stop camera after capture
    stopCamera();

    canvas.toBlob(blob => {
        predictImage(new File([blob], "capture.jpg", { type: "image/jpeg" }));
    }, "image/jpeg");
}

// --- Upload Logic ---
window.handleFileUpload = function (input) {
    if (input.files && input.files[0]) {
        processFile(input.files[0]);
    }
}

function processFile(file) {
    // Show raw preview
    const reader = new FileReader();
    reader.onload = function (e) {
        const rawPreview = document.getElementById("raw-preview");
        rawPreview.src = e.target.result;
        document.getElementById("raw-preview-container").classList.remove("hidden");
        document.getElementById("result").classList.add("hidden"); // Hide previous results

        // Stop camera if running
        stopCamera();
    }
    reader.readAsDataURL(file);

    // Send for prediction
    predictImage(file);
}

// --- Drag & Drop Logic ---
document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-upload");

    if (dropZone) {
        dropZone.addEventListener("click", () => {
            fileInput.click();
        });

        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.classList.add("drop-zone--over");
        });

        ["dragleave", "dragend"].forEach(type => {
            dropZone.addEventListener(type, () => {
                dropZone.classList.remove("drop-zone--over");
            });
        });

        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.classList.remove("drop-zone--over");

            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFileUpload(fileInput);
            }
        });
    }
});
