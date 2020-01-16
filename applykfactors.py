#!/bin/python3
import ROOT
from ROOT import *
from array import *
import sys
import io



def make_hists(names,hists):    
    for name in names:
        hist = ROOT.TH1D( "mjj_" + name , "", 100,0,1000)
        hists.append( hist )


def fill_hists(hists,weights,mjj,nominal_weight):    

    for hist, weight in zip(hists, weights):
        hist.Fill(mjj,weight*nominal_weight)

def save_hists(hists):    

    fout = ROOT.TFile("out2.root","RECREATE")
    for hist in hists:
        hist.Write()

def get_nominal_weight(event):
    weight = 1.

    weight *= event.VetoElectron_eventVetoW
    weight *= event.LooseMuon_eventVetoW
    weight *= event.puWeight
    weight *= event.VLooseSITTau_eventVetoW
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

    for part in range(len(event.pdgId)):
        if ( (abs(event.GenPart_pdgId[part])>10 and abs(event.GenPart_pdgId[part]) < 17) and ( (event.GenPart_status[part] == 1 and (event.GenPart_statusFlags[part] & 0x1)>0) or ((event.GenPart_statusFlags[part] & 0x1)>0 and (event.GenPart_statusFlags[part] & 0x2)>0) ) ):
            if (event.genPartIdxMother[part]>=0):
                mother = event.genPartIdxMother[part]

                while True:

                    if (event.GenPart_pdgId[mother] == 23 or abs(event.GenPart_pdgId[mother]) == 24):
                        boson_found = True
                        break
                    else:
                        mother = mother.genPartIdxMother;
                        if ( event.genPartIdxMother[mother] < 0  ):
                            break

            if (boson_found):
                boson_pt = event.pt[mother]

            if (event.GenPart_pdgId[part]>0):
                lep1.SetPtEtaPhiM( GenPart_pt[part], GenPart_eta[part], GenPart_phi[part], GenPart_mass[part]  );
                if ( abs(GenPart_GenPart_pdgId[part]) == 12 or abs(GenPart_GenPart_pdgId[part]) == 14 or abs(GenPart_GenPart_pdgId[part]) == 16):
                    lep1_isnu = True
            else:
                lep2.SetPtEtaPhiM( GenPart_pt[part], GenPart_eta[part], GenPart_phi[part], GenPart_mass[part]  );
                if ( abs(GenPart_GenPart_pdgId[part]) == 12 or abs(GenPart_GenPart_pdgId[part]) == 14 or abs(GenPart_GenPart_pdgId[part]) == 16):
                    lep2_isnu = True


    if (not boson_found):
        boson_pt = (lep1.p4()+lep2.p4()).Pt()
        boson_found = True




    jet = ROOT.TLorentzVector()

    jets = []
    for pt,eta,phi,m in zip(event.GenJet_pt,event.GenJet_eta,event.GenJet_phi,event.GenJet_mass):
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

    mjj = (jets[0] + jets[1]).M()

    
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

chain = TChain("Events")


chain.Add("root://gfe02.grid.hep.ph.ic.ac.uk:1097///store/user/ebhal/CHIP_skim_mc_2018_20200104/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/crab_DYJetsToLL_M-50_HT-400to600_RunIIAutumn18NanoAODv5_ext2-v1/200104_215104/0000/tree_10.root")




systs = ["Nominal", "Renorm_Up"]
hists = []
make_hists(systs,hists)


i = 0
for entry,event in enumerate(chain):
    if ( entry%1000 == 0 ):
        print entry
    if ( pass_selection(event) ):

        bospt,mjj = get_gen_boson_jet(event)

        print (bospt,mjj)

        nomweight =  get_nominal_weight(event)

        #get weights list
        weights = []
        for i,syst in enumerate(systs):
            weights.append(1)

        fill_hists(hists,weights,event.diCleanJet_M,nomweight)
        i=i+1

    # if entry > 100000:
    #     break;
save_hists(hists)
print (i)
