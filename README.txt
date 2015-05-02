=====     EECS 349 Problem Set 2     =====
===== Thomas Huang and Gregory Leung =====

Hello! This is our submission for problem set #2.

To run the code, simply navigate to the directory containing 'ps2.py',
and type 'Python' in the command line to enter the Python shell

In the shell, load the file with the command 'execfile("ps2.py")', and then you have access to the key decision tree functions. Every one of functions' parameters are optional, so they can all be called without parameters. 

	1) makeTree(pruning[bool], maxHeight[int], trainPath[string]) 
	Learns a decision tree of maxHeight from the .csv training set specified by 'trainPath' (default path is 'btrain.csv'). If pruning is True, the decision tree will be pruned. Returns the decision tree.
	Examples: 
		tree = makeTree()
		unpruned = makeTree(False, 8)
		pruned = makeTree(True, 10, 'btrain50.csv')

	2) validate(pruning, maxHeight, trainPath, validatePath)
	Learns a decision tree from 'trainPath', and then tests its performance using the .csv validation set specified by 'validatePath'.
	The program will then print out the accuracy for the tree
	Default paths are 'btrain.csv' and 'bvalidate.csv'
	Examples:
		validate()
		validate(True, 12)

	3) predict(pruning, maxHeight, trainPath, testPath, outPath)
	Learns a decision tree from 'trainPath', and then reads in data from the .csv testing set specified by 'testPath'. It generates predictions for that data and then saves the modified data as a .csv file in 'outPath'. 
	Default paths are 'btrain.csv', 'btest.csv', and 'result.csv'
	Examples:
		predict()
		predict(True, 12, 'btrain.csv', 'btest.csv', 'result2.csv')