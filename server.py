from flask import Flask, request

app = Flask(__name__)

@app.route('/label', methods=['GET'])
def label():
    # Get the 'text' argument from the URL
    text = request.args.get('text')
    
    if text:
        # Print the text to the console
        print(f"Received text: {text}")
        return f"Text received: {text}", 200
    else:
        return "No text provided", 400

if __name__ == '__main__':
    app.run(debug=True)