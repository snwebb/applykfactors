#!/bin/python
import ROOT
from ROOT import *
from array import *
import sys
import io
import signal
import yaml

interruptLoop = False

def signal_handler(sig, frame):
    global interruptLoop
    interruptLoop = True

def make_hists(names,hists):    
    for name in names:
        hist = ROOT.TH1D( "mjj" + name , "", 100,0,1000)
        hists.append( hist )


def fill_hists(hists,weights,mjj,nominal_weight):    

    for hist, weight in zip(hists, weights):
        hist.Fill(mjj,weight*nominal_weight)

def save_hists(hists,outputname):    
    fout = ROOT.TFile(outputname,"RECREATE")
    for hist in hists:
        hist.Write()

def get_nominal_weight(event):
    weight = 1.

    weight *= event.VetoElectron_eventVetoW
    weight *= event.LooseMuon_eventVetoW
    weight *= event.puWeight
    #    weight *= event.VLooseSITTau_eventVetoW
    weight *= event.VLooseTau_eventVetoW
    weight *= event.MediumBJet_eventVetoW
#    weight *= event.xs_weight
    weight *= event.genWeight
#    weight *= event.trigger_weight_METMHT2018


    return weight


def get_gen_boson_jet(event):

    #find boson and leptons

    boson_found = False
    lep1 = ROOT.TLorentzVector()
    lep2 = ROOT.TLorentzVector()
    lep1_isnu = False
    lep2_isnu = False

    for part in range(len(event.GenPart_pdgId)):
        if ( (abs(event.GenPart_pdgId[part])>10 and abs(event.GenPart_pdgId[part]) < 17) and ( (event.GenPart_status[part] == 1 and (event.GenPart_statusFlags[part] & 0x1)>0) or ((event.GenPart_statusFlags[part] & 0x1)>0 and (event.GenPart_statusFlags[part] & 0x2)>0) ) ):
            if (event.GenPart_genPartIdxMother[part]>=0):
                mother = event.GenPart_genPartIdxMother[part]

                while True:

                    if (event.GenPart_pdgId[mother] == 23 or abs(event.GenPart_pdgId[mother]) == 24):
                        boson_found = True
                        break
                    else:
                        mother = event.GenPart_genPartIdxMother[mother];
                        if ( mother < 0  ):
                            break

            if (boson_found):
                boson_pt = event.GenPart_pt[mother]

            if (event.GenPart_pdgId[part]>0):
                lep1.SetPtEtaPhiM( event.GenPart_pt[part], event.GenPart_eta[part], event.GenPart_phi[part], event.GenPart_mass[part]  );
                if ( abs(event.GenPart_pdgId[part]) == 12 or abs(event.GenPart_pdgId[part]) == 14 or abs(event.GenPart_pdgId[part]) == 16):
                    lep1_isnu = True
            else:
                lep2.SetPtEtaPhiM( event.GenPart_pt[part], event.GenPart_eta[part], event.GenPart_phi[part], event.GenPart_mass[part]  );
                if ( abs(event.GenPart_pdgId[part]) == 12 or abs(event.GenPart_pdgId[part]) == 14 or abs(event.GenPart_pdgId[part]) == 16):
                    lep2_isnu = True


    if (not boson_found):
        boson_pt = (lep1+lep2).Pt()
        boson_found = True






    jets = []
    for pt,eta,phi,m in zip(event.GenJet_pt,event.GenJet_eta,event.GenJet_phi,event.GenJet_mass):
        jet = ROOT.TLorentzVector()
        jet.SetPtEtaPhiM(pt,eta,phi,m)
        if not lep1_isnu:
            if ( jet.DeltaR(lep1) < 0.4 ):
                continue
        if not lep2_isnu:
            if ( jet.DeltaR(lep2) < 0.4 ):
                continue

        jets.append(jet)
        if (len(jets) == 2):
            break

    if (len(jets) == 2): 
        mjj = (jets[0] + jets[1]).M()
    else:
        mjj = 0

    jet0 = ROOT.TLorentzVector()
    jet1 = ROOT.TLorentzVector()
    jet0.SetPtEtaPhiM(event.GenJet_pt[0],event.GenJet_eta[0],event.GenJet_phi[0],event.GenJet_mass[0])
    jet1.SetPtEtaPhiM(event.GenJet_pt[1],event.GenJet_eta[1],event.GenJet_phi[1],event.GenJet_mass[1])
    
    return boson_pt,mjj

