#main.py for THERIN_Generator
#Using a .csv file with major elements in the top row and sample name in the left 
#column, this will convert from wt% to mol% (assuming Fe is reduced) and output
#a THERIN file for each record. These files will need to be renamed "THEREIN" when
#used in THERIAK-DOMINO

#This program reads csv files that have geochemical data in wt%. The header needs to be formatted like so:
#[Name, you can call this column whatever you want],[Oxide1],[Oxide2],[oxide3]...
#The order of the oxides shouldnt matter and if you have weird components that 
#arent accounted for the program will tell you but it should be easy to add those in. 
#If you have both Fe2O3 and FeO it will combine those into one column in the output file for Fe.
# Don't include anything like Fe2O3(T), just rename it.
#Get the file names and directories and put them in the correct format
#The sample name column should be the same as SAMPLE
#There must be no empty cells! If you have no data for a cell enter 0 in the file

#This program was written by Sabastien C. Dyer
#Questions? Concerns? Find my contact info at www.scdyer.com

import Geochem_const
import Component
import SCRIPT_Generator
import SampleComp
#import numpy as np
#import pandas as pd
#import re
#import sys
import csv
import os
import easygui

INIT_T = 500 #First temp in first line
INIT_P = 2500#First pressure in first line

#Following constants for scripting change at leisure
#Temperature range
T1 = 450 
T2 = 650
#Pressure range
P1 = 3000
P2 = 8000

#Garnet isopleth parameters
GT_MIN = 0 #Lowest molar proportion of a component
GT_MAX = 0.5 #Highest molar proportion of a component
GT_INT = 0.02 #Interval size between each isopleth
VOL_MIN = 0
VOL_MAX = 0.3
VOL_INT = 0.01
DATABASE = "tcdb55c2.txt"

#Column names in CSV file
SAMPLE = "Name"

PRINT_CODE = 0
#   < -1:   print information about selected or rejected phases from the database. 
#               NO EQUILIBRIUM CALCULATED. 
#       =-1:    print composition, considered phases and solution models. 
#               NO EQUILIBRIUM CALCULATED. 
#       = 0:    short output (stable assemblage) 
#       = 1:    long output (composition, considered phases, solution models, stable 
#               assemblage, activities of all phases 





print('Select the csv file where the geochemical data is stored')
#fileIn = input('Enter the full file name of the formatted geochem CSV file including directory: ')
fileIn = easygui.fileopenbox()
fileIn = fileIn.strip()
fileIn = fileIn.strip('"')

print('Select the desired directory for the THERIN files to be saved (WARNING: THIS WILL OVERWRITE FILES OF THE SAME NAME, SAVE TO NEW FOLDER IF YOU DONT WANT THIS TO HAPPEN)')
#fileOut = input('Enter the desired directory for the output files to be saved (WARNING: THIS WILL OVERWRITE FILES OF THE SAME NAME, SAVE TO NEW FOLDER IF YOU DONT WANT THIS TO HAPPEN): ')
fileOut = easygui.diropenbox()
fileOut = fileOut.strip()
fileOut = fileOut.strip('"')

print('Select the desired directory for the script files to be saved (WARNING: THIS WILL OVERWRITE FILES OF THE SAME NAME, SAVE TO NEW FOLDER IF YOU DONT WANT THIS TO HAPPEN): ')
#scriptOut = input('Enter the desired directory for the script files to be saved (WARNING: THIS WILL OVERWRITE FILES OF THE SAME NAME, SAVE TO NEW FOLDER IF YOU DONT WANT THIS TO HAPPEN): ')
scriptOut = easygui.diropenbox()
scriptOut = scriptOut.strip()
scriptOut = scriptOut.strip('"')


#This just adds appropriate formatting depending on if using a Mac or PC
if os.name == 'nt':#PC
    fileOut += "\\"
    scriptOut += "\\"
else:#Mac
    fileOut += "/"
    scriptOut += "/"
