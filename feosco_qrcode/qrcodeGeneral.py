#-*- coding:utf-8 -*-

from openerp.osv import osv, fields
import openerp
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

class ir_qrcode(osv.osv):

    _name = "ir.qrcode"

    def general_qrcode(self, cr, uid, vals, context={}):
        import qrcode

        size = 128, 128

        a = "No. :" + vals['id'] + "\n"+"QRcode : " + vals['code']

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=10,
        )
        qr.add_data(a)
        qr.make()
        im = qr.make_image()
        modpath = openerp.modules.get_module_path('feosco_qrcode')

        font = ImageFont.truetype(modpath + "/fonts/arial.ttf", 14)
        draw = ImageDraw.Draw(im)
        draw.text((80, 0), vals['name'], font=font)
        draw.text((80, 15), vals['code'], font=font)

        im.rotate(45).show()

        # im.thumbnail(size, Image.ANTIALIAS) # covert size image
        im.save(modpath + '/' + vals['id'] +".png")
        with open(modpath + '/' + vals['id'] +".png", "rb") as f:
            data = f.read()
            base64String = data.encode("base64")
            return base64String
