#!/usr/bin/python
# -*- coding: utf-8 -*.

import sys
import os
import logging
import argparse
import graypy
import json
from fmtparser import parse_log_string

def bailout(msg):
    sys.stderr.write(msg + '\n')
    exit(1)


def check_args():
    loglevels = { 'DEBUG': logging.DEBUG,
                  'INFO': logging.INFO,
                  'WARNING': logging.WARNING,
                  'ERROR': logging.ERROR,
                  'CRITICAL': logging.CRITICAL }

    cmdline_options = { "facility": "PythonLogger",
                        "version": "1.0",
                        "level": 1,
                        "nolog": False,
                        "template": None,
                        "message": None,
                        "server": None,
                        "data": None,
                        "port": 12201 }

    parser = argparse.ArgumentParser(description='send a message to a graylog server',
        usage='%(prog)s [options] SERVER MESSAGE')

    parser.add_argument("server", help="graylog server name")
    parser.add_argument("message", help="message being sent or @FILENAME to read from FILENAME or - to read from StdIn")
    parser.add_argument("-l", "--level", help="log level (defaults to ALERT)", choices=loglevels)
    parser.add_argument("-f", "--facility", help="facility name (defaults to 'PythonLogger')")
    parser.add_argument("-p", "--port", help="graylog port (defaults to 12201)", type=int)
    parser.add_argument("-d", "--data", help="additional data field (key:value)", action="append")
    parser.add_argument("-t", "--template", help="specify template to parse log message", type=str)
    parser.add_argument("-n", "--nolog", help="do not log, simulate and show on console", action="store_true")
    args = parser.parse_args()

    cmdline_options['server'] = args.server

    # process message, may be a string, a file ref starting with '@'
    # or a dash to read from stdin
    if args.message.startswith('@'):
        fname = args.message[1:]
        if os.path.exists(fname):
            cmdline_options['message'] = open(fname).read()
        else:
            bailout('file {0} not found'.format(fname))
    else:
        if args.message.strip() == '-':
            _fullmsg = ""
            for line in iter(sys.stdin.readline, ""):
                _fullmsg += line + ' '
            cmdline_options['message'] = _fullmsg
        else:
            cmdline_options['message'] = args.message

    # check port override
    if args.port is not None:
        cmdline_options['port'] = args.port

    # process facility option
    if args.facility is not None:
        cmdline_options['facility'] = args.facility

    # process template option
    if args.template is not None:
        cmdline_options['template'] = args.template

    # process simulation option
    if args.nolog is not None:
        cmdline_options['nolog'] = True

    # set the level
    if args.level is not None:
        cmdline_options['level'] = loglevels[args.level.upper()]

    # process additional data fields, if present
    cmdline_options['data'] = {}
    if args.data is not None:
        for entry in args.data:
            entry = entry.strip().split(':')
            key = entry[0]
            value = ''.join(entry[1:])
            cmdline_options['data'][key] = value

    return cmdline_options


def main():
    try:
        args = check_args()
        my_logger = logging.getLogger(args['facility'])
        my_logger.setLevel(args['level'])
        handler = graypy.GELFHandler(args['server'], args['port'], debugging_fields=False)
        my_logger.addHandler(handler)
        d = args['data']

        if args['template'] is not None:
            parsing = parse_log_string(args['template'], args['message'])
            d.update(parsing)

        if args['nolog'] is True:
            print(u'Simulation mode:')
            print(u'Log level: {0}'.format(args['level']))
            print(u'Facility: {0}'.format(args['facility']))
            print(u'Server: {0}'.format(args['server']))
            print(u'Message: {0}'.format(args['message']))
            print(u'Custom fields: {0}'.format(json.dumps(d)))
        else:
            my_logger.log(args['level'], args['message'], extra=d)
    except Exception as e:
       bailout("Exception during log operation: {0}".format(e))

if __name__ == '__main__':
    main()
