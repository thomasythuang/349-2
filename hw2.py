import csv
import math

class DataNode:
	"""class for the dataset"""

	def __init__(self, dataset):
		"""dataset constructor"""

		self.dataPoints = dataset

		self.size = len(self.dataPoints)
		self.attrCount = len(self.dataPoints[0].data)
		self.vals = [[None] for n in range(self.attrCount)]
		self.medians = [None]*self.attrCount
		for i in range(self.attrCount):
			for point in self.dataPoints:
				self.vals[i].append(point.data[i])
			self.medians[i] = median(self.vals[i])

		self.entropy = self.getEntropy(self.attrCount-1, 0)

	def split(self, attrIndex, splitNum):
		self.children = []
		set1 = []
		set2 = []

		for pt in self.dataPoints:
			if (pt.data[attrIndex] >= splitNum):
				set1.append(pt)
			else:
				set2.append(pt)
		"""
		print "Num:", attrIndex
		print "Split:", splitNum
		print len(set1)
		print len(set2)
		"""

		self.children.append(DataNode(set1))
		self.children.append(DataNode(set2))

	def getEntropy(self, attrIndex, splitNum):
		total = 0
		succ = 0

		for pt in self.dataPoints:
			if (pt.data[attrIndex] > -100):
				total = total + 1
				if (pt.data[attrIndex] > splitNum):
					succ = succ + 1
		p = float(succ)/float(total)
		q = float(total - succ)/float(total)
		
		if (p == 0.0) or (q == 0.0):
			return 0.0

		entropy = -(p * math.log(p, 2) + q * math.log(q, 2))
		return entropy

	def test(self):
		for n in range(2):
			self.dataPoints[n].print_data()

class Datapoint:
	"""class for datapoints"""

	def __init__(self, data):
		"""datapoint constructor"""
		self.data = [None]*len(data)
		for i in range(len(data)):
			if (data[i] == '?'):
				self.data[i] = -100.0
			else:
				self.data[i] = float(data[i])

	def print_data(self):
		for i in self.data:
			print i

def median(lst):
	even = (0 if len(lst) % 2 else 1) + 1
	half = (len(lst) - 1) / 2
	return sum(sorted(lst)[half:half + even]) / float(even)

def test():
	path = 'btrain.csv'

	csv_f = csv.reader(open(path))
	csv_f.next()
	dataPoints = []

	for row in csv_f:
		dataPoints.append(Datapoint(row))

	nn = DataNode(dataPoints)
	entropies = [0.0]*nn.attrCount
	for i in range(nn.attrCount):
		nn.split(i, nn.medians[i])
		entropies[i] += (nn.children[0].entropy * nn.children[0].size)
		entropies[i] += (nn.children[1].entropy * nn.children[1].size)
		entropies[i] /= nn.size
		print entropies[i]
	print nn.entropy
