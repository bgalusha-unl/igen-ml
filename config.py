import logging
import pathlib
import glob
import itertools
from typing import Iterable

from util import readlines_strip

log = logging.getLogger(__name__)

def parse(path: pathlib.Path) -> list:
	'''Given a path, find and parse all default config files.
	These files are of the pattern dom.default*  
	If no such files exist, an empty list is returned.
	'''
	assert isinstance(path, pathlib.Path)
	assert path.is_dir() 
	
	config_pattern = path / 'dom.default*'
	log.info('searching for glob pattern "%s"', config_pattern)
	matches = glob.glob(str(config_pattern))
	matches = [pathlib.Path(p) for p in matches]
	log.info('found %s matches: %s', len(matches), [m.name for m in matches])
	configs = []
	# convert lines of each dom.default file into a dictionary 
	# such that "a 1" -> {a: 1} 
	for config_path in matches:
		config_lines = readlines_strip(config_path)
		config = {k:v for k,v in [line.split() for line in config_lines]}
		configs.append(config)
	return configs

def iterate(dom: dict) -> Iterable[dict]:
	'''Given a dom, create an iterator that iterates over all
	combinations of the domain values. Output is in the form:
	{'a':'1', 'b':'2', 'c':'3'}
	'''
	return ConfigIterable(dom)

class ConfigIterable:
	def __init__(self, dom):
		self.keys = dom.keys()
		self.iter = itertools.product(*dom.values())
	def __iter__(self):
		return self
	def __next__(self):
		config = next(self.iter)
		return dict(zip(self.keys, config))
