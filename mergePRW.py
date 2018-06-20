"""

@brief merge PRW files with hadd
@note assumes that PRW files are stored in directory "PRW"
provide input file list that was used to download files from rucio

@author Sam Dysch (samuel.dysch@cern.ch)

"""

import os, sys
from argparse import ArgumentParser

#=============================================================================================================================================================================

def getDSID(sample):
	split  = sample.split(".")
	return split[1]

#=============================================================================================================================================================================

parser = ArgumentParser(description = 'merge PRW')
parser.add_argument('-i', '--inputfile', help = 'Input prw directory', required = True)
options = parser.parse_args() 

samplelist = open(options.inputfile)
samples = []

# Get list of samples from txt file
for line in samplelist:
	if line.startswith("mc1"):
		sample = line.strip("\n")
		samples +=[sample]

# merge
for sample in samples:
	DSID = getDSID(sample)
	output = "output/pileup_chan" + DSID + ".root"
	print "[INFO]: doing {}. Output file: {}".format(DSID, output)
	cmd = "hadd " + output + " PRW/" + sample + "/*.root"
	print cmd

	os.system("mkdir -p output")
	os.system(cmd)

print "All done :)"
