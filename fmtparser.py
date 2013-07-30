#!/usr/bin/python
# -*- coding: utf-8 -*.

def parse_log_string(format_description, input_string):
    DELIMITERS = {'open': ['"', '[', '(', '|'], 'close': ['"', ']', ')', '|']}
    identifier_list = format_description.strip().split(" ")
    wo = 0
    result = {}

    for identifier in identifier_list:
        open_delim = None
        close_delim = None

        if identifier[0:1] in DELIMITERS['open']:
            open_delim = identifier[0:1]
            identifier = identifier[1:]

        if identifier[-1] in DELIMITERS['close']:
            close_delim = identifier[-1]
            identifier = identifier[0:-1]

        while input_string[wo:wo + 1] in [' ', '\t']:
            wo += 1

        token = ''
        if open_delim is not None:
            while input_string[wo:wo + 1] != open_delim and input_string[wo:wo + 1] != '':
                wo += 1
            token = open_delim
            wo += 1

        if close_delim is not None:
            while input_string[wo:wo + 1] != close_delim and input_string[wo:wo + 1] != '':
                token += input_string[wo:wo + 1]
                wo += 1
            token += close_delim
            wo += 1
        else:
            while input_string[wo:wo + 1] not in [' ', '\t'] and input_string[wo:wo + 1] != '':
                token += input_string[wo:wo + 1]
                wo += 1

        result[identifier] = token

    return result

