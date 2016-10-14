#!/usr/bin/env python

from ROOT import *
import os,sys


import argparse
parser =  argparse.ArgumentParser(description='Limit Tree maker')
parser.add_argument('-x', nargs='+', choices=['res', 'nonres'], required=True, default=None,
                    help = "Chose what samlples to create the trees from.")

opt = parser.parse_args()


if 'nonres' in opt.x:
  nodes = [[2, 50000]]
  #nodes = [ ["box", 49600], ["SM", 50000], [2, 50000], [3, 47600], [4, 50000], [5, 50000], [6, 50000],
  #          [7, 49800], [8, 50000], [9, 50000], [10, 50000], [11, 50000], [12, 50000], [13, 50000] ]
  
  Signals = "root://eoscms//eos/cms/store/user/rateixei/HHbbgg/FlatTrees/ICHEP_Regressed4b/output_GluGluToHHTo2B2G_node_THENODE_13TeV-madgraph.root"
  Data = "root://eoscms//eos/cms/store/user/rateixei/HHbbgg/FlatTrees/ICHEP_Regressed4b/DoubleEG.root"

  dirPrefix = "NonResAnalysis_ICHEP"

  postFix = " --MX --btagWP 0.8 "

  SFs = " --bVariation 0 --phoVariation 0"

  directory = dirPrefix
  os.system( "mkdir " + directory+"_LowMass" )
  os.system( "mkdir " + directory+"_HighMass" )


  for MM in nodes:
    i = MM[0]
    sigScale = 2.7/float(MM[1])
    print "DOING LowMassCat Signal, node ", i
    command = "pyLimitTreeMaker.py -f " + Signals.replace("THENODE", str(i)) + " -o " + directory+"_LowMass" + " --min 0 --max 350 --scale " + str(sigScale) + postFix + SFs
    print command
    os.system(command)
    #	continue
    print "DOING HighMassCat Signal, node ", i
    command = "pyLimitTreeMaker.py -f " + Signals.replace("THENODE", str(i)) + " -o " + directory+"_HighMass" + " --min 350 --max 35000 --scale " + str(sigScale) + postFix + SFs
    print command
    os.system(command)
    
  '''
  print "DOING LowMassCat Data"
  command = "pyLimitTreeMaker.py -f " + Data + " -o " +   directory+"_LowMass" + " --min 0 --max 350 --scale 1." + postFix
  os.system(command)
  print "DOING HighMassCat Data"
  command = "pyLimitTreeMaker.py -f " + Data + " -o " +   directory+"_HighMass" + " --min 350 --max 35000 --scale 1." + postFix
  os.system(command)
  '''
    
else:
  print 'These options are not covered yet...', opt.x
  sys.exit(1)
  