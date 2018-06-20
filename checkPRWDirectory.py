"""

Script to check whether samples in sample list are contained in PRW directory

adapted from original checkSamplesInPRWfile.py script by @author Eric Drechsler - eric.drechsler@cern.ch

@author Sam Dysch (samuel.dysch@cern.ch)

"""

import os, sys, glob
from argparse import ArgumentParser

#=============================================================================================================================================================================

def isDSID(dsid):
	try:
		int(dsid)
		return True
	except ValueError:
		return False

#=============================================================================================================================================================================

def stripToDSID(foundSamples):
	returnSamples = []
	for sample in foundSamples:
		splitDir  = sample.split(options.input_dir)
		splitDSID = splitDir[1].split("pileup_chan")
		if splitDSID[1].endswith(".root"):
			DSID = splitDSID[1]
			DSID = DSID[:-5]
			if not isDSID(DSID):
				raise NameError("Could not properly get DSID for {0}".format(DSID))
			else:
				returnSamples += [DSID]
	return returnSamples

#=============================================================================================================================================================================

parser = ArgumentParser(description = 'Check PRW directory')
parser.add_argument('-i', '--input-dir', help = 'Input prw directory', required = True)
parser.add_argument('-d', '--input-dsids', help = 'List of input DSIDs', nargs = '+', default=[])
parser.add_argument('-l', '--input-sample-list', help = 'Input sample list', required = True)
options = parser.parse_args() 

samplelist = open(options.input_sample_list)
missing = set()
found = set()
samplesToCheck = []

# get list of PU profiles in specified directory
foundSamples = glob.glob(os.path.join(options.input_dir, "pileup_chan*.root"))

if not foundSamples:
	print "Could not find any pileup files in directory {0} -- please check the path".format(options.input_dir)
	sys.exit()

# strip off everything but the DSID
samplesInDir = stripToDSID(foundSamples)

# Get list of samples from txt file
for line in samplelist:
	if line.startswith("mc1"):
		DSID = line.strip("\n")
		splitDSID = DSID.split(".")
		if isDSID(splitDSID[1]):
			samplesToCheck += [splitDSID[1]]
		else:
			raise NameError("Could not properly get DSID for {0}".format(splitDSID[1]))
    
# get DSIDs
for dsid in options.input_dsids:
	if not isDSID(dsid):
		raise NameError("Could not recognise input DSID '%s'"%(dsid))
	else:
		if dsid not in samplesToCheck:
			samplesToCheck.append(dsid)
  
# check whether sample is in PU directory
for dsid in samplesToCheck:
	if dsid not in samplesInDir: 
		missing.add(dsid)
	else:
		found.add(dsid)

# results
if len(missing) is 0:
	print "No missing DSIDS :)"
else:
	print "These DSID(s) are missing:" + " ".join(str(el) for el in missing)
