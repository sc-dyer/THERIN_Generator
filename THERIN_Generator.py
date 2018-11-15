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


import Geochem_const
#import numpy as np
#import pandas as pd
#import re
#import sys
#import csv
import os

INIT_T = 500 #First temp in first line
INIT_P = 2500#First pressure in first line
PRINT_CODE = 0
#   < -1:   print information about selected or rejected phases from the database. 
#               NO EQUILIBRIUM CALCULATED. 
#       =-1:    print composition, considered phases and solution models. 
#               NO EQUILIBRIUM CALCULATED. 
#       = 0:    short output (stable assemblage) 
#       = 1:    long output (composition, considered phases, solution models, stable 
#               assemblage, activities of all phases 

#Get the file names and directories and put them in the correct format
#fileIn = "/Users/Sabastien/Desktop/Synced Docs/Carleton/Python_Programs/THERIN_Generator/Geochem_data.csv"
#fileIn = "C:\\Users\\Sabastien\\Documents\\Carleton\\Python_Programs\\THERIN_Generator\\Geochem_Data.csv"
fileIn = input('Enter the full file name of the formatted geochem CSV file including directory: ')
fileIn = fileIn.strip()
fileIn = fileIn.strip('"')


#fileOut = "/Users/Sabastien/Desktop/Synced Docs/Carleton/Python_Programs/THERIN_Generator/"
#fileOut = "C:\\Users\\Sabastien\\Documents\\Carleton\\Python_Programs\\THERIN_Generator\\"
fileOut = input('Enter the desired directory for the output files to be saved (WARNING: THIS WILL OVERWRITE FILES OF THE SAME NAME, SAVE TO NEW FOLDER IF YOU DONT WANT THIS TO HAPPEN): ')
fileOut = fileOut.strip()
fileOut = fileOut.strip('"')
if os.name == 'nt':
    fileOut += "\\"
else:
    fileOut += "/"

#attempt to open the read file and exit program if not found
try:
    readFile = open(fileIn, 'r')
except:
    print("File not found")
    exit(0)

#Next we want to read the top line and parse it out, assuming the first column is the sample name
header = readFile.readline()
header = header.strip('\n')
columns = header.split(',')

#Now we want to parse out the rest of the file
row = readFile.readline()#Get the first row of data in the file


samples = [] #empty array for sample names
all_comp = [] #empty array for each row of wt data, to correspond with the sample in the same array position

while len(row) > 3:#check if reached end of data when row = \n or something else
        rowParse = row.strip('\n').split(',')
        samples.append(rowParse[0])#add the first column as the sample name
        sample_comp = []
        #This will convert each string into a float value, if the cell is empty it will add a 0 for that cell
        for i in range(1, len(rowParse)):
            if len(rowParse[i]) > 0:
                sample_comp.append(float(rowParse[i]))
            else:
                sample_comp.append(0)
        all_comp.append(sample_comp)#add row to matrix
        row = readFile.readline()#read line for next iteration
readFile.close()
#Before we convert to mol we have match the headers with the corresponding position in the oxide array in Geochem_const.py
ox_pos = []
for i in range(1, len(columns)):
    for j in range(len(Geochem_const.MAJ_OX)):
        
        if columns[i].lower() == Geochem_const.MAJ_OX[j].lower():
            ox_pos.append(j)#Provides a reference position to compare the two arrays
    if len(ox_pos) < i - 1:#If it didn't add a value to the array
        print("No data for component: " + columns[i])
        print("Please add to Geochem_const.py")
    
#Now we have our samples and their compositions and we want to convert it to mols

all_mols = []
Fe2O3_pos = -1
FeO_pos = -1
    
for i in range(len(samples)):
    sample_mols = []
    for j in range(len(ox_pos)):
        mol = Geochem_const.CAT_NUM[ox_pos[j]]*all_comp[i][j]/Geochem_const.MOL_W[ox_pos[j]]#Cation # * Wt% composition/Mol_wt
        sample_mols.append(mol)
    
   
    #This finds where the two iron oxides are (if there is more than one)
    for j in range(len(sample_mols)):
        if Geochem_const.MAJ_OX[ox_pos[j]] == "Fe2O3":
            Fe2O3_pos = j
        elif Geochem_const.MAJ_OX[ox_pos[j]] == "FeO":
            FeO_pos = j
    if Fe2O3_pos >= 0 and FeO_pos >= 0:
        #Basically if there is both FeO and Fe2O3 in the sample composition then 
        #add them together and put the total in the FeO column and bring the Fe2O3 column with 0
        sample_mols[FeO_pos] += sample_mols[Fe2O3_pos]
        sample_mols[Fe2O3_pos] = 0
    all_mols.append(sample_mols)

