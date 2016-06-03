import argparse
import dateutil.parser
import logging
import pandas
import csv
import os
import sys
import base64
import math
import Image


import skyrec


class Data(object):
    def __init__(self, data):
        [setattr(self, key, value) for key, value in data.items()]

    def make_request_message(self):
        with open(self.path, 'rb') as image:
            data = {
                'image': base64.b64encode(image.read()).decode('ascii')
            }
        message = skyrec.MessageOut(data)
        return message


def cloud_area_fraction_to_octal(cloud_area_fraction):
    return math.floor((cloud_area_fraction / 100) * 8)


def cloud_area_fraction_to_symbol(cloud_area_fraction):
   # Sun
   if cloud_area_fraction < 0.13:
      return 1
   # Partly cloudy
   elif cloud_area_fraction < 0.38:
      return 2
   # Mostly cloudy
   elif cloud_area_fraction < 0.86:
      return 3
   # Cloudy
   else:
      return 4


def octal_to_symbol(octal):
   cloud_area_fraction = octal_to_percent(octal) / 100
   return cloud_area_fraction_to_symbol(cloud_area_fraction)


def octal_to_percent(octal):
    return (octal * 100) / 8


def unserialize_datetime(dt):
    return dateutil.parser.parse(dt)


def get_icon_filename(path, symbol):
   return "%s/%d.png" % (path, symbol)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s: (%(levelname)s) %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S%Z',
                        level=logging.INFO)

    parser = argparse.ArgumentParser(description="Overlays a weather symbol on images")
    parser.add_argument('addr', type=str, help='ZeroMQ bind address')
    parser.add_argument('inputs', type=str, help='filenames of input image', nargs='+')
    parser.add_argument('outputpath', type=str, help='path where files should be saved')
    parser.add_argument('--iconpath', type=str, help='Path to icon images', default='contrib', required=False)
    args = parser.parse_args()

    pipeline = skyrec.DataReqPipeline(args.addr)

    for input_filename in args.inputs:
       data = Data({'path':  input_filename})
       logging.debug('Start processing %s', data.path)
       request = data.make_request_message()
       pipeline.send(request)
       response = pipeline.recv()

       # Determine weather symbol
       cloud_area_fraction = response.data['cloud_area_fraction']
       symbol = cloud_area_fraction_to_symbol(cloud_area_fraction)
       icon_filename = get_icon_filename(args.iconpath, symbol)

       # Create overlay image
       background = Image.open(input_filename)
       overlay = Image.open(icon_filename)

       background = background.convert("RGBA")
       overlay = overlay.convert("RGBA")

       background.paste(overlay, (20,20))
       output_filename = "%s/%s" % (args.outputpath, input_filename.split('/')[-1])
       background.save(output_filename, "jpeg")
