#!/usr/bin/env python
import os, re, subprocess
import commands
import math, time
import sys

NumberOfJobs= 1

infile = open("run_2018.sh", 'r')
cmds = infile.read().splitlines()


#OutputDir =  "/vols/cms/snwebb/kFactor/" 

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
   for x,cmd in enumerate(cmds):

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

         fout.write("cd /home/hep/snwebb/invisible/CMSSW_9_4_10/src\n")
         fout.write("eval `scramv1 runtime -sh`\n")
         fout.write("cd /home/hep/snwebb/invisible/applykfactors\n")
         fout.write(cmd)
         fout.write("\necho 'STOP---------------'\n")
         fout.write("echo\n")
         fout.write("echo\n")

         os.system("chmod 755 job_"+str(x)+".sh")

         ###### sends bjobs ######
         #os.system("bsub -q "+queue+" -o logs job.sh")
      os.system("qsub -cwd -q hep.q -l h_vmem=4G -l s_vmem=3.5G -l h_rt=1:0:0 -l s_rt=0:50:0 job_"+str(x)+".sh")
      print "job nr " + str(x) + " submitted"


   print
   print "your jobs:"
   os.system("qstat")
   print
   print 'END'
   print


if __name__ == '__main__':
  main()
