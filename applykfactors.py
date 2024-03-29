#!/bin/python
import ROOT
from ROOT import *
from array import *
import sys
import io
import signal
import yaml
from array import array
import time

interruptLoop = False

def signal_handler(sig, frame):
    global interruptLoop
    interruptLoop = True

def make_hists(names,hists):  

    bins = array( 'f', [ 200, 400, 600, 900, 1200, 1500, 2000, 2750, 3500, 5000 ] )
    for name in names:
        hist = ROOT.TH1D( "mjj" + name , "", 9, bins)
        hists.append( hist )


def fill_hists(hists,weights,mjj,nominal_weight):    

    for hist, weight in zip(hists, weights):
        hist.Fill(mjj,weight*nominal_weight)

def save_hists(hists,outputname):    
    fout = ROOT.TFile(outputname,"RECREATE")
    for hist in hists:
        hist.Write()

def get_nominal_weight(event):
    weight = event.xs_weight

    weight *= event.VetoElectron_eventVetoW
    weight *= event.LooseMuon_eventVetoW
    weight *= event.puWeight
    #weight *= event.VLooseSITTau_eventVetoW
    weight *= event.VLooseTau_eventVetoW

    weight *= event.trigger_weight_METMHT2017 #2017
    weight *= event.L1PreFiringWeight_Nom #2017

    weight *= event.fnlo_SF_EWK_corr*event.fnlo_SF_QCD_corr_EWK_proc

#    weight *= event.MediumBJet_eventVetoW
#    weight *= event.xs_weight
#    weight *= event.genWeight
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

def get_gen_boson_jet_AM(event):
    return event.Gen_boson_pt, event.Gen_Mjj

def preselection(tr):
    if tr.MetNoLep < 160 : return False
    if tr.nJets < 2: return False
    if (tr.MET_pt - tr.CaloMET_pt)/tr.MetNoLep > 0.5 : return False
    if tr.isData==1 and (not (tr.met_filters_2017_data>0.1)): return False
    if (not tr.isData==1) and (not (tr.met_filters_2017_mc>0.1)): return False
    if abs(tr.JetMetmindPhi) < 0.5 : return False
    if tr.nMediumBJet > 0.5 : return False
    if tr.nLoosePhoton > 0.5 : return False
    if tr.isData : 
        if tr.nVetoElectron > 0.5 : return False 
        if tr.nLooseMuon    > 0.5 : return False 
        if tr.nVLooseTau    > 0.5 : return False 
     
    horn_sel = False
    if ( ( abs(tr.MetNoLep - tr.TkMET_pt)/tr.MetNoLep > 0.8 ) &
         ( ( ( abs(tr.Leading_jet_eta) > 2.8 ) & ( abs(tr.Leading_jet_eta) < 3.2 ) ) |
           ( ( abs(tr.Subleading_jet_eta) > 2.8 ) & ( abs(tr.Subleading_jet_eta) < 3.2 ) ) ) ):
        horn_sel = True
    if horn_sel: return False

    return True
    # here define a simple analysis (selection of cuts or whatever)

def selectMTR(tr): 
     
    if tr.MetNoLep < 250 : return False
    if tr.dijet_M  < 200 : return False
    if tr.Leading_jet_pt     < 80 : return False
    if tr.Subleading_jet_pt  < 40 : return False
    if abs(tr.dijet_dPhi)    > 1.5 : return False
    if abs(tr.dijet_dEta)    < 1   : return False
    if not (tr.Leading_jet_eta*tr.Subleading_jet_eta < 0): return False
    if abs(tr.Leading_jet_eta)    > 4.7 : return False
    if abs(tr.Subleading_jet_eta) > 4.7 : return False
    if tr.isData==1 and (not (tr.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight>0.1 or tr.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60>0.1) ): return False 
    return True

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
        and event.nMediumBJet == 0
    ):
 
        # if ((event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 == 1 or event.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)
        #     and event.nLoosePhoton == 0
        #     #        and event.met_filters_2018_mc
        #     and event.MetNoLep_CleanJet_mindPhi > 1.8
        #     and event.MetNoLep_pt  >= 160
        #     and event.MetNoLep_pt  < 250
        #     and event.nCleanJet >= 2
        #     and event.CleanJet_pt[0] > 140
        #     and abs(event.CleanJet_eta[0]) < 5.0
        #     and event.CleanJet_pt[1] > 70
        #     and abs(event.CleanJet_eta[1]) < 5.0
        #     and event.CleanJet_eta[0]*event.CleanJet_eta[1] < 0
        #     and event.diCleanJet_M > 900
        #     and event.diCleanJet_dPhi < 1.5
        #     and abs(event.diCleanJet_dEta) > 1
        # ):
        return True
    else:
        return False
        
