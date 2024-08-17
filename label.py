from escpos.printer import Usb
import argparse
from PIL import Image, ImageDraw, ImageFont

vendor_id = 0x28e9
product_id = 0x0289

def create_text_image(text, font_path, font_size, max_width):
    # Load the font
    font = ImageFont.truetype(font_path, font_size)
    
    # Create a new image with white background
    image = Image.new('RGB', (max_width, 1000), 'white')
    draw = ImageDraw.Draw(image)
    
    # Function to split text into lines
    def split_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            width = draw.textlength(test_line, font=font)
            if width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
    
    # Split the text into lines that fit within max_width
    lines = split_text(text, font, max_width)
    
    # Calculate the height needed for the image
    line_height = draw.textbbox((0, 0), "gyh\ngyh", font=font)[3] - draw.textbbox((0, 0), "gyh", font=font)[3]
    image_height = int(line_height * len(lines) * 1.2)
    
    # Create a new image with the correct height
    image = Image.new('RGB', (max_width, image_height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw each line of text
    y = 0
    for line in lines:
        width = draw.textlength(line, font=font)
        draw.text(((max_width - width) // 2, y), line, fill='black', font=font)
        y += line_height
    
    # Convert the image to monochrome (1-bit) for bitImageColumn
    image = image.convert('1')  # '1' for monochrome
    return image

def main():
    printer = Usb(vendor_id, product_id, 0, timeout=5000)

    parser = argparse.ArgumentParser(description="Parse command line parameters for styling.")
    parser.add_argument('-m', '--margin', type=int, default=0, help='Margin value (default: 5)')
    parser.add_argument('-p', '--padding', type=int, default=5, help='Padding value (default: 5)')
    parser.add_argument('-b', '--borderwidth', type=int, default=5, help='Border width value (default: 5)')
    parser.add_argument('-f', '--font-size', type=int, default=20, help='Font size value (default: 12)')
    parser.add_argument('-l', '--label', type=str, default="My Label for my Box", help='Label text (default: "default label")')
    parser.add_argument('-fp', '--font-path', type=str, default="Arial.ttf", help='Path to ttf font family')

    args = parser.parse_args()
    image_width = 384

    # Create the text image
    text_image = create_text_image(args.label, args.font_path, args.font_size, image_width - (args.margin + args.padding + args.borderwidth) * 2)
    margin = (args.margin + args.padding + args.borderwidth)
    image_height = text_image.size[1] + 2 * margin
    image = Image.new('1', (image_width, image_height), 1)  # Create final image in monochrome
    image.paste(text_image, (margin, margin))

    draw = ImageDraw.Draw(image)
    draw.rectangle([(args.margin, args.margin), (image_width-args.margin, image_height-args.margin)], outline='black', width=args.borderwidth)

    # Print the image
    printer.ln(1)
    printer.image(image, impl="bitImageColumn")
    printer.ln(4)

if __name__ == "__main__":
    main()
