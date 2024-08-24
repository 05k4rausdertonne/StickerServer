from flask import Flask, request, render_template, jsonify

from PIL import Image
from emoji import EMOJI_DATA

from print_image import Printer
from label_maker import LabelMaker
from emoji_sticker_maker import EmojiStickerMaker


# Adjust this values to compensate for your printer
spacer_size = 60

fonts_path = '/home/pi/StickerServer/static/fonts/'
default_font_path = f'{fonts_path}NotoSans-Regular.ttf'
bold_font_path = f'{fonts_path}NotoSans-Bold.ttf'
italic_font_path = f'{fonts_path}NotoSans-Italic.ttf'
bold_italic_font_path = f'{fonts_path}NotoSans-BoldItalic.ttf'
emoji_font_path = f'{fonts_path}NotoEmoji.ttf'

def contains_emoji(s):
    return any(char in EMOJI_DATA for char in s)

printer = Printer(0x28e9, 0x0289)
label_maker = LabelMaker()
emoji_sticker_maker = EmojiStickerMaker()
app = Flask(__name__)

@app.route('/label', methods=['GET'])
def label():
    # Get the 'text' argument from the URL
    text = request.args.get('text')
    bold = request.args.get('bold') == 'true'
    italic = request.args.get('italic') == 'true'
    font_size = request.args.get('fontsize')
    do_emoji = request.args.get('emoji') == 'true'

    if font_size:
        font_size = int(font_size)
    
    
    if text and text != "":
        # Print the text to the console
        print(f"Received text: {text}")

        if do_emoji:
            if len(text) > 1:
                rotate = True
            else:
                rotate = False
            for char in text:
                if contains_emoji(char):
                    printer.print_image(emoji_sticker_maker.make_emoji_sticker(char, emoji_font_path, rotate))
                else:
                    printer.print_image(emoji_sticker_maker.make_emoji_sticker(char, default_font_path, rotate))
            success = printer.print_spacer(px=spacer_size)
        elif contains_emoji(text):
            printer.print_image(
                label_maker.make_label(
                    text, 
                    font_path=emoji_font_path, 
                    font_size=font_size))
            success = printer.print_spacer(px=spacer_size)
        elif bold and not italic:
            printer.print_image(
                label_maker.make_label(
                    text, 
                    font_path=bold_font_path, 
                    font_size=font_size))
            success = printer.print_spacer(px=spacer_size)
        elif not bold and italic:
            printer.print_image(
                label_maker.make_label(
                    text, 
                    font_path=italic_font_path, 
                    font_size=font_size))
            success = printer.print_spacer(px=spacer_size)
        elif bold and italic:
            printer.print_image(
                label_maker.make_label(
                    text, 
                    font_path=bold_italic_font_path, 
                    font_size=font_size))
            success = printer.print_spacer(px=spacer_size)
        else:
            printer.print_image(
                label_maker.make_label(
                    text, 
                    font_path=default_font_path,
                    font_size=font_size))
            success = printer.print_spacer(px=spacer_size)
    if success:
        return render_template('index.html'), 200
    else:
        return 'Error: Printer not working, maybe its not initialized?', 503
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html'), 200
    
@app.route("/image",methods=["POST"])
def image():

    image=request.files['file']
    auto_rotate = request.args.get('autorotate') == 'true'
    edge_enhance = request.args.get('edgeenhance') == 'true'

    pil_image = Image.open(image)

    printer.print_image(pil_image, auto_rotate=auto_rotate, edge_enhance=edge_enhance)
    success = printer.print_spacer(px=spacer_size)

    if success:
        return jsonify({"message": "Image processed successfully"}), 200
    else:
        return jsonify({"message": "Error: Printer not working, maybe its not initialized?"}), 503

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)