#attempt to open the read file and exit program if not found
try:
    readFile = open(fileIn, 'r')
except:
    print("File not found")
    exit(0)


chemRead = csv.DictReader(readFile)

sampleCompos = [] #empty array for SampleComp objects, will contain each record

for row in chemRead:
    #Add a SampleComp object to sampleCompos for each record
    name = row[SAMPLE]
    wtArray = []
    components = []
    for elem in Geochem_const.COMPONENTS:
        try:
            wtArray.append(float(row[elem.formula]))
            components.append(elem)
        except:
            print(elem.formula + " not in file")
    sampleCompos.append(SampleComp.SampleComp(name, wtArray, components))
    


readFile.close()

    


    
#Now lets output the mol percent in a spreadsheet

molCentFile = fileOut + "Sample_mols.csv"
try: 
    writeFile = open(molCentFile, 'w')
except:
    print('Problem creating new file')
    exit(0)
    
#Write the header
writeFile.write(SAMPLE)
firstSample = sampleCompos[0]
for elem in firstSample.components:
     writeFile.write("," + elem.cation + "(mol)")#Header column as the cation (mol)
   
for elem in firstSample.components:
    writeFile.write("," + elem.cation + "(mol %)")#Header column as the cation (mol %)
    

writeFile.write("\n")

#write each line
for i in range(len(sampleCompos)):
    thisSample = sampleCompos[i]
    writeFile.write(thisSample.name)
    
    for elem in thisSample.molArray: #Mol values
        writeFile.write("," + str(elem))
        
    for elem in thisSample.molCent:
        writeFile.write("," + str(elem))
    
    writeFile.write("\n")

        
writeFile.close()

#Finally it is time to write the Therein files
#It will not title the files "THERIN" but instead with the sample name. The user
#will have to change the name of the file themselves
title = ""
msg = "Enter mols of H2O and CO2, use a number less than 0 to use the values from the table"
fieldNames = ["Mols H2O","Mols CO2"]
fieldVals = easygui.multenterbox(msg,title,fieldNames)
H2O = float(fieldVals[0])
CO2 = float(fieldVals[1])

redCO2 = easygui.boolbox("Is CO2 reduced?",title,["Yes","No"])
#H2O = float(input('Enter the mols of H2O you wish to have in each sample, enter a number less than 0 if you want to use H2O from the table: '))
#CO2 = float(input('Enter the mols of CO2 you wish to have in each sample, enter a number less than 0 if you want to use CO2 from the table: '))
#redCO2 = input("Is the CO2 reduced? (y/n)")

for elem in sampleCompos:
   
    therinFile = fileOut + elem.name + ".txt"
    try: 
        writeFile = open(therinFile, 'w')
    except:
        print('Problem creating new file')
        exit(0)
    
    writeFile.write("    " + str(INIT_T) + "    " + str(INIT_P) + "\n")
    compoLine = str(PRINT_CODE) + "    "
    
   
    
    compoLine += elem.writeTHERINcompo(redCO2, CO2, H2O)
    writeFile.write(compoLine)
    writeFile.close()
    
    #Create script files, remove this if you dont want script files
    SCRIPT_Generator.phaseScript(compoLine,P1,P2,T1,T2,elem.name,scriptOut, DATABASE)#Generate script file for calculating phase diagram
    #Generate script file for calculating Gt isopleths for each endmember (Except andradite). 
    #Go to Geochem_const.py to see the endmembers used
    for i in range(len(Geochem_const.GT_ENDMEM)):
        SCRIPT_Generator.isoScript(compoLine, P1, P2, T1, T2, elem.name, scriptOut, DATABASE,"GARNET", Geochem_const.GT_ENDMEM[i], GT_MIN, GT_MAX, GT_INT)
    SCRIPT_Generator.volScript(compoLine, P1, P2, T1, T2, elem.name, scriptOut, DATABASE, "GARNET", VOL_MIN, VOL_MAX, VOL_INT)
  
                
        
print("Done!")