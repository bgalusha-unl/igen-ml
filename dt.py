import logging
import copy
from collections import OrderedDict

log = logging.getLogger(__name__)

class DecisionTree:
	def __init__(self):
		self.var = None
		self.val = None
		self.result = None
		self.parent = None
		self.children = []
	
	def __str__(self):
		return 'var: {}, val: {}'.format(self.var, self.val)

	def add(self, var, val, result=None):
		tree = DecisionTree()
		tree.var = var
		tree.val = val
		tree.result = result
		tree.parent = self
		self.children.append(tree)
		return tree

	def is_leaf(self):
		return not self.children

	def leaves(self):
		leaves = []
		if self.children:
			for c in self.children:
				leaves += c.leaves()
		else:
			return [self]
		return leaves

def summary(tree, dom):
	assert tree.children
	var = tree.children[0].var
	vdom = set(dom[var])
	reached = set([c.val for c in tree.children])
	not_reached = vdom - reached 
	print(reached, not_reached)

def pretty_print(tree, name='*'):
	'''Print a decision tree, treating the tree as a root.
	'''
	print(name)
	if tree.children:
		for child in tree.children[:-1]:
			print(pretty_print_helper(child))
		print(pretty_print_helper(tree.children[-1], last=True))
	
def pretty_print_helper(tree, gaps=[], masks=[], last=False):
	'''Recursively print a decision tree.
	'''
	output = ''
	for gap, mask in zip(gaps, masks):
		output += (' ' if mask else '│') + (' ' * gap)
	output += '└' if last else '├'
	output += '[{0}:{1}]'.format(tree.var, tree.val) 
	if tree.children:
		output += '┐'
		for child in tree.children[:-1]:
			output += '\n'
			output += pretty_print_helper(child, 
				gaps + [len(str(tree.val)) + 4], 
				masks + [last], 
				False)
		output += '\n'
		output += pretty_print_helper(tree.children[-1], 
			gaps + [len(str(tree.val)) + 4], 
			masks + [last], 
			True)
	else:
		output += '─(T)' if tree.result else '-(F)'
	return output

def update_tree(tree, config, result):
	'''Recursively update a tree given a config.
	Note: config is destructively updated on each call.
	'''
	if not tree.children:
		var, val = config.popitem()
	else:
		var = tree.children[0].var
		val = config[var]
		del config[var]
	found = [c for c in tree.children if c.val == val]
	child = found[0] if found else tree.add(var, val)
	if config:
		update_tree(child, config, result)	
	else:
		child.result = result

def init_tree(tree):
	if not tree.children:
		tree.result = False
	else:
		for c in tree.children:
			init_tree(c)

def update_forest(forest: OrderedDict, config: dict, locations: set):
	'''given a forest, a test config, and a list of output locations,
	update the forest to reflect reached/unreached locations for this config.
	'''
	# if a new location is found, create a DecisionTree for it
	for loc in locations:
		if loc not in forest:
			if forest:
				copy_loc = next(iter(forest))
				tree = copy.deepcopy(forest[copy_loc])
				init_tree(tree)
				log.info('adding new tree to the forest: %s (copying %s)', loc, copy_loc)
				forest[loc] = tree
			else:
				log.info('adding new tree to the forest: %s', loc)
				forest[loc] = DecisionTree()

	for loc, tree in forest.items():
		# to produce trees of consistent structure, convert config to an OrderedDict
		log.debug('updating forest with config %s and locations %s', config, locations)
		ordered_config = OrderedDict(sorted(config.items(), reverse=True))
		result = loc in locations
		update_tree(forest[loc], ordered_config, result)

