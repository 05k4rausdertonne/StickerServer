from flask import Flask, request, render_template, jsonify
from PIL import Image
from emoji import EMOJI_DATA

from print_image import Printer
from label_maker import LabelMaker
from emoji_sticker_maker import EmojiStickerMaker
import subprocess



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

@app.route('/spice-jar', methods=['POST'])
def spice_jar():
    text = request.form.get('text', '')
    file = request.files.get('file')
    bold = request.form.get('bold') == 'true'
    italic = request.form.get('italic') == 'true'
    font_size = int(request.form.get('fontsize', 35))
    edge_enhance = request.form.get('edgeenhance') == 'true'

    pil_image = None
    if file:
        pil_image = Image.open(file)

    # Create the 979x384 image in label_maker
    spice_image = label_maker.make_spice_jar(
        text,         
        pil_image=pil_image, 
        font_path=bold_italic_font_path if bold and italic else (bold_font_path if bold else (italic_font_path if italic else default_font_path)),
        font_size=font_size
    )
    
    # Rotate to 384x979 for the printer (landscape orientation on paper)
    spice_image = spice_image.rotate(90, expand=True)

    success = printer.print_image(spice_image, auto_rotate=False, edge_enhance=edge_enhance)
    
    if success:
        return jsonify({"message": "Spice jar printed successfully"}), 200
    else:
        return jsonify({"message": "Error: Printer failed"}), 503


@app.route('/shutdown', methods=['POST'])
def shutdown():
    try:
        # Using sudo to ensure it has permission on Linux/Raspbian
        subprocess.run(['sudo', 'shutdown', 'now'], check=True)
        return jsonify({"message": "Shutdown signal sent"}), 200
    except Exception as e:
        print(f"Error during shutdown attempt: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)