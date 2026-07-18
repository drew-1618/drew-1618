import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_image(input_path, output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: Cannot find input image at '{input_path}'")
        return

    print("Step 1: Removing background...")
    with open(input_path, 'rb') as f:
        input_data = f.read()
    
    # rembg isolates the subject and makes the background transparent
    no_bg_data = remove(input_data)
    
    # Convert bytes to a numpy array for OpenCV processing
    nparr = np.frombuffer(no_bg_data, np.uint8)
    img_rgba = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)

    print("Step 2: Boosting local contrast (CLAHE)...")
    # Split channels to isolate the Alpha (transparency) mask
    b, g, r, alpha = cv2.split(img_rgba)
    
    # Convert RGB to grayscale to evaluate brightness[cite: 1]
    gray = cv2.cvtColor(cv2.merge([b, g, r]), cv2.COLOR_BGR2GRAY)
    
    # Apply CLAHE (Contrast-Limited Adaptive Histogram Equalization)
    # This keeps features sharp and prevents flat lighting from turning into a blob[cite: 1]
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray_enhanced = clahe.apply(gray)
    
    # Rebuild the RGBA image with the enhanced grayscale and original alpha mask[cite: 1]
    img_enhanced_rgba = cv2.merge([gray_enhanced, gray_enhanced, gray_enhanced, alpha])

    print("Step 3: Compositing onto a pure white background...")
    # Convert to PIL to easily handle clean alpha compositing[cite: 1]
    pil_img = Image.fromarray(cv2.cvtColor(img_enhanced_rgba, cv2.COLOR_BGRA2RGBA))
    
    # Create a solid white background matching the image size[cite: 1]
    background = Image.new("RGBA", pil_img.size, (255, 255, 255, 255))
    
    # Paste the face over the white background (white maps to blank spaces in ASCII)[cite: 1]
    final_img = Image.alpha_composite(background, pil_img)
    
    # Save the final prepped image[cite: 1]
    final_img.convert("RGB").save(output_path)
    print(f"Success! Prepped image saved to: {output_path}[cite: 1]")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <path_to_source_photo>")
        sys.exit(1)
        
    input_photo = sys.argv[1]
    prep_image(input_photo)
