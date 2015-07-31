#!/usr/bin/python
# -*- coding: utf8 -*-

__author__ = 'sford'

import time

# Functions

def tail(filenames):
    in_files = [open(filename) for filename in filenames]
    for f in in_files:
        f.seek(0, 2)
    while True:
        for f in in_files:
            line = f.readline().rstrip('\n')
            if not line:
                continue
            yield line
        if not line:
            time.sleep(0.01)
            continue

def process_matches(matchtext, deny_list, log_file):
    while True:
        line = (yield)

        if matchtext in line:
            for deny_matches in deny_list:
                if deny_matches in line:
                    break
            else:
                # log_line = in_log_file + '\t' + line
                log_line = line
                print log_line
                log_file.write(log_line + '\n')

# Main Code

log_file_to_monitor = ['/var/log/apache2/access.log',
                      '/var/log/apache2/error.log',
                      ]

result_log_file = 'out.log'

list_of_matches = ['ERROR', 'WARNING']
deny_list_of_matches = ['SSL error',
                        'account is disable',
                        ]

matches = [process_matches(string_match, deny_list_of_matches, open(result_log_file, 'a')) for string_match in list_of_matches]

for m in matches:   # prime matches
    m.next()

while True:
    auditlog = tail(log_file_to_monitor)
    for line in auditlog:
        for m in matches:
            m.send(line)
