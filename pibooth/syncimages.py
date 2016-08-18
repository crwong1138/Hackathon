#! /usr/bin/env python2.7
# -*- coding: UTF8 -*-

import sys, os, glob, re, boto
from boto.s3.key import Key

# make pathnames easier
os.chdir(os.path.dirname(sys.argv[0]))

if sys.platform == "raspberrypi":
  import RPi.GPIO as GPIO

bin = os.path.basename(sys.argv[0])

def setPinHigh(pin):
  if sys.platform == "raspberrypi":
    GPIO.output(pin, GPIO.HIGH)

def setPinLow(pin):
  if sys.platform == "raspberrypi":
    GPIO.output(pin, GPIO.LOW)

def getBucket(bucketName):
  print("connecting to s3")
  conn = boto.connect_s3()
  bucket = conn.get_bucket(bucketName)
  bucketlocation = bucket.get_location()
  if bucketlocation:
    print("reconnecting to " + bucketlocation)
    conn = boto.s3.connect_to_region(bucketlocation)
    bucket = conn.get_bucket(bucketName)
  else:
    print("could not get bucketlocation, sticking with whatever s3 thinks is the right answer")
  return(bucket)
  
def percent_cb(complete, total):
  sys.stdout.write('.')
  sys.stdout.flush()

def getLocalFiles(d, e):
  # get all files in directory "d" with extension "e"
  return [os.path.basename(x) for x in glob.glob(str(d) + "*" + e)]

def removefile(f):
  print('removing local file {}'.format(f))
  os.remove(f)

# only returns objects in the bucket "b" that is "in" the "i" directory
def getObjectNames(b, i):
  prog = re.compile("^" + i)
  return [ x.name for x in b.list() if prog.match(x.name) ]

def alreadyInBucket(f, bl):
  # returns true if file "f" is in bucketlist "bl"
  # (bl is a list of objects)
  # should short circuit a return once it finds a match
  return (len([ x for x in bl if (x == f) ])>0)

def upload_S3(b, f, k, o, pin):
  if (alreadyInBucket(f, o)):
    print('Skipping {} because it is already in the bucket {}'.format(f, b))
  else:
    print('Uploading {} to Amazon S3 bucket {}'.format(f, b.name))
    k.key = f
    setPinHigh(pin)
    k.set_contents_from_filename(f, cb=percent_cb, num_cb=10)
    setPinLow(pin)
    print('')
    #removeLocal(imagedir, f)

def main():
  extension = '.png'
  bucketName = "buckethead9"
  imagedir = "images/"
  pin = 7

  bucket = getBucket(bucketName)
  key = Key(bucket)
  objects = getObjectNames(bucket, imagedir) # keep this out of loop
  for f in getLocalFiles(imagedir, extension):
    photo = imagedir + f
    upload_S3(bucket, photo, key, objects, pin)

if __name__ == "__main__":
  main()
