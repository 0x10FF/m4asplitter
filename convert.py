#!/usr/bin/env python

import os, commands, sys, re
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--filename",
                action="store", type="string", dest="filename", help="audio book input file, .m4a file for example")
parser.add_option("-o", "--outdir",
                action="store", type="string", dest="outdir", help="where to put .mp3 files for each section, if not provided current directory will be used")
options, args = parser.parse_args()

if not options.filename:
    parser.print_help()
    sys.exit(1)

#----------------- lets get started
titleLinePattern = re.compile("title.+\:(.*)$", re.IGNORECASE)
chapterPattern = re.compile("start ([\d\.]+), end ([\d\.]+)", re.IGNORECASE)
GET_INFO_CMD = "ffmpeg -i {0}".format(options.filename)
CONVERT_FFMPEG_CMD = "ffmpeg -i {0} -ss {1} -t {2} {3}"

def extractStartEndFromLine(line):
    start = 0.0
    end = 0.0
    chaptersResult = chapterPattern.search(line)
    if chaptersResult:
        start = float(chaptersResult.group(1))
        end = float(chaptersResult.group(2))
        
    return start, end

def extractTitleFromLine(line):
    title = None

    titleResult = titleLinePattern.search(line)
    if titleResult:
        title = str(titleResult.group(1))

    return title

def makeChapterFile(chapterIndex, title, start, end):
        safeTitle = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).strip()
        outFile = "'{0}/{1}_{2}.mp3'".format(outdir, chapterIndex, safeTitle)
        
        print CONVERT_FFMPEG_CMD.format(options.filename, start, end, outFile)

        if not os.path.isfile(outFile):
            CMD = CONVERT_FFMPEG_CMD.format(options.filename, start, end, outFile)
            ffmpegOut = commands.getstatusoutput(CMD)
            if ffmpegOut[0] == 0:
                print "success, created {0}".format(outFile)
            else:
                print ffmpegOut
        else:
            print "{0} already exists, ignoring..."

cmdTuple = commands.getstatusoutput(GET_INFO_CMD)

lineList = cmdTuple[1].split("\n")
lineIndex = 0

outdir = '.'
if options.outdir:
    outdir = options.outdir

sectionCount = 1 #start counting from chapters from 1
for lineIndex in range(len(lineList)):

    start, end = extractStartEndFromLine(lineList[lineIndex])
    end = end - start

    if start > 0 or end > 0:
        line = lineList[lineIndex+2]
        title = extractTitleFromLine(line)
        print "{0}: {1}-{2}".format(title, start, end)
        makeChapterFile(sectionCount, title, start, end)
        sectionCount += 1
