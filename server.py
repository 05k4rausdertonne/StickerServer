from flask import Flask, request, render_template
from PIL import Image
from print_image import Printer
from label_maker import LabelMaker
from emoji_sticker_maker import EmojiStickerMaker

# TODO: build frontend


printer = Printer(0x28e9, 0x0289)
label_maker = LabelMaker()
emoji_sticker_maker = EmojiStickerMaker()
app = Flask(__name__)

@app.route('/label', methods=['GET'])
def label():
    # Get the 'text' argument from the URL
    text = request.args.get('ltext')
    bold = request.args.get('lbold')
    italic = request.args.get('litalic')
    font_size = request.args.get('lfontsize')
    do_emoji = request.args.get('lemoji')

    if font_size:
        font_size = int(font_size)
    
    if text and text != "":
        # Print the text to the console
        print(f"Received text: {text}")
        
        if do_emoji:
            printer.print_image(emoji_sticker_maker.make_emoji_sticker(text))
        if bold and not italic:
            printer.print_image(label_maker.make_label(text, font_path='liberation-sans.bold.ttf', font_size=font_size))
        if not bold and italic:
            printer.print_image(label_maker.make_label(text, font_path='liberation-sans.italic.ttf', font_size=font_size))
        if bold and italic:
            printer.print_image(label_maker.make_label(text, font_path='liberation-sans.bold-italic.ttf', font_size=font_size))
        if not bold and not italic and not do_emoji:
            printer.print_image(label_maker.make_label(text, font_size=font_size))
            
    return render_template('index.html'), 200
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html'), 200
    
@app.route("/image",methods=["POST"])
def image():
    image=request.files['file']
    pil_image = Image.open(image)
    printer.print_image(pil_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)