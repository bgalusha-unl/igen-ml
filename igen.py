#!/usr/bin/env python3

import argparse
import logging
import pathlib
import sys
import random
from collections import OrderedDict

import domain
import config
import coverage
import dt
from util import panic 

log = logging.getLogger("igen")
# note: refrain from using logging prior to configure_log() being called

def run_argparse():
	parser = argparse.ArgumentParser('igen')
	aa = parser.add_argument
	aa('dir', help='a directory containing the domain and run script')
	aa('--log', '--log-level', type=int, choices=range(5), default=1,
		help='log level: 0=DEBUG, 1=INFO, 2=WARNING, 3=ERROR, 4=CRITICAL')
	aa('--iter', type=int, default=100,
		help='number of training iterations, ignored if --all is passed')
	aa('--all', action='store_true', help='use all possible configs')
	aa('--seed', type=float, default=random.random(), help='a seed for the randomizer')
	return parser.parse_args()
	
def configure_log(level):
	# convert 0-4 to 10-50 as per the logging levels table:
	# https://docs.python.org/3/library/logging.html#logging-levels
	level_table = (level + 1) * 10  
	logging.basicConfig(level=level_table, stream=sys.stdout, format='%(name)s:%(levelname)s:%(message)s')

def do_all(dom, dir_path):
	forest = OrderedDict()
	for conf in config.iterate(dom):
		out, err, code = coverage.run(dir_path, conf)
		if code != 0:
			panic(err, code)
		locations = coverage.parse(out)
		dt.update_forest(forest, conf, locations) 
	for location, tree in sorted(forest.items()):
		dt

def do_iter(dom, dir_path, iter_max):
	forest = OrderedDict()
	iter_i = 0
	for conf in config.iterate(dom):
		out, err, code = coverage.run(dir_path, conf)
		if code != 0:
			panic(err, code)
		locations = coverage.parse(out)
		dt.update_forest(forest, conf, locations) 
		iter_i += 1
		if iter_i >= iter_max:
			break
	for location, tree in sorted(forest.items()):
		dt.pretty_print(tree, location)

def main():
	args = run_argparse()
	configure_log(args.log)
	random.seed(args.seed)

	dir_path = pathlib.Path(args.dir) 
	dom = domain.parse(dir_path)
	default_confs = config.parse(dir_path)

	if args.all:
		do_all(dom, dir_path)
	else:
		do_iter(dom, dir_path, args.iter)

if __name__ == '__main__':
	main()
