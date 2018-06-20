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

# output dir
os.system("mkdir -p output")

# Get list of samples from txt file
for line in samplelist:
	if line.startswith("mc1") and "NTUP_PILEUP" in line:
		sample = line.strip("\n")
		samples +=[sample]

print "[INFO] found {} samples to merge".format(len(samples))

mergedfiles = 0

# merge
for sample in samples:
	sample = sample.split(":")[1] # remove mc16_13TeV: scope from rucio
	if not (os.path.isdir("PRW/" + sample)):
		print "[WARNING]: could not locate config files for {} -- skipping".format(sample)
		continue
	DSID = getDSID(sample)
	output = "output/pileup_chan" + DSID + ".root"
	print "[INFO]: doing {}. Output file: {}".format(DSID, output)
	cmd = "hadd -f " + output + " PRW/" + sample + "/*NTUP_PILEUP*.root*"
	print cmd

	os.system(cmd)
	mergedfiles += 1

if mergedfiles == 0:
	print "Merged no PRW files. Please check your inputs!"
else:
	print "Merged {} samples - all done :)".format(mergedfiles)
