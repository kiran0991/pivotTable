#!/usr/bin/python3

import argparse
import sys
import pprint
import statistics

def summarise(data_matrix,mathOperation,tsvout,columns):
	''' Perform mathematical operation on list of alues '''
	numList=[]
	mathVal = None
	for k in data_matrix:
		tsvout.write(k+"\t")
		for i,sub_key in enumerate(data_matrix[k]):
			L = data_matrix[k][sub_key]
			##DEBUG
			#print(k,sub_key,data_matrix[k][sub_key])
			for e in  L:
				if e.strip() != '':
					numList.append(float(e))
			if numList == []:
				mathVal='NA'
			else:
				if mathOperation == 'median':
					mathVal = statistics.median(numList)
				elif mathOperation == 'mean':
					mathVal = statistics.mean(numList)
				elif mathOperation == 'mode':
					mathVal = statistics.mean(numList)
				elif mathOperation == 'sum':
					mathVal = sum(numList)
			if columns[i+1] == sub_key:
				tsvout.write(str(mathVal)+"\t")
			data_matrix[k][sub_key]=mathVal
			numList=None
			numList=[]	
		tsvout.write("\n")
	##DEBUG
	#pprint.pprint(data_matrix,tsvout,indent=4)


def main(inputfile,outputfile,summarisedBy):
	''' Parse input data file '''
	data_matrix=dict()
	columns = []
	tsvout = open(outputfile,"w")
	if inputfile.endswith(".txt"):
		tsvin = open(inputfile,'r')
	else:
		LOGGER.error("Input file %s expected to ends with .txt" % inputfile )
		sys.exit(1)
	for line in tsvin:
		line=line.rstrip("\n")
		if line.startswith("#"):
			tsvout.writelines(line+"\n")
			columns = line.split("\t")
		else:
			values=line.split("\t")
			_id = values[0]
			for index,val in enumerate(values):
				#DEBUG
				#print(index,columns[index],val)
				if index > 0:
					if _id in data_matrix.keys():
						if columns[index] in data_matrix[_id]:
							#'GSM1124869': ['5.83', '3.37', '', '']
							data_matrix[_id][columns[index]].append(val)						
						else:
							#{'1': {'GSM678382_B99': ['7.098182']}
							data_matrix[_id].update({(columns[index]):[val]})	
					else:
						#{'1': {'GSM678382_B99': ['7.098182']}
						data_matrix.update({_id:{(columns[index]):[val]}})


	#pprint.pprint(data_matrix,tsvout,indent=4)
	#print(data_matrix)
	summarise(data_matrix,summarisedBy,tsvout,columns)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Remove redundancy from given input tsv')
	parser.add_argument('-i','--inputfile',help='input tsv text file')
	parser.add_argument('-o','--outputfile',help='output tsv text file')
	parser.add_argument('-s','--summarisedBy',help='summarised values by sum , mean, median, mode')
	args = parser.parse_args()
	if args.inputfile == None:
		print("Please specify arguments")
		parser.print_usage()
		sys.exit(1)
	elif args.outputfile == None:
		print("Please specify arguments")
		parser.print_usage()
		sys.exit(1)
	elif args.summarisedBy == None:
		print("Please specify arguments")
		parser.print_usage()
		sys.exit(1)

	main(args.inputfile,args.outputfile,args.summarisedBy)