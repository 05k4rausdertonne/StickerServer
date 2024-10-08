from escpos.printer import Usb
from PIL import Image, ImageFilter

# vendor_id = 0x28e9
# product_id = 0x0289
class Printer:
    def __init__(self, vendor_id, product_id):
        try:
            self.printer = Usb(vendor_id, product_id, 0, timeout=5000)
            self.printer.open()
        except Exception as e:
            self.printer = None
            print(f"Warning: Failed to initialize the USB printer. Error: {e}")


    def print_image(self, img, auto_rotate=False, print_width=384, edge_enhance=True):

        if self.printer == None:
            try:
                self.printer = Usb(vendor_id, product_id, 0, timeout=5000)
                self.printer.open()
            except Exception as e:
                self.printer = None
                print(f"Warning: Failed to initialize the USB printer. Error: {e}")
                print("Aborting print!")
                return False

        img = img.convert("L")

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

        if edge_enhance:
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        
        # print image
        self.printer.ln()
        self.printer.image(img, impl="bitImageColumn")

        return True
        

    def print_spacer(self, px=10, print_width=384):

        if self.printer == None:
            try:
                self.printer = Usb(vendor_id, product_id, 0, timeout=5000)
                self.printer.open()
            except Exception as e:
                self.printer = None
                print(f"Warning: Failed to initialize the USB printer. Error: {e}")
                print("Aborting print!")
                return False

        spacer = Image.new('1', (print_width, px), 'white')
        self.printer.ln()
        self.printer.image(spacer, impl="bitImageColumn")
        return True


    # def feed_lines(self, feed_lines):
    #     print(f"feeding {feed_lines} lines")
    #     self.printer.ln(count=feed_lines)


    def close_connection(self):
        self.printer.close()