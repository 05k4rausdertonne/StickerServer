from escpos.printer import Usb
from PIL import Image, ImageFilter

# vendor_id = 0x28e9
# product_id = 0x0289
class Printer:
    def __init__(self, vendor_id, product_id):
        self.printer = Usb(vendor_id, product_id, 0, timeout=5000)
    
    def print_image(self, img, auto_rotate=False, print_width=384, feed_lines=1):
        self.printer.open()
        img = img.convert("L").filter(ImageFilter.EDGE_ENHANCE)
        width, height = img.size
        if auto_rotate and width > height:
            # rotate image
            img = img.rotate(90, expand=True)
            # and swap width and height
            width, height = height, width

        # scale the image to max printable width
        scalar = print_width / width
        new_size = (int(width * scalar), int(height * scalar))
        img = img.resize(new_size, Image.LANCZOS)
        
        # print image
        self.printer.ln()
        self.printer.image(img, impl="bitImageColumn")
        for _ in range(feed_lines):
            self.printer.textln(txt='\n')
        self.printer.close()

    def feed_lines(self, feed_lines):
        self.printer.open()
        print(f"feeding {feed_lines} lines")
        self.printer.ln(count=feed_lines)
        self.printer.close()
