# THERIN_Generator
This program was written by Sabastien C. Dyer
If you have any questions or comments please email me at sabastien.dyer@carleton.ca
The latest version of this program and other programs I develop will be available at www.scdyer.com/software and https://github.com/sc-dyer/THERIN_Generator


A program for generating THERIN and script files for use in THERIAK-DOMINO

If you are unfamiliar with python I reccomend starting with downloading and installing pyzo(https://pyzo.org/). 
It is an integrated development environment which makes getting started with python fairly straightforward.
This program should work for python3 or python2. This program requires easygui to run. If you are running a python version earlier than 3.7 you will also need to install tkinter(https://tkdocs.com/tutorial/install.html)
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
 NOTE: If you are having problems with reading the CSV file make sure it is encoded as UTF-8
 
Get the file names and directories and put them in the correct format
The sample name column should be the same as SAMPLE
There must be no empty cells! If you have no data for a cell enter 0 in the file


