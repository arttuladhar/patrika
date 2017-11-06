#!/usr/bin/python

import datetime
import urllib
import os, sys
import re
import shutil
from pyPdf import PdfFileWriter, PdfFileReader


def main(date):
      
  _paperDirectoryOutput = "paper"
  _urlbase = "http://epaper.ekantipur.com/epaper/the-kathmandu-post/"  
  pageURL = _urlbase + date + "/" + date + ".pdf"

  print ("Downloading Page: ", pageURL)
  outputFilePath = _paperDirectoryOutput + "/TheKathmanduPost-" + date
  download_file(pageURL, outputFilePath)
  
  print "Program End"


def download_file(download_url, location):
  """Downloads PDF Page via download_url to certain location.
  Returns:
    Boolean value for completed multi-parted download
  """

  # Check URI Exists
  response = urllib.urlopen(download_url)
  responseCode = response.getcode()

  if (responseCode == 200):
    file = open( location + ".pdf", "w");
    file.write(response.read())
    file.close()
    print ("Download Complete")
  else:
    print "File Doesn't Exists"

  print "Closing the URL Object"
  response.close()
  return

if __name__ == "__main__":
      
  now = datetime.datetime.now()
  ddmmyy = "{:02d}-{:02d}-{:02d}".format(now.year, now.month, now.day)

  ## Check if File Exists
  for root, dirs, files in os.walk('paper'):
    print (files)
    if 'TheKathmanduPost-' + ddmmyy + '.pdf' in files:
      print "File Already Exists"
      sys.exit();
  
  main(ddmmyy)