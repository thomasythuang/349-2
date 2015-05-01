import csv, math, random

"""

	EECS 349 Problem Set 2- Thomas Huang & Gregory Leung

"""

class Node:
	"""Class for a decision tree node"""

	def __init__(self, data, height):
		"""Node constructor"""
		self.data = data
		self.height = height
		self.branches = []
		self.attrs = len(data[0])

		# Calculate the entropy of this Node
		self.entropy = getEntropy(self.data, self.attrs-1, 0.0)

		# Calculate the best attribute to split on, and what value to split
		self.attrIndex, self.median = findSplit(data, self.attrs)


class Leaf(Node):
	def setProb(self, prob):
		self.prob = prob

def findSplit(data, attrs):
	"""Find the most appropriate attribute to split on"""
	values = [[None] for n in range(attrs)]
	medians = [None]*attrs
	entropies = [0.0]*(attrs-1)
	for i in range(attrs):
		for point in data:
			values[i].append(point[i])
		medians[i] = median(values[i])

	for i in range(attrs-1):
		set1 = []
		set2 = []
		for point in data:
			if (point[i] > medians[i]):
				set1.append(point)
			else:
				set2.append(point)

		# For each attribute, calculate the weighted sum of its splits' entropies
		entropies[i] += getEntropy(set1, attrs-1, 0.0) * len(set1)
		entropies[i] += getEntropy(set2, attrs-1, 0.0) * len(set2)
		entropies[i] /= len(data)

		# If entropy = 0, that attr has already been split on, so ignore it
		if entropies[i] == 0.0:
			entropies[i] = 10.0

	index = entropies.index(min(entropies))
	med = medians[index]

	return index, med

def getEntropy(data, attrIndex, splitNum):
	"""Calculate the entropy of a node"""

	if len(data) == 0:
		return 1.0

	total = 0
	succ = 0
	for pt in data:
		if (pt[attrIndex] > -100):
			total = total + 1
			if (pt[attrIndex] > splitNum):
				succ = succ + 1
	p = float(succ)/float(total)
	q = float(total - succ)/float(total)

	if (p == 0.0) or (q == 0.0):
		return 0.0

	entropy = -(p * math.log(p, 2) + q * math.log(q, 2))
	return entropy

def getRatio(data, attrIndex, splitNum):
	"""For a leaf, get the ratio of wins to losses for the remaining
	data. This will become the probability property for the leaf"""
	if len(data) == 0:
		return 0.0

	total = 0
	succ = 0
	for pt in data:
		if (pt[attrIndex] > -100):
			total = total + 1
			if (pt[attrIndex] > splitNum):
				succ = succ + 1
	p = float(succ)/float(total)
	#q = float(total - succ)/float(total)

	return p

def convertCSV(row):
	"""Convert the CSV strings to floats"""
	data = [None]*len(row)
	for i in range(len(row)):
		if (row[i] == '?'):
			data[i] = -100.0
		else:
			data[i] = float(row[i])

	return data

def median(lst):
	"""Calculate median value of a list"""
	even = (0 if len(lst) % 2 else 1) + 1
	half = (len(lst) - 1) / 2
	return sum(sorted(lst)[half:half + even]) / float(even)

def learn(node, maxHeight):
	"""Learn a decision tree"""
	set1 = []
	set2 = []
	for point in node.data:
		if (point[node.attrIndex] > node.median):
			set1.append(point)
		else:
			set2.append(point)

	if node.height < maxHeight:
		#print node.height
		node.branches.append(Node(set1, node.height+1))
		node.branches.append(Node(set2, node.height+1))
		for branch in node.branches:
			learn(branch, maxHeight)
	else:
		#print "Reached max height", maxHeight
		node.branches.append(Leaf(set1, node.height+1))
		node.branches.append(Leaf(set2, node.height+1))
		p = getRatio(node.data, node.attrs-1, 0.0)
		node.branches[0].setProb(p)
		node.branches[1].setProb(1.0-p)

def followTree(node, example):
	"""For an example, follow the decision tree and predict the outcome"""
	if len(node.branches) > 0:
		val = example[node.attrIndex]
		if val > node.median:
			return followTree(node.branches[0], example)
		else:
			return followTree(node.branches[1], example)
	else:
		rand = random.random()
		if rand <= node.prob:
			return 1.0
		else:
			return 0.0

def makeTree(trainPath='btrain.csv', maxHeight=6):
	"""Generates a decision tree based on the training set"""

	csv_train = csv.reader(open(trainPath))
	csv_train.next()
	dataPoints = []
	print "Learning tree..."
	for row in csv_train:
		dataPoints.append(convertCSV(row))

	root = Node(dataPoints, 0)
	learn(root, maxHeight)
	print "Done!"
	return root

def validate(trainPath='btrain.csv', validatePath='bvalidate.csv'):
	"""Learns a model from the training set and then reports the
	model's performance using the validation set"""
	csv_train = csv.reader(open(trainPath))
	csv_train.next()
	print "Learning decision tree..."
	dataPoints = []
	for row in csv_train:
		dataPoints.append(convertCSV(row))
	root = Node(dataPoints, 0)
	learn(root, 6)
	print "Decision tree learned!"

	csv_validate = csv.reader(open(validatePath))
	csv_validate.next()
	print "Measuring performance with validation set..."
	correct = 0
	incorrect = 0
	for row in csv_validate:
		example = convertCSV(row)
		predicted_result = followTree(root, example)
		if predicted_result == example[len(example)-1]:
			correct += 1
		else:
			incorrect += 1
	print "Done!"
	print "Correct:", correct
	print "Incorrect:", incorrect
	print "Accuracy:", 100*float(correct)/float(correct+incorrect), "%"

def predict(trainPath='btrain.csv', testPath='btrain.csv', outPath='result.csv'):
	"""Generates predictions for a set and writes the predictions 
	to csv format"""
	csv_train = csv.reader(open(trainPath))
	csv_train.next()
	print "Learning decision tree..."
	dataPoints = []
	for row in csv_train:
		dataPoints.append(convertCSV(row))
	root = Node(dataPoints, 0)
	learn(root, 6)
	print "Decision tree learned!"

	csv_test = csv.reader(open(testPath))
	csv_test.next()
	print "Predicting results..."
	output = []
	for row in csv_test:
		output.append(convertCSV(row))
	for point in output:
		point[len(point)-1] = followTree(root, point)
	writer = csv.writer(open(outPath, 'w'))
	writer.writerows(output)
	print "Done!"