import datetime
import urllib
import os, sys
import re
from pyPdf import PdfFileWriter, PdfFileReader


def main():

  now = datetime.datetime.now()
  print ("Month: %d" %now.month)
  print ("Day: %d" %now.day)
  print ("Year: %d" %now.year)

  _urlbase = "http://epaper.thehimalayantimes.com/epaperpdf/"
  _urlMMDDYY = str(now.day) + str(now.month) + str(now.year)
  paperURL = _urlbase + _urlMMDDYY + "/"

  _paperDirectory = "paper/" + _urlMMDDYY

  # Creating Daily Directory
  if not os.path.exists(_paperDirectory):
    os.mkdir(_paperDirectory, 0755)
  else:
    print "Directory Exists"

  print "Download Directory: ", _paperDirectory


  # Printing Paper
  startIndex = 1
  resume = True

  while (resume == True):
    pageURL = paperURL + _urlMMDDYY + "-md-hr-" + str(startIndex) + ".pdf"
    print "Downloading Page: ", pageURL
    resume = download_file(pageURL, _paperDirectory, startIndex)
    startIndex += 1

  # Merging PDF
  _paperDirectoryMerge = _paperDirectory + "/merged"
  mergePDF(_paperDirectory, _paperDirectoryMerge)

  print "Program End"


def download_file(download_url, location, part):

  _continue = False;

  # Check File Exists
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

def mergePDF(_inputDir, _outputDir):
  print "InputDir: ", _inputDir
  print "OutputDir: ", _outputDir

  _now = datetime.datetime.now()
  _outputFileMerged = "THT-" + str(_now.month) + str(_now.day) + str(_now.year)

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
  main()