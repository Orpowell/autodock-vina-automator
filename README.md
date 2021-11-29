# AutoDock Vina Automator

A.V.A, is designed to automate the docking of multiple ligands to a single target protein in AutoDock Vina.  A.V.A automates large parts of the workflow associated with ligand docking including:

- Preparing ligand config file for AutoDock Vina
- Running AutoDock Vina
- Producing technical replicates of ligand docking simulations
- Visualising ligand docking simulations
- Collating predicted binding affinity data for ligands
- Storing and organising files produced by AutoDock Vina and A.V.A

Dependencies for A.V.A can be found in requirements.txt.  A.V.A also requires Python >=3.7 and AutoDock Vina v1.1.2 to run. 

### Future Updates
Future updates to A.V.A may include:
- Introducing flexible residues in the target protein
- Docking for multiple target proteins to a set of ligands

## Installation on MacOSX and Linux
At the command line, change directory to the directory where ava.py was downloaded, E.g <download-directory>, using the full path name.

    cd <download-directory>

Now move the file to where you normally keep your binaries. This directory should be in your path. Note: you may require administrative privileges to do this (either switching user to root or by using sudo).

As root:

    mv ava.py /usr/local/bin/

As regular user:

    sudo mv ava.py /usr/local/bin/

After installation, A.V.A can be run directly from the shell or Terminal using the  follwing command: 

 		ava.py

Alternatively, A.V.A can be run from an IDE.

## Ligand Docking with A.V.A
### Scenario
In this scenario, we will run predict how 3 ligands (Ligand1, Ligand2 & Ligand3) bind to the active site of the target protein (ProteinX).  To ensure reproducibility of results, each ligand docking will be run 3 times with 3 unique seeds: 22, 495 & 1,000. 

### Pre-processing for A.V.A
Before running A.V.A, all files must be prepared in the appropriate format for AutoDock Vina (.pdbqt files). This must be done for ligands and the target protein. Additionally, the size and location of the search space must be determined for the target protein. These tasks can be achieved using AutoDock Tools. 

In our scenario, we will create the 4 following files: Ligand1.pdbqt, Ligand2.pdbqt, Ligand3.pdbqt & ProteinX.pdbqt . Using AutoDock Tools, we identified the co-ordinates for active site (10,-5,88) and the dimensions of the box needed to cover the area (20, 20, 20). 

### Running A.V.A
To begin, a directory should be set-up containing all ligand and receptor files in the .pdbqt file format before running ava.py in the directory. In the scenario, we will store the prepared files in a directory named, <MyWorkingDirectory> . A.V.A will then ask for the following inputs, press enter to continue after each input:

Working directory: 
- The path to the directory containing all pre-processed files. 
- e.g MyWorkingDirectory

Ligand(s): 
- The file name for each ligand separated by a space
- e.g: Ligand1.pdbqt Ligand2.pdbqt Ligand3.pdbqt

Receptor: 
- The file name of the target protein
- e.g: ProteinX.pdbqt
          
Coordinates: 
- The coordinates of the search area separated by spaces formatted as x y z
-  e.g: 10 -5 88
             
Box size: The size of the search area separated by spaces formatted as x y z
          e.g: 20 20 20

Seed(s): 
- The integers used to seed the docking experiment(s) separated by spaces
- e.g: 20 400 1000 
- The default seed used is 0, if left blank
     
Autodock Vina will begin running as soon as all parameters are provided.

### A.V.A Outputs
A.V.A creates config files for each ligand for every seed in order to run AutoDock Vina. These are saved directly into the working directory in the format LIGAND-config-X.txt .
The conformation and log files created by AutoDock Vina for each ligand are stored in directories labelled with seed used for the experiment in the format Conformations-X and Logs-X. Log files are saved in the format LIGAND-log-X.txt. Conformation files are saved in the format LIGAND-X.pdbqt. (LIGAND = ligand used, X = seed used). 

After running AutoDock Vina, A.V.A processes the raw dat into processed outputs storied in a directory labelled results. This directory contains two files:

- A csv file containing the ligand binding affinity for every ligand in each docking experiment. This is collected from the log files generated by AutoDock Vina. This is called binding-affinity-data.csv

- A PyMol session that visualises docking conformations of all ligands from all seeds on the target protein. This is called analysis.pse.

In the scenario, the structure of files produced by A.V.A for docking experiments using the seed 20 would be as follows:

	MyWorkingDirectory
		 |
		 |---Ligand1-config-20.txt
		 |---Ligand2-config-20.txt
		 |---Ligand3-config-20.txt
		 |
		 |------Conformations-20
		 |	|---Ligand1-20.pdbqt
		 |	|---Ligand2-20.pdbqt
		 |	|---Ligand3-20.pdbqt
		 |
		 |------Logs-20
		 |	|---Ligand1-log-20.txt
		 |	|---Ligand2-log-20.txt
		 |	|---Ligand3-log-20.txt
		 |
		 |------Results
			|---analysis.pse
			|---binding-affinity-data.csv

## Citing this work

Information for citing this repository can be found in the CITATION.cff file.

