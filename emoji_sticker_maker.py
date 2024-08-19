from PIL import Image, ImageDraw, ImageFont


class EmojiStickerMaker:
    def __init__(self):
        return

    def make_emoji_sticker(self, label, font_path='NotoEmoji.ttf'):   
        image_size = 384
        emoji_size = 325
        emoji_images = []

        # Use the image size as the font size to make the emoji as large as possible
        font = ImageFont.truetype(font_path, emoji_size)

        for char in label:
            # Create a new image with a white background
            image = Image.new('1', (image_size, image_size), 'white')
            draw = ImageDraw.Draw(image)

            text_width, text_height = draw.textsize(char, font=font)

            while not (image_size <= text_width or image_size <= text_height):
                emoji_size += 1
                font = ImageFont.truetype(font_path, emoji_size)
                text_width, text_height = draw.textsize(char, font=font)

            print(f"printing emoji at font size {emoji_size}")

            # Draw the emoji centered in the image
            draw.text((0, 0), label[:1], fill='black', font=font)
            image = image.rotate(90, expand=True)

            emoji_images.append(image)

        return emoji_images