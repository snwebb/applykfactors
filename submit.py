#!/usr/bin/env python
import os, re, subprocess
import commands
import math, time
import sys
import yaml

NumberOfJobs= 1

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

#infile = open("run_2018.sh", 'r')
#cmds = infile.read().splitlines()
YamlDir = "/home/hep/snwebb/invisible/MJ2/CHIP/analysis/samples/2018/background/"

OutputDirBase =  "/home/hep/snwebb/invisible/applykfactors/" 

def main():
    print 
    print 'START'
    print 

    if subprocess.call(["voms-proxy-info",'--exists']) == 1:
        print "Voms proxy does not exist:"
        os.system("voms-proxy-init -voms cms -valid 96:00")
    else:
        print "Voms proxy exists"
    print

    ##### loop for creating and sending jobs #####
    for y,inv in enumerate(inlist):

        vectorid = "w"
        if (y==1):
            vectorid = "z"
        for v in inv:

            os.chdir(OutputDirBase)
            os.system("rm -rf " + v + "/tmp")
            os.system("mkdir -p " + v + "/tmp")
            os.system("mkdir -p " + v + "/root")

            with open(YamlDir + v + ".yml", 'r') as f:
                infile = yaml.load(f)
            for x,filename in enumerate(infile["datasets"][0]["files"]):

                ##### creates jobs #######
                os.chdir( OutputDirBase + v + "/tmp/" )
                with open('job_' + v + "_" + str(x)+'.sh', 'w') as fout:                  

                    fout.write("#!/bin/sh\n")
                    fout.write("echo\n")
                    fout.write("echo\n")
                    fout.write("ulimit -c 0\n")
                    fout.write("echo 'START---------------'\n")
                    fout.write("echo 'WORKDIR ' ${PWD}\n")

                    fout.write("trap \"echo SIGINT seen\"  SIGINT\n")
                    fout.write("trap \"echo SIGUSR1 seen\" SIGUSR1\n")
                    fout.write("trap \"echo SIGUSR2 seen\" SIGUSR2\n")
                    fout.write("trap \"echo SIGTERM seen\" SIGTERM\n")
                    fout.write("trap \"echo SIGXCPU seen\" SIGXCPU\n")

                    fout.write("cd /home/hep/snwebb/invisible/CMSSW_9_4_10/src\n")
                    fout.write("eval `scramv1 runtime -sh`\n")
                    fout.write("cd /home/hep/snwebb/invisible/applykfactors\n")
                    fout.write("python -u applykfactors.py " + vectorid + " " + YamlDir + v + ".yml " + filename + " " + OutputDirBase + v + "/root/" + v + "_" + str(x) + ".root")
                    fout.write("\necho 'STOP---------------'\n")
                    fout.write("echo\n")
                    fout.write("echo\n")

                os.system("chmod 755 job_" + v + "_" + str(x)+".sh")

                ###### sends bjobs ######
                os.system("qsub -cwd -q hep.q -l h_vmem=4G -l s_vmem=3.5G -l h_rt=2:0:0 -l s_rt=1:50:0 job_"+ v + "_" + str(x)+".sh")
                print "job nr " + str(x) + " submitted"


    print
    print "your jobs:"
    os.system("qstat")
    print
    print 'END'
    print
            

if __name__ == '__main__':
  main()
