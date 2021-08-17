# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-70to100.yaml 2017_DYJetsToLL_M-50_HT-70to100.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-100to200.yaml 2017_DYJetsToLL_M-50_HT-100to200.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-200to400.yaml 2017_DYJetsToLL_M-50_HT-200to400.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-400to600.yaml 2017_DYJetsToLL_M-50_HT-400to600.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-600to800.yaml 2017_DYJetsToLL_M-50_HT-600to800.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-800to1200.yaml 2017_DYJetsToLL_M-50_HT-800to1200.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-1200to2500.yaml 2017_DYJetsToLL_M-50_HT-1200to2500.root
# python -u applykfactors.py z ~/invisible/Nick/analysis/samples/2017/background/DYJetsToLL_M-50_HT-2500toInf.yaml 2017_DYJetsToLL_M-50_HT-2500toInf.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-70To100.yaml 2017_WJetsToLNu_HT-70to100.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-100To200.yaml 2017_WJetsToLNu_HT-100to200.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-200To400.yaml 2017_WJetsToLNu_HT-200to400.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-400To600.yaml 2017_WJetsToLNu_HT-400to600.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-600To800.yaml 2017_WJetsToLNu_HT-600to800.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-800To1200.yaml 2017_WJetsToLNu_HT-800to1200.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-1200To2500.yaml 2017_WJetsToLNu_HT-1200to2500.root
# python -u applykfactors.py w ~/invisible/Nick/analysis/samples/2017/background/WJetsToLNu_HT-2500ToInf.yaml 2017_WJetsToLNu_HT-2500toInf.root


python -u applykfactors.py z /vols/cms/magnan/Hinvisible/Run2/200415/output_skims_2017/Nominal/dy.root 2017_DYJetsToLL.root
python -u applykfactors.py w /vols/cms/magnan/Hinvisible/Run2/200415/output_skims_2017/Nominal/wjets.root 2017_WJetsToLNu.root
