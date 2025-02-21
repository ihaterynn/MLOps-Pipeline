import os
import logging
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
import torch
import torchvision.transforms as transforms
from PIL import Image

from apscheduler.schedulers.background import BackgroundScheduler  # NEW: APScheduler
from model import MyResNet18
from message_provider import get_random_message  # NEW: Import message provider

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Determine environment (Local vs. Production on Render)
IS_PRODUCTION = os.getenv("RENDER", "False") == "True"

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local frontend
        "https://mlops-pipeline.vercel.app"  # Production frontend
    ] if IS_PRODUCTION else ["*"],  # Allow all in development
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
    logger.info(f"Received text for prediction: {user_input}")
    prediction = dummy_ml_logic(user_input)
    logger.info(f"Returning text-based prediction: {prediction}")
    return {"prediction": prediction}

# ---------- Image-Based Inference ----------
class_labels = {0: "Nasi Lemak", 1: "Roti Canai"}

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Load the model only if available
model_path = os.path.join(os.path.dirname(__file__), "resnet18.pth")
if os.path.exists(model_path):
    logger.info(f"Found model file at: {model_path}")
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
    logger.info("📥 Received image upload request.")
    if model is None:
        logger.warning("⚠️ No model loaded; cannot perform inference.")
        return JSONResponse(content={"error": "Model not loaded. Ensure 'resnet18.pth' exists."}, status_code=500)

    try:
        logger.info(f"📁 Uploaded file name: {file.filename}")

        # Convert and transform the image
        image = Image.open(file.file).convert("RGB")
        logger.info("🎨 Image converted to RGB.")
        input_tensor = inference_transform(image).unsqueeze(0).to(device)
        logger.info(f"🧩 Input tensor shape: {input_tensor.shape}")

        with torch.no_grad():
            output = model(input_tensor)
            logger.info(f"📊 Model output: {output}")
            _, predicted_class = torch.max(output, 1)

        predicted_label = class_labels.get(int(predicted_class.item()), "Unknown")
        logger.info(f"🎯 Predicted class index: {predicted_class.item()}")
        logger.info(f"🏷️ Predicted label: {predicted_label}")

        return JSONResponse(content={"prediction": predicted_label}, status_code=200)

    except Exception as e:
        logger.error(f"❌ Error processing image: {str(e)}")
        return JSONResponse(content={"error": f"Failed to process image: {str(e)}"}, status_code=500)

# ---------- Random Message with APScheduler ----------
current_message = get_random_message()  # Fetch initial message from message_provider

def update_random_message():
    """Update the global random message every 24 hours."""
    global current_message
    current_message = get_random_message()
    logger.info(f"Updated random message: {current_message}")

# Start APScheduler
scheduler = BackgroundScheduler()
scheduler.add_job(update_random_message, 'interval', hours=24)
scheduler.start()
logger.info("✅ APScheduler started: Updating random message every 24 hours.")

@app.post("/random_message")
async def random_message():
    logger.info(f"Returning random message: {current_message}")
    return JSONResponse(content={"message": current_message}, status_code=200)

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
                <li>/random_message - for random meme messages</li>
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
