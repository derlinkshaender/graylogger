#!/usr/bin/python
# -*- coding: utf-8 -*.

import sys
import os


FMT = 'ip ident user [time] "request" status bytes'
input_string = '127.0.0.1 user-identifier frank [10/Oct/2000:13:56:08 -0700] "GET /apache_pb.zap HTTP/1.0" 404 0'

identifer_list = FMT.strip().split(" ")
wo = 0
result = []

for identifier in identifer_list:
	open_delim = None
	close_delim = None

	if identifier[0:1] in ['"', '[']: 
		open_delim = identifier[0:1]
		identifier = identifier[1:]

	if identifier[-1] in ['"', ']']: 
		close_delim = identifier[-1]
		identifier = identifier[0:-1]

	print 'Open: ', open_delim
	print 'Close: ', close_delim
	print 'identifier:', identifier
	print '--------'

	while input_string[wo:wo+1] in [' ', '\t']:
		wo += 1

	# now collect
	token = ''
	if open_delim is not None:
		while input_string[wo:wo+1] != open_delim:
			wo += 1

	if close_delim is not None:
		while input_string[wo:wo+1] != close_delim:
			token += input_string[wo:wo+1]
			wo += 1
	else:
		while input_string[wo:wo+1] not in [' ', '\t']:
			token += input_string[wo:wo+1]
			wo += 1

	print "Token: |{token}|".format(token=token)
	print '========'






