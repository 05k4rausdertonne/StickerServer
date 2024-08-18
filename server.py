from flask import Flask, request
from PIL import Image
from print_image import Printer
from label_maker import LabelMaker

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
        printer.print_image(label_maker.make_label(text))
        
        return f"Text received and printed: {text}", 200
    else:
        return "No text provided", 400
    
@app.route("/image",methods=["POST"])
def image():
    image=request.files['file']
    pil_image = Image.open(image)
    printer.print_image(pil_image)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)