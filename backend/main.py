from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
import torch
import torchvision.transforms as transforms
from PIL import Image

from model import MyResNet18

app = FastAPI()

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For production, restrict to your frontend URL
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

# Class label mapping
class_labels = {0: "Nasi Lemak", 1: "Roti Canai"}

# Set up device and load the trained model (ensure num_classes matches training)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MyResNet18(num_classes=2).to(device)
model.load_state_dict(torch.load("resnet18.pth", map_location=device))
model.eval()  # Set model to inference mode

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
            <p>Go to /docs for interactive API documentation.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
