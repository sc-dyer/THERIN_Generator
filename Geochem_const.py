#Geochem_const.py
#Contains definitions of the different components

import Component
#Making the components: Input values are name, molar weight, oxide ratio, cation number, Cation name
SiO2 = Component.Component("SiO2", 60.08, 2, 1, "Si")
Al2O3 = Component.Component("Al2O3", 101.96, 3/2, 2, "Al")
Fe2O3 = Component.Component("Fe2O3", 159.69, 1, 2, "Fe") #Assumes reduced iron so using oxide ratio for FeO instead, only used for calculating O2
FeO = Component.Component("FeO", 71.844, 1, 1, "Fe")
MnO = Component.Component("MnO", 70.937, 1, 1, "Mn")
MgO = Component.Component("MgO", 40.3044, 1, 1, "Mg")
CaO = Component.Component("CaO", 56.0774, 1, 1, "Ca")
Na2O = Component.Component("Na2O", 61.9789, 1/2, 2, "Na")
K2O = Component.Component("K2O", 94.2, 1/2, 2, "K")
TiO2 = Component.Component("TiO2", 79.866, 2, 1, "Ti")
P2O5 = Component.Component("P2O5", 283.886, 5/2, 2, "P")
H2O = Component.Component("H2O", 18.01528, 1/2, 2, "H")
CO2 = Component.Component("CO2", 44.01, 2, 1, "C")

COMPONENTS = [SiO2, Al2O3, Fe2O3, FeO, MnO, MgO, CaO, Na2O, K2O, TiO2, H2O, CO2] #No P2O5 because unreliable data, add if desired
GT_ENDMEM = ['alm','spss','gr','py']#End member codes for garnet in domino
