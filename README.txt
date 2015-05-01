=====     EECS 349 Problem Set 2     =====
===== Thomas Huang and Gregory Leung =====

Hello! This is our submission for problem set #2.

To run the code, simply navigate to the directory containing 'ps2.py',
and type 'Python' in the command line to enter the Python shell

In the shell, load the file with the command 'execfile("ps2.py")', and then you have access to all of the decision tree functions:

	1) makeTree(trainPath, maxHeight) 
	Learns a decision tree of maxHeight from the .csv training set specified by 'trainPath' (default path is 'btrain.csv'). Returns the decision tree.

	2) validate(trainPath, validatePath)
	Learns a decision tree from 'trainPath', and then tests its performance using the .csv validation set specified by 'validatePath'.
	Default paths are 'btrain.csv' and 'bvalidate.csv'

	3) predict(trainPath, testPath, outPath)
	Learns a decision tree from 'trainPath', and then reads in data from the .csv testing set specified by 'testPath'. It generates predictions for that data and then saves the modified data as a .csv file in 'outPath'. 
	Default paths are 'btrain.csv', 'btest.csv', and 'result.csv'