#!/usr/bin/env python

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

BOLD='\033[1m'
TEXT_RED='\033[31m'
TEXT_GREEN='\033[32m'
TEXT_YELLOW='\033[33m'
TEXT_BLUE='\033[34m'
TEXT_CYAN='\033[36m'
TEXT_WHITE_RED_BG='\033[37;41m'
RESET_FORMATTING='\033[0m'

import re
import sys

filters = [
    (r"(.*\[INFO\] .*)", TEXT_BLUE + BOLD + "\\1" + RESET_FORMATTING),
    (r"(.*\[DEBUG\] .*)", TEXT_CYAN + BOLD + "\\1" + RESET_FORMATTING),
    (r"(.*\[WARNING\] .*)", TEXT_YELLOW + BOLD + "\\1" + RESET_FORMATTING),
    (r"(.*\[ERROR\] .*)", TEXT_RED + BOLD + "\\1" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:,]+|[0-9:,]+) (INFO[ ]+)\[(.*)\] (.*)", "\\1 " + TEXT_BLUE + BOLD + "\\2" + RESET_FORMATTING + TEXT_BLUE + "[\\3]" + BOLD + " \\4" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:,]+|[0-9:,]+) (DEBUG[ ]+)\[(.*)\] (.*)", "\\1 " + TEXT_CYAN + BOLD + "\\2" + RESET_FORMATTING + TEXT_CYAN + "[\\3]" + BOLD + " \\4" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:,]+|[0-9:,]+) (WARN[I]*[ ]+)\[(.*)\] (.*)", "\\1 " + TEXT_YELLOW + BOLD + "\\2" + RESET_FORMATTING + TEXT_YELLOW + "[\\3]" + BOLD + " \\4" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:,]+|[0-9:,]+) (ERROR[ ]+)\[(.*)\] (.*)", "\\1 " + TEXT_RED + BOLD + "\\2" + RESET_FORMATTING + TEXT_RED + "[\\3]" + BOLD + " \\4" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:,]+|[0-9:,]+) (FATAL[ ]+)\[(.*)\] (.*)", "\\1 " + TEXT_WHITE_RED_BG + BOLD + "\\2" + RESET_FORMATTING + TEXT_WHITE_RED_BG + "[\\3]" + BOLD + " \\4" + RESET_FORMATTING),
    (r"(BUILD SUCCESSFUL)", BOLD + TEXT_GREEN + "\\1" + RESET_FORMATTING ),
    (r"(BUILD (FAILURE|FAIL))", BOLD + TEXT_RED + "\\1" + RESET_FORMATTING ),
    (r"\[INFO\] (BUILD SUCCESS)", "[INFO] " + BOLD + TEXT_GREEN + "\\1" + RESET_FORMATTING),
    (r"\[INFO\] (BUILD (FAILURE|FAIL))", "[INFO] " + BOLD + TEXT_RED + "\\1" + RESET_FORMATTING),
    (r"\[INFO\] (.*)(SUCCESS)", "[INFO] \\1" + BOLD + TEXT_GREEN + "\\2" + RESET_FORMATTING),
    (r"\[INFO\] (.*)(FAILURE|FAIL)", "[INFO] \\1" + BOLD + TEXT_RED + "\\2" + RESET_FORMATTING),
    (r"\[INFO\] (.*)(SKIPPED)", "[INFO] \\1" + BOLD + TEXT_YELLOW + "\\2" + RESET_FORMATTING),
    (r"([0-9-]+ [0-9:.]+)INFO([: ]+)(Started .*)", "\\1" + TEXT_GREEN + BOLD + "INFO\\2\\3" + RESET_FORMATTING),
]

i = 0
for f in filters:
    filters[i] = (re.compile(f[0], re.IGNORECASE), f[1])
    i+=1

test_filters = [
    r"Tests run: ([0-9]+), Failures: ([0-9]+), Errors: ([0-9]+), Skipped: ([0-9]+), Time elapsed: (.*)",
    r"Tests run: ([0-9]+), Failures: ([0-9]+), Errors: ([0-9]+), Skipped: ([0-9]+)",
    r"Passed: ([0-9]+) Failed: ([0-9]+) Total: ([0-9]+) \(ignored ([0-9]+)\) \(([0-9.]+) seconds\)"
]
i = 0
for f in test_filters:
    test_filters[i] = re.compile(f, re.IGNORECASE)
    i+=1

def colorize_test(num, color, colorZero):
    if num > '0':
        return BOLD + color + num + RESET_FORMATTING
    else:
        return BOLD + colorZero + num + RESET_FORMATTING

def test_filter(str):
    m = test_filters[0].search(str)
    if m:
        failures = colorize_test(m.group(2), TEXT_RED, TEXT_GREEN)
        errors = colorize_test(m.group(3), TEXT_RED, TEXT_GREEN)
        skipped = colorize_test(m.group(4), TEXT_YELLOW, TEXT_GREEN)

        str = str.replace(m.group(0), "Tests run: " + BOLD + TEXT_GREEN + m.group(1) + RESET_FORMATTING +
                ", Failures: " + failures +
                ", Errors: " + errors +
                ", Skipped: " + skipped +
                ", Time elapsed: " + BOLD + TEXT_CYAN + m.group(5) + RESET_FORMATTING)
        return str

    m = test_filters[1].search(str)

    if m:
        failures = colorize_test(m.group(2), TEXT_RED, TEXT_GREEN)
        errors = colorize_test(m.group(3), TEXT_RED, TEXT_GREEN)
        skipped = colorize_test(m.group(4), TEXT_YELLOW, TEXT_GREEN)
        str = str.replace(m.group(0), "Tests run: " + BOLD + TEXT_GREEN + m.group(1) + RESET_FORMATTING +
            ", Failures: " + BOLD + failures + RESET_FORMATTING +
            ", Errors: " + BOLD + errors + RESET_FORMATTING +
            ", Skipped: " + BOLD + skipped + RESET_FORMATTING)
        return str

    m = test_filters[2].search(str)

    if m:
        passed = colorize_test(m.group(1), TEXT_GREEN, TEXT_YELLOW)
        errors = colorize_test(m.group(2), TEXT_RED, TEXT_GREEN)

        skipped = colorize_test(m.group(4), TEXT_YELLOW, TEXT_GREEN)
        str = str.replace(m.group(0),
            "Passed: %s Failed: %s Total: %s (ignored %s) (%s seconds)" %
            (passed, errors, BOLD + TEXT_GREEN + m.group(3) + RESET_FORMATTING, skipped, BOLD + TEXT_CYAN + m.group(5) + RESET_FORMATTING))
        return str

    return str




def read_line_and_terminator():
    buff = StringIO()
    
    while True:
        ch = sys.stdin.read(1)
        
        if not ch or ch == "\r" or ch == "\n":
            return buff.getvalue(), ch
        
        buff.write(ch)

try:
    print("Colorizing...")

    while True:
        line, terminator = read_line_and_terminator()
        
        for f in filters:
            line = f[0].sub(f[1], line)

        line = test_filter(line)

        if len(line) > 0:
            sys.stdout.write(line)
            sys.stdout.write(RESET_FORMATTING)
            
            if terminator:
                sys.stdout.write(terminator)

            sys.stdout.flush()
        
        if not terminator:
            break
        
except KeyboardInterrupt:
    pass 
