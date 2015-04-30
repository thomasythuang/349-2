import csv, math

"""

---- THIS IS THE ACTUAL FILE WE'RE WORKING ON NOW ----

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
	def test():
		print "yo"

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

	index = entropies.index(min(entropies))
	med = medians[index]

	return index, med

def getEntropy(data, attrIndex, splitNum):
	"""Calculate the entropy of a node"""
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

def convertCSV(row):
	"""Convert the CSV strings to floats"""
	data = [None]*len(row)
	for i in range(len(row)):
		if (row[i] == '?'):
			data[i] = -100.0
		else:
			data[i] = float(row[i])

	return data

def learn(data, default):
	print data

def make():
	path = 'btrain.csv'

	csv_f = csv.reader(open(path))
	csv_f.next()
	dataPoints = []

	for row in csv_f:
		dataPoints.append(convertCSV(row))

	return Node(dataPoints, 0)