import logging
import pathlib

from util import readlines_strip

log = logging.getLogger(__name__)

def parse(path: pathlib.Path) -> dict:
	'''Given a path, find and parse a file: dom, the domain file. 
	This file is assumed to exist, an error will be thrown otherwise.	
	'''
	assert isinstance(path, pathlib.Path)
	assert path.is_dir() 
	
	dom_path = path / 'dom'
	log.info('reading domain from "%s"', dom_path)
	dom_lines = readlines_strip(dom_path)	
	# convert each line of 'dom' into a dictionary entry
	# where "a 1 2 3" -> {a: [1, 2, 3]} 
	return { i[0]: frozenset(i[1:]) for i in [line.split() for line in dom_lines] } 

