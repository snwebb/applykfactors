#!/usr/bin/env python
import os, re, subprocess
import commands
import math, time
import sys

OutputDirBase =  "/home/hep/snwebb/invisible/applykfactors/" 

inw = [
    "WJetsToLNu_HT-70To100", 
    "WJetsToLNu_HT-100To200", 
    "WJetsToLNu_HT-200To400", 
    "WJetsToLNu_HT-400To600", 
    "WJetsToLNu_HT-600To800", 
    "WJetsToLNu_HT-800To1200", 
    "WJetsToLNu_HT-1200To2500",
    "WJetsToLNu_HT-2500ToInf", 
]

inz = [
    "DYJetsToLL_M-50_HT-70to100", 
    "DYJetsToLL_M-50_HT-100to200", 
    "DYJetsToLL_M-50_HT-200to400", 
    "DYJetsToLL_M-50_HT-400to600", 
    "DYJetsToLL_M-50_HT-600to800", 
    "DYJetsToLL_M-50_HT-800to1200",
    "DYJetsToLL_M-50_HT-1200to2500",
    "DYJetsToLL_M-50_HT-2500toInf", 
]


inlist = []
inlist.append(inw)
inlist.append(inz)

os.system("mkdir -p " + "merged")
os.chdir("merged")

for y,inv in enumerate(inlist):
    for v in inv:
        os.system("hadd -f " + v + ".root " + OutputDirBase + v + "/root/" + v  + "*.root")

#Final merge
os.system("hadd -f WJetsToLNu.root WJetsToLNu_HT*.root")
os.system("hadd -f DYJetsToLL.root DYJetsToLL_M-50_HT*.root")