all_molCent = []
#Just for fun lets convert to mol percent so that we might be able to interpret the output better
for i in range(len(samples)):
    sample_molCent = []
    totMol = 0
    for j in range(len(all_mols[i])):
        totMol += all_mols[i][j]
    for j in range(len(all_mols[i])):
        sample_molCent.append(round(100*all_mols[i][j]/totMol,5))
    all_molCent.append(sample_molCent)
    
#Now lets output the mol percent in a spreadsheet

molCentFile = fileOut + "Mol_Percent.csv"
try: 
    writeFile = open(molCentFile, 'w')
except:
    print('Problem creating new file')
    exit(0)
#Write the header
writeFile.write(columns[0])
for i in range(len(ox_pos)):
    if Fe2O3_pos >= 0 and FeO_pos >= 0:
        if i != Fe2O3_pos:#Ignore Fe2O3, remove this if you want to account for different ox states
            writeFile.write("," + Geochem_const.CAT[ox_pos[i]])#Header column as the cation
    else:
        writeFile.write("," + Geochem_const.CAT[ox_pos[i]])
writeFile.write("\n")

#write each line
for i in range(len(samples)):
    writeFile.write(samples[i])#sample name
    for j in range(len(all_molCent[i])):
        if Fe2O3_pos >= 0 and FeO_pos >= 0:
            if j != Fe2O3_pos:#Ignore Fe2O3, remove this if you want to account for different ox states
                writeFile.write("," + str(all_molCent[i][j]))#Mol percentage
        else:    
            writeFile.write("," + str(all_molCent[i][j]))
    writeFile.write("\n")

        
writeFile.close()

#Finally it is time to write the Therein files
#It will not title the files "THEREIN" but instead with the sample name. The user
#will have to change the name of the file themselves

H2O = float(input('Enter the mols of H2O you wish to have in each sample, enter a number less than 0 if you want to use H2O from the table: '))
CO2 = float(input('Enter the mols of CO2 you wish to have in each sample, enter a number less than 0 if you want to use CO2 from the table: '))
redCO2 = input("Is the CO2 reduced? (y/n)")

for i in range(len(samples)):
    mol_O = 0
    thereinFile = fileOut + samples[i] + ".txt"
    try: 
        writeFile = open(thereinFile, 'w')
    except:
        print('Problem creating new file')
        exit(0)
        
    writeFile.write("    " + str(INIT_T) + "    " + str(INIT_P) + "\n")
    writeFile.write(str(PRINT_CODE) + "    ")
    
    for j in range(len(all_molCent[i])):
        #IF block, writes to the file and calculates Oxygen
        #If a CO2 or H2O value is given, they will ignore the values that might be in the data tables
        #If CO2 is reduced, it will ignore the value for the Oxygen calculation
        if all_molCent[i][j] > 0:
            if redCO2 == "y" or CO2 >= 0:
                if H2O >= 0:
                    if Geochem_const.MAJ_OX[ox_pos[j]]!= "H2O" and Geochem_const.MAJ_OX[ox_pos[j]]!= "CO2" :
                        mol_O += all_molCent[i][j]*Geochem_const.OX_RATIO[ox_pos[j]]            
                        writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
                elif Geochem_const.MAJ_OX[ox_pos[j]]!= "CO2":#Ignore the CO2 column for adding up mols of stuff
                    mol_O += all_molCent[i][j]*Geochem_const.OX_RATIO[ox_pos[j]]
                    writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
            else:
                if H2O >= 0:
                    if Geochem_const.MAJ_OX[ox_pos[j]]!= "H2O":
                        mol_O += all_molCent[i][j]*Geochem_const.OX_RATIO[ox_pos[j]]
                        writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
                else:
                    mol_O += all_molCent[i][j]*Geochem_const.OX_RATIO[ox_pos[j]]
                    writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
            
            if redCO2 != "y" and CO2 < 0:#This is to catch if CO2 is reduced but you still have a value provided in the data table
                if Geochem_const.MAJ_OX[ox_pos[j]]== "CO2":
                    writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
                    mol_O += all_molCent[i][j]*Geochem_const.OX_RATIO[ox_pos[j]]
            elif redCO2 == "y" and CO2 <0:
                if Geochem_const.MAJ_OX[ox_pos[j]]== "CO2":
                    writeFile.write(Geochem_const.CAT[ox_pos[j]].upper() + "(" + str(all_molCent[i][j]) + ")")
                
    #Write preset C and H into file
    if CO2 >= 0 and redCO2 != "y":
        mol_O += CO2*2
        writeFile.write("C(" + str(CO2) + ")")
    elif CO2 >= 0:
        writeFile.write("C(" + str(CO2) + ")")
        
        
    if H2O >= 0:
        mol_O += H2O
        writeFile.write("H(" + str(H2O*2) + ")")
    
    writeFile.write("O(" + str(round(mol_O,5)) + ")     *")
    
    writeFile.close()
  
    
  
                
        

print("Done!")