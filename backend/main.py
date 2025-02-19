import os
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import torch
import torchvision.transforms as transforms
from PIL import Image

from model import MyResNet18

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Determine environment (Local vs. Production on Render)
IS_PRODUCTION = os.getenv("RENDER", "False") == "True"
FRONTEND_URL = "https://mlops-pipeline.vercel.app" if IS_PRODUCTION else "*"

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://mlops-pipeline.vercel.app",  # Production frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
,   # Only allow Vercel in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Dummy Text-Based Prediction ----------
def dummy_ml_logic(input_data: str) -> str:
    return f"Predicted label for '{input_data}'"

@app.post("/predict")
def predict(input_data: dict):
    user_input = input_data.get("input_data", "")
    prediction = dummy_ml_logic(user_input)
    return {"prediction": prediction}

# ---------- Image-Based Inference ----------
class_labels = {0: "Nasi Lemak", 1: "Roti Canai"}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model only if available
model_path = os.path.join(os.path.dirname(__file__), "resnet18.pth")
if os.path.exists(model_path):
    logger.info("Loading model...")
    model = MyResNet18(num_classes=2).to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()  # Set model to inference mode
    logger.info("Model loaded successfully.")
else:
    logger.warning(f"Model file {model_path} not found! Inference won't work.")
    model = None

# Define transforms used during training
inference_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

@app.post("/predict_image")
async def predict_image(file: UploadFile = File(...)):
    """
    Accepts an image file upload and returns a predicted class label.
    """
    if model is None:
        return {"error": "Model not loaded. Ensure 'resnet18.pth' exists."}

    image = Image.open(file.file).convert("RGB")
    input_tensor = inference_transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        output = model(input_tensor)
        _, predicted_class = torch.max(output, 1)

    predicted_label = class_labels.get(int(predicted_class.item()), "Unknown")

    return {"prediction": predicted_label}

# ---------- Root Endpoint ----------
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head><title>FastAPI MLOps App</title></head>
        <body>
            <h1>Hello from FastAPI!</h1>
            <p>Available endpoints:</p>
            <ul>
                <li>/predict - for text input inference</li>
                <li>/predict_image - for image upload inference</li>
            </ul>
            <p>Go to <a href='/docs'>/docs</a> for interactive API documentation.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    # Set different host for local and Render deployment
    HOST = "0.0.0.0" if IS_PRODUCTION else "127.0.0.1"
    PORT = int(os.getenv("PORT", 8000))

    uvicorn.run("main:app", host=HOST, port=PORT, reload=not IS_PRODUCTION)
