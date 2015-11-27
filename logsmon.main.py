#!/usr/bin/python
# -*- coding: utf8 -*-
# v.1.0.3

import time

__author__ = 'fosterkh'


# Functions

def tail(filenames, timeout):
    in_files = [open(filename) for filename in filenames]
    for f in in_files:
        f.seek(0, 2)
    while True:
        for f in in_files:
            s_line = f.readline().rstrip('\n')
            if not s_line:
                continue
            yield s_line
        if not s_line:
            time.sleep(timeout)
            continue


def process_matches(match_text, deny_list, log_file):
    while True:
        s_line = (yield)
        if match_text in s_line:
            for deny_matches in deny_list:
                if deny_matches in s_line:
                    break
            else:
                # log_line = in_log_file + '\t' + s_line
                log_line = s_line
                print log_line
                log_file.write(log_line + '\n')


def text_file_2_list(text_filename):
    line_list = []
    try:
        text_file = open(text_filename, 'r')
        line_list = [s_line.strip() for s_line in text_file if s_line.strip() and s_line[0] != '#']
        # print line_list
        text_file.close()
    finally:
        return line_list

# Main Code

time_interval = 0.01
result_log_filename = 'test.out.log'
filename_list = ('log_file_to_monitor.txt', 'list_of_matches.txt', 'deny_list_of_matches.txt')
log_file_to_monitor, list_of_matches, deny_list_of_matches = [text_file_2_list(filename) for filename in filename_list]

result_log_file = open(result_log_filename, 'a')
matches = [process_matches(string_match, deny_list_of_matches, result_log_file) for string_match in list_of_matches]

for m in matches:   # prime matches
    m.next()

while True:
    audit_log = tail(log_file_to_monitor, time_interval)
    for line in audit_log:
        for m in matches:
            m.send(line)
