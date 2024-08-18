from flask import Flask, request, render_template
from PIL import Image
from print_image import Printer
from label_maker import LabelMaker

# TODO: build frontend

printer = Printer(0x28e9, 0x0289)
label_maker = LabelMaker()
app = Flask(__name__)

@app.route('/label', methods=['GET'])
def label():
    # Get the 'text' argument from the URL
    text = request.args.get('text')
    
    if text:
        # Print the text to the console
        print(f"Received text: {text}")
        # TODO: pass different args on
        printer.print_image(label_maker.make_label(text))
        
        return render_template('index.html'), 200
    else:
        return "No text provided", 400
    
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