def getKFactorWeight(hist,mjj,bospt,syst):
    weight = hist.GetBinContent(hist.FindBin(bospt,mjj))
    #print (bospt,mjj,hist.FindBin(bospt,mjj),weight)
    return weight

# def getKFactorWeight(hist,bospt,syst,nom):
#     weight = hist.GetBinContent(hist.FindBin(bospt))

    #Apply ad-hoc correction for scales missing below 200 GeV pT
    # if ( bospt < 200 and 
    #      (     
    #          syst == "_Renorm_Up"
    #          or syst == "_Renorm_Down"
    #          or syst == "_Fact_Up"
    #          or syst == "_Fact_Down"
    #      )
         
    # ):

    #     difference220 = hist.GetBinContent(hist.FindBin(220))-nom.GetBinContent(nom.FindBin(220))
    #     weight = difference220 + nom.GetBinContent(nom.FindBin(bospt))

#    return weight
    

def main(args):
    

    signal.signal(signal.SIGINT, signal_handler) 
    signal.signal(signal.SIGUSR1, signal_handler) 
    sampletype = args[1] 

    #print (sampletype)
    # with open(args[2], 'r') as f:
    #     infile = yaml.load(f)

    chain = TChain("Events")
    chain.Add(args[2])
    # for filename in infile["datasets"][0]["files"]:
    #     print(filename)
    #     chain.Add(filename)

    #chain.Add(args[3])

    #Get the normalisation (scale by xs/sum of weights, taken from yaml file)
    #norm = float(infile["datasets"][0]["xs"])/infile["datasets"][0]["nevents"]
    
    

    systs = ["", "_Renorm_Up", "_Renorm_Down", "_Fact_Up", "_Fact_Down", "_PDF_Up", "_PDF_Down"]
    hists = []
    make_hists(systs,hists)
    #    load k-factors file
    kfac_w = ROOT.TFile("20200325/2Dkfactor_VBF_wjet.root","READ")
    kfac_z = ROOT.TFile("20200325/2Dkfactor_VBF_zjet.root","READ")
    # kfac_w = ROOT.TFile("kfactor_VTR_wjet.root","READ")
    # kfac_z = ROOT.TFile("kfactor_VTR_zjet.root","READ")
    kfacfile = kfac_w
    if ( sampletype == "z" ):
        kfacfile = kfac_z
    
    kfacs = []
    # _200_500 = []
    # kfac_500_1000 = [] 
    # kfac_1000_1500 = []
    # kfac_1500_5000 = []

    for syst in systs:
        #kfac_200_500.append(kfacfile.Get("kfactors_shape%s/kfactor_VTR_boson_pt"%(syst)))
        kfacs.append(kfacfile.Get("kfactors_shape%s/kfactor_vbf"%(syst)))
        
        # kfac_200_500.append( hist.ProjectionX(str(syst) + "_200_500",2,2) )
        # kfac_500_1000.append( hist.ProjectionX(str(syst) + "_500_1000",3,3) )
        # kfac_1000_1500.append( hist.ProjectionX(str(syst) + "_1000_1500",4,4) )
        # kfac_1500_5000.append( hist.ProjectionX(str(syst) + "_1500_5000",5,5) )

    #i = 0
    totalEntries = str(chain.GetEntries())
    for entry,event in enumerate(chain):
        if ( entry%10000 == 0 ):
            print (str(entry) + " / " + totalEntries)
            #start = time.time()
        if ( preselection(event) and selectMTR(event) ):
            # end = time.time()
            # print (start-end)
            
            bospt,mjj = get_gen_boson_jet_AM(event)
            print (mjj)
            nomweight =  get_nominal_weight(event)
            #nomweight*=norm

            #Get NLO weight and apply based on pt and mjj
            
            # mjjhist = kfac_200_500
            # if (mjj>500):
            #     mjjhist = kfac_500_1000
            # if (mjj>1000):
            #     mjjhist = kfac_1000_1500
            # if (mjj>1500):
            #     mjjhist = kfac_1500_5000
            weights = []            
            
            for i,syst in enumerate(systs):
                weights.append(getKFactorWeight(kfacs[i],mjj,bospt,syst))
                #weights.append(getKFactorWeight(kfacs[i],bospt,syst,mjjhist[0]))

            #fill_hists((hists,weights,event.diCleanJet_M,nomweight))
            fill_hists(hists,weights,event.dijet_M,nomweight)

            if (interruptLoop==True):
                break

    save_hists(hists,args[3])


main(sys.argv)
