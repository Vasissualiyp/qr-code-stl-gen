import qrcode
import numpy as np
from PIL import Image

# taking image which user wants 
# in the QR code center
Logo_link = './test.png'
 
logo = Image.open(Logo_link)
 
# taking base width
basewidth = 100
 
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr_matrix = QRcode.get_matrix()
qr_matrix_size = len(qr_matrix)
basewidth = qr_matrix_size

# adjust image size
#wpercent = (basewidth/float(logo.size[0]))
#hsize = int((float(logo.size[1])*float(wpercent)))
hsize = basewidth
#logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
 
# taking url or text
url = 'https://www.zou-mse-utoronto-ca.net/'
 
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make()
 
# # taking color name from user
# QRcolor = 'Black'
 
# adding color to QR code
QRimg = QRcode.make_image( back_color="white").convert('RGB')

# set size of QR code
logo_sizex = logo.size[0]
logo_sizey = logo.size[1]
pos = ((QRimg.size[0] - logo_sizex) // 2,
       (QRimg.size[1] - logo_sizey) // 2)

# Paste logo
#QRimg.paste(logo, pos)

# save the QR code generated
QRimg.save('./qrout.png')
qr_matrix = QRcode.get_matrix()
 
print('QR code generated!')
print(len(qr_matrix))
