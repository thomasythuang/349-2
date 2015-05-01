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
		self.attrIndex, self.split = findSplit(data, self.attrs)

		if attributes[self.attrIndex] > 0:
			self.numeric = False
		else:
			self.numeric = True

class Leaf(Node):
	def setProb(self, prob):
		self.prob = prob

def findSplit(data, attrs):
	"""Find the most appropriate attribute to split on"""
	values = [[None] for n in range(attrs)]
	splits = [None]*attrs
	entropies = [0.0]*(attrs-1)
	for i in range(attrs):
		for point in data:
			values[i].append(point[i])
		splits[i] = median(values[i])

	for i in range(attrs-1):
		set1 = []
		set2 = []
		for point in data:
			if (point[i] > splits[i]):
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
	med = splits[index]

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
			#data[i] = -100.0
			data[i] = 1.0
		else:
			data[i] = float(row[i])

	return data

def median(lst):
	"""Calculate median value of a list"""
	even = (0 if len(lst) % 2 else 1) + 1
	half = (len(lst) - 1) / 2
	return sum(sorted(lst)[half:half + even]) / float(even)

def learn(node, attrTypes, maxHeight):
	"""Learn a decision tree"""
	if node.numeric:
		splitCount = 2
	else:
		splitCount = attrTypes[node.attrIndex]

	sets = [[] for n in range(splitCount)]
	for point in node.data:
		if node.numeric:
			if (point[node.attrIndex] > node.split):
				sets[0].append(point)
			else:
				sets[1].append(point)
		else:
			if node.attrIndex == 2:
				ind = int(point[node.attrIndex]) + 1
			elif node.attrIndex == 6 or node.attrIndex == 7:
				ind = int(point[node.attrIndex]) - 1
			else:
				ind = int(point[node.attrIndex])
			sets[ind].append(point)
			if len(sets[ind]) < 5:
				largeEnough = False

	if node.height < maxHeight:
		#print node.height
		for i in range(splitCount):
			if len(sets[i]) < 10:
				makeLeaf(node)
				return
			node.branches.append(Node(sets[i], node.height+1))
		for branch in node.branches:
			learn(branch, attrTypes, maxHeight)
	else:
		#print "Reached max height", maxHeight
		#for i in range(splitCount):
		makeLeaf(node)
		#node.branches[1].setProb(1.0-p)

def makeLeaf(node):
	node.branches.append(Leaf(node.data, node.height+1))
	p = getRatio(node.data, node.attrs-1, 0.0)
	node.branches[len(node.branches)-1].setProb(p)

def printTree(node):
	if len(node.branches) > 0:
		print "Height", node.height, ", splits at", node.attrIndex
		print  len(node.branches), "branches"
		for branch in node.branches:
			printTree(branch)
	else:
		print "Leaf"

def gregsPrintTree(node):
	spacer = ""
	for n in range(node.height):
		spacer += "-"
	if len(node.branches) > 0:
		if node.numeric:
			medianCondition = "split at " + str(node.split)
		else:
			medianCondition = ""
		print spacer, node.attrIndex, medianCondition
		for branch in node.branches:
			gregsPrintTree(branch)
	else:
		print spacer, node.prob

def followTree(node, example):
	"""For an example, follow the decision tree and predict the outcome"""
	if len(node.branches) > 0:
		if len(node.branches) > 1:
			if node.numeric:
				val = example[node.attrIndex]
				if val > node.split:
					return followTree(node.branches[0], example)
				else:
					return followTree(node.branches[1], example)
			else:
				if node.attrIndex == 2:
					val = int(example[node.attrIndex]) + 1
				elif node.attrIndex == 6 or node.attrIndex == 7:
					val = int(example[node.attrIndex]) - 1
				else:
					val = int(example[node.attrIndex])
				return followTree(node.branches[val], example)
		else:
			return followTree(node.branches[0], example)
	else:
		rand = random.random()
		if rand <= node.prob:
			return 1.0
		else:
			return 0.0

def makeTree(trainPath='btrain.csv', maxHeight=7):
	"""Generates a decision tree based on the training set"""

	csv_train = csv.reader(open(trainPath))
	csv_train.next()
	dataPoints = []
	print "Learning tree..."
	for row in csv_train:
		dataPoints.append(convertCSV(row))

	root = Node(dataPoints, 0)
	learn(root, attributes, maxHeight)
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
	learn(root, attributes, 8)
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
	learn(root, attributes, 7)
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

# List of attribute types-
# If the value is 0, the attribute is numeric
# If the value is >0, the attribute is nominal
attributes = [0, 0, 3, 0, 0, 0, 5, 5, 0, 0, 2, 0, 0, 2]