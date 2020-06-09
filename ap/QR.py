#!/usr/bin/env python3

# import qrcode

# # content
# data = "s3587391 - Shukun Lin"
# # generate
# img = qrcode.make(data=data)

# img.show()
# # img.save("Name.jpg")

import zxing
from tkinter import filedialog
import os

reader = zxing.BarCodeReader()

my_filetypes = [('all files', '.*'), ('text files', '.txt')]

path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetypes)
barcode = reader.decode(path)
print(barcode.parsed)