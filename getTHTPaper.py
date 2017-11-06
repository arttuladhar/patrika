#!/usr/bin/python

import datetime
import urllib
import os, sys
import re
import shutil
from pyPdf import PdfFileWriter, PdfFileReader


def main(date):
      
  _paperDirectoryOutput = "paper"
  _urlbase = "http://epaper.thehimalayantimes.com/epaperimages/"
  cachedPaperDir = "cache/" + date
  
  paperURL = _urlbase + date + "/"

  # Creating Daily Directory
  if not os.path.exists(cachedPaperDir):
    os.mkdir(cachedPaperDir, 0755)
  else:
    print "Directory Exists"

  print "Download Directory: ", cachedPaperDir

  # Printing Paper
  startIndex = 1
  resume = True

  while (resume == True):
    pageURL = paperURL + date + "-MD-HR-" + str(startIndex) + ".pdf"
    print "Downloading Page: ", pageURL
    resume = download_file(pageURL, cachedPaperDir, startIndex)
    startIndex += 1

  # Merging PDF
  outputFileName = "TheHimalayanTimes-" + date
  mergePDF(cachedPaperDir, _paperDirectoryOutput, outputFileName)

  # Cleanup
  print "Deleting: ", cachedPaperDir
  shutil.rmtree(cachedPaperDir)

  print "Program End"


def download_file(download_url, location, part):
  """Downloads PDF Page via download_url to certain location.
     Supports sequential numeration for multi-part download file for later merge.

  Returns:
    Boolean value for completed multi-parted download
  """

  _continue = False;

  # Check URI Exists
  response = urllib.urlopen(download_url)
  responseCode = response.getcode()

  if (responseCode == 200):
    file = open( location + "/" + str(part) + ".pdf", "w");
    file.write(response.read())
    file.close()
    print ("Download Complete")
    _continue = True;
  else:
    print "File Doesn't Exists"
    _continue = False;

  print "Closing the URL Object"
  response.close()
  return _continue

def mergePDF(_inputDir, _outputDir, fileName):
  """Merges Multiple PDF Files to Single PDF File
  """
  now = datetime.datetime.now()
  mergePDF_ddmmyy = "{:02d}{:02d}{:02d}".format(now.day, now.month, now.year)

  _outputFileMerged = _outputDir + "/" + fileName

  fileList = []
  output = PdfFileWriter()

  # Iterating Through All Files for _inputDirectory
  for fn in os.listdir(_inputDir):
    fileList.append(fn)

  #Sort
  fileList.sort(key=lambda x: (int(re.sub('\D','',x)),x))

  for _file in fileList:
    append_pdf(PdfFileReader(file(_inputDir + "/" + _file, "rb")),output)

  output.write(file(_outputFileMerged + ".pdf","wb"))

# Creating a routine that appends files to the output file
def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]


if __name__ == "__main__":
      
  now = datetime.datetime.now()
  ddmmyy = "{:02d}{:02d}{:02d}".format(now.day, now.month, now.year)

  ## Check if File Exists
  for root, dirs, files in os.walk('paper'):
    print (files)
    if ddmmyy in files:
      print "File Already Exists"
      sys.exit();
  
  main(ddmmyy)