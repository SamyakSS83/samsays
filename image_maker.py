import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

def get_char(pixel_value):
    # More detailed ASCII chars from darkest to lightest
    chars = np.array(list(' .,:;irsXA253hMHGS#9B&@'))
    return chars[int(pixel_value * (len(chars) - 1) / 255)]

def image_to_ascii(image_path, width=100):
    # Read image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Calculate aspect ratio and new height
    aspect_ratio = image.shape[1] / image.shape[0]
    height = int(width / (2.5 * aspect_ratio))  # Multiply by 2.5 to account for terminal font spacing
    
    # Resize image
    image = cv2.resize(image, (width, height))
    
    # Apply adaptive histogram equalization to enhance contrast
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    image = clahe.apply(image)
    
    # Apply slight Gaussian blur to reduce noise
    image = cv2.GaussianBlur(image, (3,3), 0)
    
    # Convert to ASCII
    ascii_image = ""
    for row in image:
        for pixel in row:
            ascii_image += get_char(pixel)
        ascii_image += "\n"
    
    return ascii_image

def save_ascii_art(ascii_str, output_path, font_size=10):
    # Calculate image size based on character count
    lines = ascii_str.split('\n')
    char_width = font_size * 0.6  # Approximate width of a monospace character
    char_height = font_size
    
    img_width = int(max(len(line) for line in lines) * char_width)
    img_height = int(len(lines) * char_height)
    
    # Create image with white background
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("Courier", font_size)
    except:
        font = ImageFont.load_default()
    
    # Draw text
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill='black')
        y += char_height
    
    # Save image
    image.save(output_path)

def main(input_image_path, width=150):
    # Generate ASCII art
    ascii_art = image_to_ascii(input_image_path, width)
    
    # Print to console
    print(ascii_art)
    
    # Save as text file
    with open('ascii_output.txt', 'w') as f:
        f.write(ascii_art)
    
    # Save as image
    save_ascii_art(ascii_art, 'ascii_output.png', font_size=8)
    
    # Display original vs ASCII
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Original image
    original = cv2.imread(input_image_path)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    ax1.imshow(original)
    ax1.set_title('Original Image')
    ax1.axis('off')
    
    # ASCII art image
    ascii_img = plt.imread('ascii_output.png')
    ax2.imshow(ascii_img)
    ax2.set_title('ASCII Art')
    ax2.axis('off')
    
    # plt.show()

# Run the program
if __name__ == "__main__":
    main("a.jpeg", width=75)