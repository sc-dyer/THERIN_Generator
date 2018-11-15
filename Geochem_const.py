#Molecular weights of major oxides
M_SIO2 = 60.08
M_AL2O3 = 101.96
M_FE2O3 = 159.69
M_FEO = 71.844
M_MNO = 70.937
M_MGO = 40.3044
M_CAO = 56.0774
M_NA2O = 61.9789
M_K2O = 94.2
M_TIO2 = 79.866
M_P2O5 = 283.886
M_H2O = 18.01528
M_CO2 = 44.01

#Major element data: All these arrays need to be the same size!
MAJ_OX = ["SiO2","Al2O3","Fe2O3","FeO","MnO","MgO","CaO","Na2O","K2O","TiO2","P2O5","H2O","CO2"] #Array of oxide names for matching with csv headers
MOL_W = [M_SIO2,M_AL2O3,M_FE2O3,M_FEO,M_MNO,M_MGO,M_CAO,M_NA2O,M_K2O,M_TIO2,M_P2O5,M_H2O,M_CO2]#Array of molar weights to match with the list of major oxides
OX_RATIO = [2,3/2,1,1,1,1,1/2,1/2,2,5/2,1/2,1/2]#Ratio of O to cation to match with list of major oxides, this assumes reduced iron so the oxide ratio being used for Fe2O3 is 1
CAT_NUM = [1,2,2,1,1,1,1,2,2,1,2,2,1]#Number of cations in each major oxide
CAT = ["Si","Al","Fe","Fe","Mn","Mg","Ca","Na","K","Ti","P","H","C"]