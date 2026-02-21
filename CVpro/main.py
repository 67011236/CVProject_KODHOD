import cv2
import numpy as np
import os
from ui import ColorExtractionUI

def main():
    # Initialize the UI
    ui = ColorExtractionUI()
    
    # Check if images exist
    image_folder = os.path.join(os.path.dirname(__file__), "image")
    if not os.path.exists(image_folder):
        print("Image folder not found!")
        return
    
    # Get available images
    available_images = []
    for file in os.listdir(image_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            available_images.append(os.path.join(image_folder, file))
    
    if not available_images:
        print("No images found in the image folder!")
        return
    
    # Ensure we have images to work with
    if len(available_images) == 0:
        print("No images found in the image folder!")
        return
    
    print(f"Found {len(available_images)} images: {[os.path.basename(img) for img in available_images]}")
    
    # Run the application with all available images
    ui.run(available_images)

if __name__ == "__main__":
    main()
