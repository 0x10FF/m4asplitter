m4asplitter
===========

m4a audio book chapter splitter with ffmpeg

Usage
==========
<p>
<code>
Usage: convert.py [options]

Options:
  -h, --help            show this help message and exit
  -c FILENAME, --convervative=FILENAME
                        use beginning of next chapter as end for previous
                        chapter
  -f FILENAME, --filename=FILENAME
                        audio book input file, .m4a file for example
  -o OUTDIR, --outdir=OUTDIR
                        where to put .mp3 files for each section, if not
                        provided current directory will be used
</code>
</p>