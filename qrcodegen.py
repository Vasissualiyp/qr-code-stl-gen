import qrcode
import numpy as np
from PIL import Image
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer, VerticalBarsDrawer

def generate_qr_code(url, vistype='square', basewidth=None, Logo_link=None):
    """
    Generate QR code from the url.
    Parameters:
        url (str) - url that QR code should contain
        vistype (str) - type of the QR code (square or round)
        basewidth (int) - size of the image in px
        Logo_link (str) - file path of the logo to put in 
                          the center of the QR code
    """
    
    # taking image which user wants 
    # in the QR code center
    if Logo_link:
        logo = Image.open(Logo_link)
     
    QRcode = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr_matrix = QRcode.get_matrix()
    qr_matrix_size = len(qr_matrix)

    # If basewidth not defined, make it the size of the QR code
    # Else, do as before
    if not basewidth:
        hsize = qr_matrix_size
    else:
        # adjust image size
        wpercent = (basewidth/float(logo.size[0]))
        hsize = int((float(logo.size[1])*float(wpercent)))
        logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
     
    # adding URL or text to QRcode
    QRcode.add_data(url)
     
    # generating QR code
    QRcode.make()
     
    # # taking color name from user
    # QRcolor = 'Black'

    # adding color to QR code
    if vistype == 'round':
        QRimg = QRcode.make_image( back_color="white",image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGB')
    elif vistype == 'square':
        QRimg = QRcode.make_image( back_color="white").convert('RGB')
    
    # Paste the logo in the QR code center
    if Logo_link:
        logo_sizex = logo.size[0]
        logo_sizey = logo.size[1]
        pos = ((QRimg.size[0] - logo_sizex) // 2,
               (QRimg.size[1] - logo_sizey) // 2)
        
        # Paste logo
        QRimg.paste(logo, pos)
    
    # save the QR code generated
    QRimg.save('./qrout.png')
     
    print('QR code generated!')

    return QRcode

if __name__ == '__main__':
    url = 'https://www.zou-mse-utoronto-ca.net/'
    vistype = 'square'
    vistype = 'round'
    QRcode = generate_qr_code(url, vistype = vistype)
