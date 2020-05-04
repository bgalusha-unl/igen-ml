import logging
import pathlib

log = logging.getLogger(__name__)

def readlines_strip(path):
	'''Read all lines of a file, then perform these actions:
	1. Strip white space from each end of the line
	2. If the resulting lines are blank, remove them
	3. If the remaining lines begin with a comment marker '#', omit them
	'''
	assert isinstance(path, pathlib.Path)
	with open(path, 'r') as fil:
		# read lines from the file
		lines = [l.strip() for l in fil.readlines()]
		# remove blank lines
		lines = [l for l in lines if l]
		# remove lines that begin with a comment
		lines = [l for l in lines if not l.startswith('#')] 
	return lines

def exactly_descending(numbers):
	return exactly_ascending(numbers[::-1])

def exactly_ascending(numbers):
	n = sorted(numbers)
	for a,b in zip(n, n[1:]):
		if not b == a + 1:
			return False
	return True

def panic(err, code):
	log.critical('A FATAL ERROR OCCURRED: code %s: %s', code, err)
	exit()
