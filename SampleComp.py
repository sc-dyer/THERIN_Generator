import Geochem_const
import Component
#A class for handling each record in a table of compositions
class SampleComp:
    
    def __init__(self, nameIn, wtArrayIn, componentsIn):
        self.name = nameIn
        self.wtArray = wtArrayIn
        self.components = componentsIn
        
        self.convertMol()
        self.convertMolCent()
        
    def convertMol(self):
        #Convert wt% to mols
        self.molArray = []
        feOPos = -1
        fe2O3Pos = -1
        for i in range(len(self.wtArray)):
            mol = self.components[i].catNum*self.wtArray[i]/self.components[i].weight # CatNum * Wt% / M
            self.molArray.append(round(mol,5))
            if self.components[i].formula == "FeO":
                feOPos = i
            elif self.components[i].formula == "Fe2O3":
                fe2O3Pos = i
                
        #Basically if there is both FeO and Fe2O3 in the sample composition then 
        #add them together and put the total in the FeO column and bring the Fe2O3 column with 0
        if feOPos >= 0 and fe2O3Pos >= 0:
            self.molArray[feOPos] += self.molArray[fe2O3Pos]
            self.molArray.pop(fe2O3Pos)
            self.components.pop(fe2O3Pos)#This makes the wtArray not match with the components, shouldnt be an issue because wtArray isnt used again
            
        
            
    def convertMolCent(self):
        #Convert mol to mol %
        #Note this is not molar oxides, just %Mol of Cations
        #Shouldnt be hard to alter this to do mol% oxides though
        
        self.molCent = []
        totMol = sum(self.molArray)
        
        for elem in self.molArray:
            percent = 100*elem/totMol
            self.molCent.append(round(percent, 5))
            
    def writeTHERINcompo(self, redCO2, CO2, H2O):
        #Makes the composition line for the THERIN file
        mol_O = 0
        therin = ""
        for i in range(len(self.molArray)):
            #IF block, writes to the file and calculates Oxygen
            #If a CO2 or H2O value is given, they will ignore the values that might be in the data tables
            #If CO2 is reduced, it will ignore the value for the Oxygen calculation
            currComp = self.components[i]
            if self.molArray[i] > 0:
                
                if redCO2 or CO2 >= 0:
                    if H2O >= 0:
                        if currComp.formula!= "H2O" and currComp.formula!= "CO2" :
                            mol_O += self.molArray[i]*currComp.ox2cat            
                            therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                    elif currComp.formula!= "CO2":#Ignore the CO2 column for adding up mols of stuff
                        mol_O += self.molArray[i]*currComp.ox2cat            
                        therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                else:
                    if H2O >= 0:
                        if currComp.formula!= "H2O":
                            mol_O += self.molArray[i]*currComp.ox2cat            
                            therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                    else:
                            mol_O += self.molArray[i]*currComp.ox2cat            
                            therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                
                if not redCO2 and CO2 < 0:#This is to catch if CO2 is reduced but you still have a value provided in the data table
                    if currComp.formula== "CO2":
                            mol_O += self.molArray[i]*currComp.ox2cat            
                            therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                elif redCO2 and CO2 <0:
                    if currComp.formula== "CO2":
                        therin += currComp.cation.upper() + "(" + str(self.molArray[i]) + ")"
                    
        #Write preset C and H into file
        if CO2 >= 0 and not redCO2:
            mol_O += CO2*2
            therin += "C(" + str(CO2) + ")"
        elif CO2 >= 0:
            therin += "C(" + str(CO2) + ")"
            
        
        if H2O >= 0:
            mol_O += H2O
            therin += "H(" + str(H2O*2) + ")"
    
        therin += "O(" + str(round(mol_O,6)) + ")     *"
        return therin