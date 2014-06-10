#!/usr/bin/env python
# coding: utf-8

###
#
# Roll up, roll up: it's...
#
#  /££      /££ /££                 /££  /££££   /££££££
# | ££  /£ | ££| ££                | ££ /££  ££ /££__  ££
# | ££ /£££| ££| £££££££  /££   /££| ££|__/\ ££| ££  \__/  /££££££   /££££££   /£££££££  /££££££
# | ££/££ ££ ££| ££__  ££| ££  | ££| ££    /££/|  ££££££  /££__  ££ |____  ££ /££_____/ /££__  ££
# | ££££_  ££££| ££  \ ££| ££  | ££|__/   /££/  \____  ££| ££  \ ££  /£££££££| ££      | ££££££££
# | £££/ \  £££| ££  | ££| ££  | ££      |__/   /££  \ ££| ££  | ££ /££__  ££| ££      | ££_____/
# | ££/   \  ££| ££  | ££|  £££££££ /££   /££  |  ££££££/| £££££££/|  £££££££|  £££££££|  £££££££
# |__/     \__/|__/  |__/ \____  ££|__/  |__/   \______/ | ££____/  \_______/ \_______/ \_______/
#                         /££  | ££                      | ££
# "Sort your life out."  |  ££££££/                      | ££
#                         \______/                       |__/
#
#     $   sudo cp whyspace.py /usr/local/sbin
#     $   sudo chmod +x /usr/local/sbin/whyspace
#     $   echo "alias why='/usr/local/sbin/whyspace'" > ~/.bashrc
#     $   source ~/.bashrc
#
#     $   why /path/to/code
#     $   why /path/to/file.php
#
# There is a possibility that there will be a conflict with an already
# existing program on Debian systems called "Why". If this is the case,
# please proceed to delete the other imposter.
#
# Happy Why!?spacing!
#
###

# Get all required modules.
import sys, os, getopt, re, fileinput

def parse(_l):

  # Convert tabs to spaces.
  _l = _l.expandtabs(2)

  # Check for occurences of " )", such as in padded if statements: if ( true ).
  # This is required instead of a straight string replace because of some false positives.
  _l = re.sub(r'(?<=\S)\s[)]', ')', _l)

  # Remove trailing whitespace.
  _l = re.sub(r'[ \t]+$', '', _l)

  # General stuff.
  _l = _l.replace('( ', '(')
  _l = _l.replace('){', ') {')
  _l = _l.replace(')  {', ') {')

  # Ensure a single space after any keywords.
  for word in ['if', 'for', 'foreach', 'while', 'do', 'try', 'else', 'elseif']:
    _l = re.sub(r'\b(%s)\b(\s*?)([\(\{])' % word, r'%s \3' % word, _l)

  # Casting.
  _l = re.sub(r'\((object|array|int|string|bool)\)(?=\S)', r'(\1) ', _l)

  # Push else onto a new line (instead of "} else {").
  _l = re.sub(r'^(.*?\s*?)(\}\s*?)((else|else\s*?if)\s*?[\{|\(].*?)$', r'\1}\n\1\3', _l)

  return _l

def fixFile(_file, _root):
  # Get full file path.
  filePath = os.path.join(_root, _file)
  print 'Whyspacing: %s' % filePath
  # Start the counter for lines changed.
  counter = 0
  # Open the file for reading & writing. The 'U' mode, rather than 'r', means it'll convert it to *NIX endings :)
  readz = fileinput.input(files = filePath, inplace = 1, mode = 'U')
  # Iterate through all lines.
  for line in readz:
    # Run the parse function on the line.
    new_line = parse(line)
    # Write it to stdout (this is picked up by the fileinput module to write the file in place)
    sys.stdout.write(new_line)
    # Increment the counter if the line has been changed.
    if line != new_line:
      counter += 1
  # Print the amount of lines changed to screen.
  print 'Lines fixed: ' + str(counter)

# Root directory should be the first agument passed; otherwise the current dir.
if len(sys.argv) > 1:
  rootDir = sys.argv[1]
else:
  rootDir = os.getcwd()

# Check if the input is a directory so we can traverse through each file.
if os.path.isdir(rootDir):
  # Recursively go through directories.
  for root, subFolders, files in os.walk(rootDir):
    # Filter out all files that aren't related to modules/PHP.
    files = filter(lambda file: any(file.endswith(x) for x in ('php', 'inc', 'module', 'install', 'tpl.php')), files)
    if filename == 'whyspace.testfile.php':
      print 'Refusing to Whyspacify any source code!'
      continue
    # Loop through the files
    for filename in files:
      fixFile(filename, root)

# Check if the input is a single file.
if os.path.isfile(rootDir):
  fixFile(rootDir, '')
