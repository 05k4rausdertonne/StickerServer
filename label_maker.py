from PIL import Image, ImageDraw, ImageFont

class LabelMaker:
    def __init__(self):
        return
    
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
    

    def make_label(label, font_path='liberation-sans.regular.ttf', font_size=20, margin=0, padding=5, borderwidth=5):   
        image_width = 384

        # Create the text image
        text_image = create_text_image(label, font_path, font_size, image_width - (margin + padding + borderwidth) * 2)
        scaled_margin = (margin + padding + borderwidth)
        image_height = text_image.size[1] + 2 * scaled_margin
        image = Image.new('1', (image_width, image_height), 1)  # Create final image in monochrome
        image.paste(text_image, (scaled_margin, scaled_margin))

        draw = ImageDraw.Draw(image)
        draw.rectangle([(margin, margin), (image_width-margin, image_height-margin)], outline='black', width=borderwidth)
        return image