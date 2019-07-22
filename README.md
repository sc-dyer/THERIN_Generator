# THERIN_Generator
A program for generating THERIN files for use in THERIAK-DOMINO

This program was written in Python 3 but it should work for Python 2

To run this program just run main.py

Using a .csv file with major elements in the top row and sample name in the left 
column, this will convert from wt% to mol% (assuming Fe is reduced) and output
a THERIN file for each record. These files will need to be renamed "THERIN" when
used in THERIAK-DOMINO

This program reads csv files that have geochemical data in wt%. The header needs to be formatted like so:
[Name, you can call this column whatever you want],[Oxide1],[Oxide2],[oxide3]...
The order of the oxides shouldnt matter and if you have weird components that 
arent accounted for the program will tell you but it should be easy to add those in. 
If you have both Fe2O3 and FeO it will combine those into one column in the output file for Fe.
 Don't include anything like Fe2O3(T), just rename it.
 
Get the file names and directories and put them in the correct format
The sample name column should be the same as SAMPLE
There must be no empty cells! If you have no data for a cell enter 0 in the file

This program was written by Sabastien C. Dyer
Questions? Concerns? Find my contact info at www.scdyer.com
