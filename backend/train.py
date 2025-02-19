import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader

from model import MyResNet18

def train_model(
    data_dir=r"C:\Users\User\OneDrive\Desktop\DATASETS\malaysian_food\processed",
    num_classes=2,
    epochs=6,
    batch_size=32,
    lr=1e-4,
    model_path="resnet18.pth"
):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Define transforms: resize images to 224x224 and convert them to tensor
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    # Load the dataset from the processed folder (which should contain only nasi_lemak and roti_canai folders)
    train_dataset = datasets.ImageFolder(root=data_dir, transform=transform)

    # DEBUG: Print class names and their assigned label indices
    print("Classes in dataset:", train_dataset.classes)  # Expecting ['nasi_lemak', 'roti_canai']
    print("Class indices:", train_dataset.class_to_idx)  # Should print {'nasi_lemak': 0, 'roti_canai': 1}
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

    # Initialize the model with 2 output classes
    model = MyResNet18(num_classes=num_classes).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training loop
    model.train()
    for epoch in range(epochs):
        epoch_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()

            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()

        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}] - Loss: {avg_loss:.4f}")

    # Save the trained model weights
    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model(epochs=6, batch_size=32, model_path="resnet18.pth")
