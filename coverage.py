import logging
import pathlib
import subprocess as sp

log = logging.getLogger(__name__)

def run(path, config):
	'''Given a path, find and execute a file: run, with the given config
	This file is assumed to exist, an error will be thrown otherwise.
	Return the result of execution.
	'''
	assert isinstance(path, pathlib.Path)
	assert path.is_dir()
	
	# build the argument string
	args = ', '.join(['{} {}'.format(k,v) for k,v in config.items()])
	
	# build the command string
	run_path = path / 'run'
	run_cmd = '{} "{}"'.format(run_path, args)
	log.debug('running %s', run_cmd)
	
	# run the command and return its output
	proc = sp.Popen(run_cmd, shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
	try:
		out, err = proc.communicate(None)
	except TimeoutExpired:
		proc.kill()
		out, err = proc.communicate(None)
	
	# clean up the output
	code = proc.returncode
	out, err = out.decode('utf-8'), err.decode('utf-8')
	out, err = out.strip(), err.strip()
	log.debug('result: code %s, out: "%s", err: "%s"', code, out, err)
	return out, err, code

def parse(output):
	return [x.strip() for x in output.split(',')]
