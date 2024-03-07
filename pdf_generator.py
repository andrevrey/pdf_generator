from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw
import os

def modify_image(image_path, iteration):
    """
    Slightly modifies the image to make each insertion unique.
    """
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)
    # Add a tiny dot to the image; change its position slightly each time.
    draw.point((iteration % im.width, iteration % im.height), fill='white')
    modified_path = f"temp_{iteration}.jpg"
    im.save(modified_path)
    return modified_path

def insert_image_repeatedly(pdf_path, image_path, target_size_mb):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    page_width, page_height = letter

    image_size_bytes = os.path.getsize(image_path)
    image_size_mb = image_size_bytes / (1024 * 1024)
    images_needed = int(target_size_mb // image_size_mb)

    for i in range(images_needed):
        modified_image_path = modify_image(image_path, i)
        c.drawImage(modified_image_path, 0, 0, width=page_width, height=page_height, preserveAspectRatio=True)
        c.showPage()
        # Remove the temporarily modified image file to keep the environment clean.
        os.remove(modified_image_path)

    c.save()

def main():
    pdf_path = "sample_pdf.pdf"
    image_path = "sample_image.jpg"  # Ensure this is the correct path to your image file
    
    # Prompt for the target size
    target_size_mb = float(input("Enter the approx. target PDF size in MB (may require adjusting to land on the exact size): "))
    
    insert_image_repeatedly(pdf_path, image_path, target_size_mb-2)

if __name__ == "__main__":
    main()
