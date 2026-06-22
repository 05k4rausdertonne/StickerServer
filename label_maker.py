from PIL import Image, ImageDraw, ImageFont

# Attribution to Phlip Müller (github: muelphil) for this code

class LabelMaker:
    def __init__(self):
        return
    
    def create_text_image(self, text, font_path, font_size, max_width):
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
    

    def make_label(self, label, font_path='liberation-sans.regular.ttf', font_size=35, margin=0, padding=5, borderwidth=5):   
        image_width = 384

        # Create the text image
        text_image = self.create_text_image(label, font_path, font_size, image_width - (margin + padding + borderwidth) * 2)
        scaled_margin = (margin + padding + borderwidth)
        image_height = text_image.size[1] + 2 * scaled_margin
        image = Image.new('1', (image_width, image_height), 1)  # Create final image in monochrome
        image.paste(text_image, (scaled_margin, scaled_margin))

        draw = ImageDraw.Draw(image)
        draw.rectangle([(margin, margin), (image_width-margin, image_height-margin)], outline='black', width=borderwidth)
        return image

    # make image that is 384*979 pixels for the spice labels

    def make_spice_jar(self, text, pil_image=None, font_path='NotoSans-Regular.ttf', font_size=35, bold=False, italic=False):
        # Dimensions for 979x384 landscape label
        label_width = 985
        label_height = 384
        half_height = label_height // 2

        # Create the main canvas (RGB first for easier processing, then convert to 1-bit)
        canvas = Image.new('RGB', (label_width, label_height), 'white')
        draw = ImageDraw.Draw(canvas)

        # --- UPPER HALF: IMAGE ---
        if pil_image:
            img_w, img_h = pil_image.size
            max_w = label_width
            max_h = half_height
            
            ratio = min(max_w / img_w, max_h / img_h)
            new_w = int(img_w * ratio)
            new_h = int(img_h * ratio)
            
            resized_img = pil_image.resize((new_w, new_h), Image.LANCZOS)
            x_offset = (label_width - new_w) // 2
            y_offset = (half_height - new_h) // 2
            canvas.paste(resized_img, (x_offset, y_offset))

        # --- LOWER HALF: TEXT ---
        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # Simple text wrapping
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            left, top, right, bottom = draw.textbbox((0, 0), test_line, font=font)
            if (right - left) <= label_width * 0.8:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)

        # Vertical centering calculation for the text block
        # Estimate total height of text block
        total_text_height = 0
        line_spacing = 5
        for line in lines:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
            total_text_height += (bottom - top) + line_spacing
        
        # Start drawing from the middle of the lower half minus half the text height
        y_cursor = half_height + (half_height - total_text_height) // 2
        
        for line in lines:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
            line_w = right - left
            line_h = bottom - top
            x_pos = (label_width - line_w) // 2
            draw.text((x_pos, y_cursor), line, fill='black', font=font)
            y_cursor += line_h + line_spacing

        canvas = canvas.convert('1')
        return canvas
