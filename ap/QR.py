#!/usr/bin/env python3

import qrcode
import os
import zxing
from tkinter import filedialog

# content
data = "engineer, abc123"
# generate
img = qrcode.make(data=data)

img.show()
img.save(os.path.join(os.getcwd(), "ap\QR image\engineer.jpg"))

# reader
reader = zxing.BarCodeReader()

# my_filetypes = [('all files', '.*'), ('text files', '.txt')]

# path = filedialog.askopenfilename(initialdir=os.getcwd(),
#                                     title="Please select a file:",
#                                     filetypes=my_filetypes)

# decode
barcode = reader.decode(os.path.join(os.getcwd(), "ap\QR image\engineer.jpg"))
# print(barcode.parsed.split(', ')[0])
print(barcode.parsed)