"""
print duplicate MC samples by comparing DSIDs
"""

import os, sys
from argparse import ArgumentParser

#=============================================================================================================================================================================

def stripToDSID(foundSamples):
#return a list of samples with wildcard search for NTUP_PILEUP version
	returnSamples = []
	readSamples = []
	for sample in foundSamples:
		split  = sample.split(".")
		# get ami tag up to campaign (hard code mc16c for now)
		wildcard = split[1]
		if wildcard in readSamples:
			returnSamples += [wildcard]
		else:
			readSamples += [wildcard]
	return returnSamples

#=============================================================================================================================================================================

parser = ArgumentParser(description = 'Get list of NTUP_PILEUP files')
parser.add_argument('-i', '--inputfile', help = 'Input prw directory', required = True)
options = parser.parse_args() 

samplelist = open(options.inputfile)
missing = []
found = []
samplesToCheck = []

# Get list of samples from txt file
for line in samplelist:
	if line.startswith("mc1"):
		sample = line.strip("\n")
		samplesToCheck +=[sample]

# wildcard samples to search for
samplesWildcarded = stripToDSID(samplesToCheck)
for sample in samplesWildcarded:
	print sample
