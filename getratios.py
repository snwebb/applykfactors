#!/usr/bin/env python
import ROOT
from ROOT import *
from array import *
import sys
import io
import signal

file_w = ROOT.TFile("merged/WJetsToLNu.root","READ")
file_z = ROOT.TFile("merged/DYJetsToLL.root","READ")


w_nom = file_w.Get("mjj")
w_factup = file_w.Get("mjj_Fact_Up")
w_factdown = file_w.Get("mjj_Fact_Down")
w_renormup = file_w.Get("mjj_Renorm_Up")
w_renormdown = file_w.Get("mjj_Renorm_Down")
w_pdfup = file_w.Get("mjj_PDF_Up")
w_pdfdown = file_w.Get("mjj_PDF_Down")

z_nom = file_z.Get("mjj")
z_factup = file_z.Get("mjj_Fact_Up")
z_factdozn = file_z.Get("mjj_Fact_Down")
z_renormup = file_z.Get("mjj_Renorm_Up")
z_renormdozn = file_z.Get("mjj_Renorm_Down")
z_pdfup = file_z.Get("mjj_PDF_Up")
z_pdfdozn = file_z.Get("mjj_PDF_Down")



file_out =  ROOT.TFile("merged/ratios.root","RECREATE")

r_nom = w_nom.Clone("RatioWZ_Nominal")
r_factup = w_factup.Clone("RatioWZ_Fact_Up")
r_factdown = w_factdown.Clone("RatioWZ_Fact_Down")
r_renormup = w_renormup.Clone("RatioWZ_Renorm_Up")
r_renormdown = w_renormdown.Clone("RatioWZ_Renorm_Down")
r_pdfup = w_pdfup.Clone("RatioWZ_Pdf_Up")
r_pdfdown = w_pdfdown.Clone("RatioWZ_Pdf_Down")

r_nom.Write()
r_factup.Write()
r_factdown.Write()
r_renormup.Write()
r_renormdown.Write()
r_pdfup.Write()
r_pdfdown.Write()


