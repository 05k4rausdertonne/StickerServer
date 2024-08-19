from escpos.printer import Usb
from PIL import Image

# Replace with your actual Vendor ID and Product ID
vendor_id = 0x28e9
product_id = 0x0289

# Resize image to fit the printer width
img = Image.open("test.jpg").convert("L")


p = Usb(vendor_id, product_id, 0, timeout=5000)

p.text("Hello World\n")
p.ln(5)
p.text("Hello World again\n")
# p.image(img, impl="bitImageColumn")
p.ln(2)
p.close()