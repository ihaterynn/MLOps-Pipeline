import os
import logging
import random  # NEW: For random messages
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # ocal frontend
        "https://mlops-pipeline.vercel.app"  # production frontend
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

# ---------- Random Message Endpoint ----------
random_messages = [
    "Why did the durian refuse to share? Because it was too shellfish!",
    "Boss, got discount ah? – Every Malaysian ever.",
    "Malaysians don’t run from problems, they ‘belanja makan’ first and figure it out later.",
    "Our national sport isn’t badminton, it’s finding parking in Mid Valley on a weekend.",
    "Got Milo at home, but somehow the mamak one still tastes better.",
    "‘On the way’ – A classic Malaysian phrase meaning ‘I haven’t left the house yet.’",
    "If a Malaysian tells you ‘see first’, just assume it's a polite way of saying no.",
    "‘Eh, where you from?’ ‘KL.’ ‘Which part?’ ‘Actually, PJ.’",
    "Some say Malaysia has only two seasons: Hot and Extra Hot.",
    "‘Boss, teh o ais kurang manis’ – Still ends up 80% sugar, 20% regret.",
    "If you think waiting 10 minutes for food is long, you’ve never queued at Jalan Alor.",
    "‘Lepak where?’ ‘Anywhere also can’ *proceeds to take 2 hours to decide*.",
    "Never trust a Malaysian when they say ‘not spicy one’.",
    "That moment when Waze tells you ‘15 minutes to your destination’, but you’re in KL traffic.",
    "If a Malaysian asks ‘Ate already?’, they don’t care about your stomach, they just wanna makan together.",
    "When the mamak waiter remembers your order better than your best friend does.",
    "Public holiday announced? Malaysians already planning their long weekend getaway!",
    "Gong Xi Fa Cai! – The one time of year where even your distant relatives remember you exist.",
    "‘5G coming soon’ – but your area still struggling with 3G.",
    "Malaysian WiFi speed: Fast enough for TikTok, but buffering when paying bills.",
    "Trying to cross the road in KL is an extreme sport.",
    "KL Tower vs Petronas Towers? Both nice, but can they give me free parking?",
    "A Malaysian’s weakness: ‘Buy 1 Free 1’ and ‘Last Day Promotion’.",
    "Mamak food at 3am? The true Malaysian supper time."
]


@app.post("/random_message")
async def random_message():
    message = random.choice(random_messages)
    logger.info(f"Returning random message: {message}")
    return JSONResponse(content={"message": message}, status_code=200)

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
