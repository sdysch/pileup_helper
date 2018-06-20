"""

@breif Input a list of DxAODS, use rucio to find NTUP_Pileup version and provide list of corresponding files to download/generate
@author Sam Dysch (samuel.dysch@cern.ch)

!!!MUST HAVE SETUP RUCIO!!!

Refs: https://twiki.cern.ch/twiki/bin/view/AtlasProtected/ExtendedPileupReweighting

@note searches for NTUP_PILEUP version of mc sample. Must match AMI tags up to and including r-tag


"""

import os, sys
from argparse import ArgumentParser

#=============================================================================================================================================================================

def stripToWildCard(foundSamples):
#return a list of samples with wildcard search for NTUP_PILEUP version
	returnSamples = []
	for sample in foundSamples:
		split  = sample.split(".")
		# get ami tag up to campaign (hard code mc16c for now)
		splitTags = split[5].split("_r9781_")
		amitag = splitTags[0] + "_r9781*"
		wildcard = split[0] + "." + split[1] + "." + split[2] + "*NTUP_PILEUP*" + amitag
		returnSamples += [wildcard]
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
samplesWildcarded = stripToWildCard(samplesToCheck)
for sample in samplesWildcarded:
	print sample
