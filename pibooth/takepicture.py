#! /usr/bin/env python2.7
# -*- coding: UTF8 -*-

import sys, os, glob, re
from datetime import datetime  
from subprocess import call  
from wand.color import Color
from wand.display import display
from wand.drawing import Drawing
from wand.font import Font
from wand.image import Image

# make pathnames easier
os.chdir(os.path.dirname(sys.argv[0]))

bin = os.path.basename(sys.argv[0])

def setup(pin):
  if sys.platform == "raspberrypi":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

def docommand(cmd):
#  os.system("pwd");
#  os.system("ls");
#  print("running command: " + cmd)
  try:
    retcode = call([cmd], shell=True)
    if retcode < 0:
      print >>sys.stderr, "Command was terminated by signal", -retcode
    else:
      print >>sys.stderr, "Command returned", retcode
  except OSError as e:
    print >>sys.stderr, "Command failed:", e

def displayOnPiTFT(photo, pin):
  cmd = 'fbi -T 2 -d /dev/fb1 -noverbose -a ' + photo
  setPinHigh(pin)
  docommand(cmd)
  setPinLow(pin)

def photoShoot(photo, w, h, pin):  
  cmd = 'raspistill -t 500 -w ' + str(w) + ' -h ' + str(h) + ' --rotation 180 -o ' + photo
  print("about to take photo")
  setPinHigh(pin)
  docommand(cmd)
  setPinLow(pin)

# Add text overlay of data on the photo we just took  
def addCaption(f, date, w, h):
  with Image(filename=f) as theImage:
    captionHeight=int(theImage.height/8)
    bg = Color('#0008')
    with Image(width=w+2, height=captionHeight+2, background=bg) as canvas:
      with Drawing() as context:
        mystring = "hackathon!  taken " + date.strftime('%-I:%M%p on %A, %B %-d, %Y')
        font = Font(path="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
        context.fill_color = Color('white')
        context.font_style = 'italic'
        context.font_size = 36
        context.text(x=130, y=(2*captionHeight/3)+2, body=mystring)
        context(canvas)
        theImage.watermark(image=canvas, transparency=0.0, left=0, top=theImage.height-captionHeight)
    with Image(filename="little_n.png") as logo:
      theImage.watermark(image=logo, transparency=0.0, left=9, top=theImage.height-logo.height-4)
    theImage.save(filename=f)

def setPinHigh(pin):
  if sys.platform == "raspberrypi":
    GPIO.output(pin, GPIO.HIGH) 

def setPinLow(pin):
  if sys.platform == "raspberrypi":
    GPIO.output(pin, GPIO.LOW)

def main():
  # image dimensions
  width=1200
  height=700
  extension = '.png'
  imagedir = "images/"
  pin = 8
  setup(pin)
  date = datetime.now()  
  photo = imagedir + re.sub("\..*$", "", bin) + "_" + date.strftime('%Y%m%d-%H%M%S')  + extension
  photoShoot(photo, width, height, pin)
  addCaption(photo, date, width, height)
  print(photo)
#  displayOnPiTFT(photo, pin)

if __name__ == "__main__":
  main()