def pass_selection(event):

    if ((event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 == 1 or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)
        and event.nLoosePhoton == 0
        #        and event.met_filters_2018_mc
        and event.MetNoLep_CleanJet_mindPhi > 0.5
        and event.MetNoLep_pt  >= 250
        and event.nCleanJet >= 2
        and event.CleanJet_pt[0] > 80
        and abs(event.CleanJet_eta[0]) < 5.0
        and event.CleanJet_pt[1] > 40
        and abs(event.CleanJet_eta[1]) < 5.0
        and event.CleanJet_eta[0]*event.CleanJet_eta[1] < 0
        and event.diCleanJet_M > 200
        and event.diCleanJet_dPhi < 1.5
        and abs(event.diCleanJet_dEta) > 1
    ):
        return True
    else:
        return False

def getKFactorWeight(hist,bospt):
    weight = hist.GetBinContent(hist.FindBin(bospt))
    return weight
    

def main(args):


    signal.signal(signal.SIGINT, signal_handler) 
    sampletype = args[1] 


    with open(args[2], 'r') as f:
        infile = yaml.load(f)

#    infile = open(args[2], 'r')



    chain = TChain("Events")
    for filename in infile["datasets"][0]["files"]:
        print(filename)
        chain.Add(filename)

    #Get the normalisation (scale by xs/sum of weights, taken from yaml file)
    norm = float(infile["datasets"][0]["xs"])/infile["datasets"][0]["nevents"]
    
    

    systs = ["", "_Renorm_Up", "_Renorm_Down", "_Fact_Up", "_Fact_Down", "_PDF_Up", "_PDF_Down"]
    hists = []
    make_hists(systs,hists)
    #    load k-factors file
    kfac_w = ROOT.TFile("kfactor_VBF_wjet.root","READ")
    kfac_z = ROOT.TFile("kfactor_VBF_zjet.root","READ")
    kfacfile = kfac_w
    if ( sampletype == "z" ):
        kfacfile = kfac_z
    
    kfac_200_500 = []
    kfac_500_1000 = [] 
    kfac_1000_1500 = []
    kfac_1500_5000 = []

    for syst in systs:
        kfac_200_500.append(kfacfile.Get("kfactors_shape%s/kfactor_vbf_mjj_200_500"%(syst)))
        kfac_500_1000.append(kfacfile.Get("kfactors_shape%s/kfactor_vbf_mjj_500_1000"%(syst)))
        kfac_1000_1500.append(kfacfile.Get("kfactors_shape%s/kfactor_vbf_mjj_1000_1500"%(syst)))
        kfac_1500_5000.append(kfacfile.Get("kfactors_shape%s/kfactor_vbf_mjj_1500_5000"%(syst)))

    #i = 0
    for entry,event in enumerate(chain):
        if ( entry%10000 == 0 ):
            print entry
        if ( pass_selection(event) ):
            bospt,mjj = get_gen_boson_jet(event)
            nomweight =  get_nominal_weight(event)
            nomweight*=norm

            #Get NLO weight and apply based on pt and mjj

            mjjhist = kfac_200_500
            if (mjj>500):
                mjjhist = kfac_500_1000
            if (mjj>1000):
                mjjhist = kfac_1000_1500
            if (mjj>1500):
                mjjhist = kfac_1500_5000
            weights = []            
            
            for i,syst in enumerate(systs):
                weights.append(getKFactorWeight(mjjhist[i],bospt))
            
            fill_hists(hists,weights,event.diCleanJet_M,nomweight)

        if (interruptLoop==True):
            break

    save_hists(hists,args[3])


main(sys.argv)
