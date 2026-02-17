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
    
    # Ensure we have at least 2 images, duplicate if needed
    if len(available_images) == 1:
        available_images.append(available_images[0])  # Use same image twice if only one exists
    
    print(f"Available images: {[os.path.basename(img) for img in available_images[:2]]}")
    
    # Run the application with multiple images
    ui.run(available_images[:2])  # Pass first 2 images

if __name__ == "__main__":
    main()
