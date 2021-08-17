#!/usr/bin/env python
import os, re, subprocess
import math, time
import sys
commandlist = [

"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-70to100.yaml 2017_DYJetsToLL_M-50_HT-70to100.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-100to200.yaml 2017_DYJetsToLL_M-50_HT-100to200.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-200to400.yaml 2017_DYJetsToLL_M-50_HT-200to400.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-400to600.yaml 2017_DYJetsToLL_M-50_HT-400to600.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-600to800.yaml 2017_DYJetsToLL_M-50_HT-600to800.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-800to1200.yaml 2017_DYJetsToLL_M-50_HT-800to1200.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-1200to2500.yaml 2017_DYJetsToLL_M-50_HT-1200to2500.root",
"python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-2500toInf.yaml 2017_DYJetsToLL_M-50_HT-2500toInf.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-70To100.yaml 2017_WJetsToLNu_HT-70to100.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-100To200.yaml 2017_WJetsToLNu_HT-100to200.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-200To400.yaml 2017_WJetsToLNu_HT-200to400.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-400To600.yaml 2017_WJetsToLNu_HT-400to600.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-600To800.yaml 2017_WJetsToLNu_HT-600to800.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-800To1200.yaml 2017_WJetsToLNu_HT-800to1200.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-1200To2500.yaml 2017_WJetsToLNu_HT-1200to2500.root",
"python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-2500ToInf.yaml 2017_WJetsToLNu_HT-2500toInf.root",

]

OutputDir = '/home/hep/snwebb/invisible/applykfactors/outputs/'
#NumberOfJobs = 1000
def main():
   print ()
   print ('START')
   print ()

   os.system("mkdir -p " + OutputDir + "/tmp")
   os.chdir(OutputDir + "/tmp/")

   ##### loop for creating and sending jobs #####
   for x,command in enumerate(commandlist):
   ##### creates directory and file list for job #######

      ##### creates jobs #######
      with open('job_'+str(x)+'.sh', 'w') as fout:                  

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

         fout.write("cd /home/hep/snwebb/invisible/applykfactors/\n")
         fout.write( command + "\n")

         fout.write("echo 'STOP---------------'\n")
         fout.write("echo\n")
         fout.write("echo\n")

      os.system("chmod 755 job_"+str(x)+".sh")

      ###### sends bjobs ######
      #os.system("bsub -q "+queue+" -o logs job.sh")
      #os.system("qsub -cwd -q hep.q -l h_vmem=12G -l s_vmem=11.8G -l h_rt=2:0:0 -l s_rt=1:59:0 job_"+str(x)+".sh")
      os.system("qsub -cwd -q hep.q -l h_vmem=8G -l s_vmem=7.8G -l h_rt=8:0:0 -l s_rt=7:59:0 job_"+str(x)+".sh")
      print ("job nr " + str(x) + " submitted")

   print ()
   print ("your jobs:")
   os.system("qstat")
   print ()
   print ('END')
   print ()
 

if __name__ == '__main__':
  main()
