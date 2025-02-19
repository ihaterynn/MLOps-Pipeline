import os
import random
from PIL import Image

# Set paths
DATA_DIR = r"C:\Users\User\OneDrive\Desktop\DATASETS\malaysian_food"
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
CLASSES_TO_USE = ["nasi_lemak", "roti_canai"]
SAMPLE_SIZE = 300  # Number of images per class folder

IMG_SIZE = (224, 224)  # Resize to 224x224

def preprocess_data():
    """
    Create a 'processed' folder in DATA_DIR and place resized images for
    the selected classes (nasi_lemak, roti_canai). Randomly pick 300 images from each class.
    """

    # Create the processed folder if it doesn't exist
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)

    # For each target class: e.g., nasi_lemak or roti_canai
    for class_name in CLASSES_TO_USE:
        class_folder = os.path.join(DATA_DIR, class_name)
        if not os.path.isdir(class_folder):
            print(f"Warning: {class_folder} does not exist. Skipping.")
            continue

        # Create the subfolder under 'processed' for the current class
        processed_class_dir = os.path.join(PROCESSED_DIR, class_name)
        os.makedirs(processed_class_dir, exist_ok=True)

        # Collect all image file paths in that folder
        all_images = [
            os.path.join(class_folder, f)
            for f in os.listdir(class_folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif"))
        ]

        # Shuffle and pick a subset of images (300 or fewer if not enough)
        random.shuffle(all_images)
        subset = all_images[:SAMPLE_SIZE]

        print(f"Processing {len(subset)} images from '{class_name}'...")

        # Process each image (open, resize, save to processed folder)
        for idx, img_path in enumerate(subset):
            try:
                with Image.open(img_path) as img:
                    img = img.convert("RGB")   # Ensure 3 channels
                    img = img.resize(IMG_SIZE, Image.ANTIALIAS)

                    # Save the image in the processed subfolder
                    filename = f"{class_name}_{idx}.jpg"
                    save_path = os.path.join(processed_class_dir, filename)
                    img.save(save_path)
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

    print("Preprocessing complete!")

if __name__ == "__main__":
    preprocess_data()
