#SCRIPT_Generator.py
#Possible future direction, copy a script file as a template?
#For now, more methods can be added or these ones can be changed to fit with what you need
#Note that \n makes a newline, this set up works for me but I dont know what
#THERIN_Generator.py has these two methods implemented to automatically generate these files
#from a csv file of wt% compositions. 

#This method creates a script file that will calculate the phase assemblages
def phaseScript(compoLine, P1, P2, T1, T2, sample, fileLoc, database):
    fileName = sample + "_Phase"
    writeFile = fileLoc + fileName + ".txt"#Full filepath
    #THis portion just ensures that the file can be made
    try: 
        writeFile = open(writeFile, 'w')
    except:
        print('Problem creating new file')
        exit(0)
    
    writeFile.write("script." + fileName + ".txt\n")
    writeFile.write(fileName + ".plt\n" + database + "\n")
    writeFile.write("    1.0000    300    0.010000   0.1000000E-08   0.1000000E-08   0.1000000E+01 0.1000000E-03    400     400     500\n")#Not sure what these numbers mean
    writeFile.write(compoLine + "\n\n\n\n\n\n")
    writeFile.write("TC  "+ str(T1) + "  " + str(T2) + "\n")
    writeFile.write("P  " + str(P1) + "  " + str(P2) + "\n.\n1\n 0.0000000E+00   0.0000000E+00\n")
    writeFile.write("_"+ fileName + "_pix")
    writeFile.close()
    domjob(fileName, fileLoc)
  
#This method will create a script file that will calculate the phase isopleths for
#whichever endmember entered in to the field endMem. 
#Note to self: Edit this in future to use any mineral
def isoScript(compoLine, P1, P2, T1, T2, sample, fileLoc, database,phase, endMem,minVal, maxVal,interval):
    fileName = sample + "_" + endMem
    writeFile = fileLoc + fileName + ".txt"
    try: 
        writeFile = open(writeFile, 'w')
    except:
        print('Problem creating new file')
        exit(0)
    
    writeFile.write("script." + fileName + ".txt\n")
    writeFile.write(fileName + ".plt\n" + database + "\n")
    writeFile.write("    1.0000    300    0.010000   0.1000000E-08   0.1000000E-08   0.1000000E+01 0.1000000E-03    400     400     500\n")#Not sure what these numbers mean
    writeFile.write(compoLine + "\n\n\n\n\n\n")
    writeFile.write("TC  "+ str(T1) + "  " + str(T2) + "\n")
    writeFile.write("P  " + str(P1) + "  " + str(P2) + "\n")
    writeFile.write(phase + "  "+ endMem + "  1" + "  " + str(minVal) + "  " + str(maxVal) + "  " + str(interval) + "\n1\n 0.0000000E+00   0.0000000E+00\n")
    writeFile.write("_"+ fileName + "_pix")
    writeFile.close()
    domjob(fileName, fileLoc)
    
#Generate a script for volume% of a specific phase
def volScript(compoLine, P1, P2, T1, T2, sample, fileLoc, database,phase,minVal, maxVal,interval):
    fileName = sample + "_vol"
    writeFile = fileLoc + fileName + ".txt"
    try: 
        writeFile = open(writeFile, 'w')
    except:
        print('Problem creating new file')
        exit(0)
    
    writeFile.write("script." + fileName + ".txt\n")
    writeFile.write(fileName + ".plt\n" + database + "\n")
    writeFile.write("    1.0000    300    0.010000   0.1000000E-08   0.1000000E-08   0.1000000E+01 0.1000000E-03    400     400     500\n")#Not sure what these numbers mean
    writeFile.write(compoLine + "\n\n\n\n\n\n")
    writeFile.write("TC  "+ str(T1) + "  " + str(T2) + "\n")
    writeFile.write("P  " + str(P1) + "  " + str(P2) + "\n")
    writeFile.write(phase + "  vol%" + "  1" + "  " + str(minVal) + "  " + str(maxVal) + "  " + str(interval) + "\n1\n 0.0000000E+00   0.0000000E+00\n")
    writeFile.write("_"+ fileName + "_pix")
    writeFile.close()
    domjob(fileName, fileLoc)
    
    
#Method to write to domjob file
#Probably need to edit a domino made domjob file but whatever
def domjob(fileName, filepath):
    writeFile = filepath + "domjob.txt"
    try: 
        writeFile = open(writeFile, 'a')
    except:
        print('Problem creating new file')
        exit(0)
    writeFile.write("domino  " + fileName + ".txt\n")
    writeFile.write("guzzler " + fileName + ".plt  " + fileName + ".cln  " + fileName + ".rxn\n")
    writeFile.write("explot  " + fileName + ".cln  " + fileName + ".ps\n")
    writeFile.close()
    
