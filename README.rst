
**********
graylogger
**********

Introduction
============

*graylogger* is a python script born out of necessity. Use *graylogger.py* to send GELF-formatted messages to a graylog host.
You may log string messages, file contents or read from stdin, add additional fields. Host name and timestamp will be provided
automatically.


Usage
=====

The help option `-h` displays the usage page::

  ./graylogger.py -h

  usage: graylogger.py [options] SERVER MESSAGE

  send a message to a graylog server

  positional arguments:
    server                graylog server name
    message               message being sent or @FILENAME to read from FILENAME
                            or - to read from StdIn

  optional arguments:
    -h, --help            show this help message and exit
    -l {DEBUG,INFO,WARNING,CRITICAL,ERROR}, --level {DEBUG,INFO,WARNING,CRITICAL,ERROR}
                          log level (defaults to ALERT)
    -f FACILITY, --facility FACILITY
                          facility name (defaults to 'PythonLogger')
    -p PORT, --port PORT  graylog port (defaults to 12201)
    -d DATA, --data DATA  additional data field (key:value)
    -t TEMPLATE, --template TEMPLATE specify log message template
    -n, --nolog           do not log, simulate and show on console


Custom fields
=============

Use the `-d` (or `--data`) option to supply additional fields to graylogger. The value consists of the field name and the
field value, separated by a comma. If the field name or value contain white space, make sure to quote the fiel data
(e.g. `-d "Merchant:ACME Inc."`). Separator is the first comma, so it is perfectly to valid to have a comma in the field value string.
You may provide an arbitrary number of `-d` options as shown below::

  ./graylogger.py -l DEBUG -f "ETL" graylog.company.example.com "Start pricing ETL job" -d "Merchant:ACME Inc." -d Database:pricing_prod

Examples
========

Using a message string
----------------------
The message parameter is a string. If you have whitespace in the string, be sure to enclose it in quotes::

  ./graylogger.py -l DEBUG -f "ETL" graylog.company.example.com "Processing startet at `date +%s`"

Piping to graylogger
--------------------
Using a single dash character `-` as the message, graylogger will read from standard input::

 output_generating_program | ./graylogger.py -l INFO -f "ETL" graylog.company.example.com -

Reading from a file
-------------------
If the first character of the message parameter is a `@`, the message will be read
from the file name directly following the `@`, e.g. `@result.txt`. If needed, a path
may be specified (e.g. `@/tmp/some/file.log`)::

  ./graylogger.py -l WARNING -f "ETL" graylog.company.example.com @warnings.txt


Credits and Thank You
=====================

 * Sever Banesiu and Daniel Miller for their graypy package hosted at https://github.com/severb/graypy
 * Peter Fröhlich for valuable feedback and ideas


License
=======

MIT License

Copyright (c) 2013 Armin Hanisch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
