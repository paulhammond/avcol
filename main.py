#!/usr/bin/env python

# avcol - image analysis on Google App Engine
# http://www.paulhammond.org/2010/08/avcol/
#
# Copyright (c) 2010 Paul Hammond
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from google.appengine.api import images
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from django.utils import simplejson
import wsgiref.handlers
import urllib2
import png
import os

class MainHandler(webapp.RequestHandler):

  def get(self):

      url = self.request.get('url')

      # go grab the image
      result = urllib2.urlopen(url)

      # resize to a 20px thumbnail
      img = images.Image(result.read())
      img.resize(width=20, height=20)
      thumbnail = img.execute_transforms(output_encoding=images.PNG)

      # read the thumbnail
      r = png.Reader(bytes = thumbnail)
      png_w,png_h,pixels,info = r.asDirect()

      # analyze the pixel data
      pixelcount = red = blue = green = 0
      pixelcount = png_w * png_h
      for row in pixels:
        for pixel in png.group(row,info['planes']):
          red   = red   + pixel[0]
          green = green + pixel[1]
          blue  = blue  + pixel[2]

      data = {
        'url' : url,
        'mean': {
          'r':red/pixelcount, 
          'g':green/pixelcount, 
          'b':blue/pixelcount, 
          'hex':"#%02X%02X%02X" %(red/pixelcount,green/pixelcount,blue/pixelcount)
        }
      }

      if self.request.path == '/html':
          data['debug'] = {
             'w': png_w * 20,
             'h': png_h * 20,
          }
          path = os.path.join(os.path.dirname(__file__), 'templates/image.html')
          self.response.out.write(template.render(path, data))

      elif self.request.path == '/json':
          simplejson.dump(data,self.response.out)

def main():
  application = webapp.WSGIApplication([
                                          ('/json', MainHandler),
                                          ('/html', MainHandler),
                                      ])
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()