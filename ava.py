#!/usr/bin/env python3

import os
import re
from numpy import array
import pandas as pd


# Get working directory for data
def get_working_directory():
    dir_path = input('Please input working directory: ')

    if dir_path in os.listdir():
        return dir_path

    else:
        print(f'Error: Directory {dir_path} not found...')
        retry = get_working_directory()
        return retry


# Collect ligand file names for log files
def get_ligands():
    # Check that a file exists with the working directory
    def file_check(file):
        if os.path.isfile(file):
            pass
        else:
            print(f'Error: {file} not found...')

    ligand = input('Ligands: ')  # Receive files names for ligands
    ligands = ligand.split()  # Split filenames into list
    ligand_map = map(os.path.isfile, ligands)  # Map ligands to check if all files exist

    # Check if all files can be found, if they can't be found: flag non-existent files and ask for input again
    if not all(ligand_map):
        [file_check(file) for file in ligands]
        print('Please check filenames and re-enter')
        retry = get_ligands()
        return retry

    # If all files found accept input and return list of files
    else:
        print('File(s) accepted...')
        return ligands


# Collect receptor file name for log files
def get_receptor():
    receptor_file = input('Receptor file: ')

    # Check that the file exists and returns filename if True
    if os.path.isfile(receptor_file):
        print('Receptor file accepted...')
        return receptor_file

    # If file not found - re-request file name
    else:
        print(f'Error: {receptor_file} not found')
        print('Please check filenames and re-enter')
        retry = get_receptor()
        return retry


# Collect coordinates for log files
def get_coords():
    # Function to determine if a value is a float, returns True or False accordingly
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    coordinates_input = input('Grid co-ordinates: ')  # Receive coordinates in format x y z
    coord = coordinates_input.split()  # Generate list of coordinates
    coord_map = map(is_float, coord)  # Check coordinates are float

    # Check all 3 coordinates have been provided
    if len(coord) != 3:
        print('Error: Please enter exactly 3 coordinates separated by a space')
        retry = get_coords()
        return retry

    # Check all coordinates are numeric values
    if not all(coord_map):
        print('Error not all values are not numbers')
        retry = get_coords()
        return retry

    # accept and return input if all values are present and correct
    else:
        print('Coordinates accepted...')
        return coord


# Collect box size parameters for log files
def get_box_size():
    # Check if a give value is a positive integer
    def check_pos(value):

        n = int(value)

        if n > 0:
            return True

        else:
            return False

    box_size_input = input('Box size: ')
    box = box_size_input.split()
    box_map = map(int, box)

    # Check all 3 coordinates have been provided
    if len(box) != 3:
        print('Error: Please enter exactly 3 coordinates separated by a space')
        retry = get_box_size()
        return retry

    # Check all 3 coordinates are integers
    try:
        all(box_map)

    except ValueError:
        print('Error: Box values must be positive integers greater than 0')
        retry = get_box_size()
        return retry

    # Check all integers are positive
    if not all([check_pos(n) for n in box]):
        print('Error: Box values must be positive integers greater than 0')
        retry = get_box_size()
        return retry

    # accept and return input if all values are present and correct
    else:
        print('Box parameters accepted...')
        return box


# Collect seeds if any for log files
def get_seeds():
    seed = input('Seed (optional): ')  # Receive seeds in format 1 2 3
    seed_list_input = seed.split()  # separate seeds into list

    # Check seeds are integers (can be positive or negative)
    try:
        seed_map = map(int, seed_list_input)  # generate a list of seeds as integers

        # If no input give - default seed is 0
        if len(seed_list_input) < 1:
            return [0]

        # accept and return input if all values are present and correct
        else:
            print('Seed(s) accepted...')
            return list(seed_map)

    # If not integer value is received ask for input again
    except ValueError:
        print('Error: seed(s) must be an integer')
        retry = get_seeds()
        return retry


# Write a basic  config file for AutoDock Vina - ligands, receptors, outputs, seed (0), grid size and coordinates.
def config_writer(ligands, receptor_input, coord, box, seeding=0):
    conformations_directory = f'conformations-{seeding}'
    logs_directory = f'logs-{seeding}'
    file_name = f'{ligands[:-6]}-config-{seeding}.txt'
    receptor_file = receptor_input
    ligand_file = ligands
    output_file = f'{conformations_directory}/{ligands[:-6]}-{seeding}.pdbqt'
    log_file = f'{logs_directory}/{ligands[:-6]}-log-{seeding}.txt'

    # Generate the config file using inputs
    with open(file_name, 'w') as config:
        config.write(f'receptor = {receptor_file}\n'  # receptor file
                     f'ligand = {ligand_file}\n\n'  # ligand file
                     f'center_x = {coord[0]}\n'  # grid coordinates for box
                     f'center_y = {coord[1]}\n'
                     f'center_z = {coord[2]}\n\n'
                     f'size_x = {box[0]}\n'  # box size parameters 
                     f'size_y = {box[1]}\n'
                     f'size_z = {box[2]}\n\n'
                     f'out = {output_file}\n'  # Docking confirmation output
                     f'log = {log_file}\n\n'  # Log file output
                     f'seed = {seeding}'  # Seed for experiment
                     )

        file_names.append(file_name)  # append file name to list for automatic docking


def get_binding_data_csv():
    # Extract data from log files
    def extract_data(file, i):
        file_name = file.split('-')  # extract ligand name and seed number from file name as a list
        ligand = file_name[0]  # store ligand name
        seed = file_name[-1].replace('.txt', '')  # store seed number

        # Open log file to collect binding data
        with open(file, 'r') as log:
            try:
                logs = log.readlines()  # convert each line into a string
                raw_data = logs[i].split()  # split values into list
                map_data = map(float, raw_data)  # convert strings to floats
                list_data = list(map_data)  # convert map to list
                list_data.insert(0, ligand)  # Add ligand name as 1st element
                list_data.insert(1, seed)  # Add seed number as 2nd element
                log_list.append(list_data)  # Append data to overall data list

            except IndexError:
                print(f'Error could not read file: {file}')
                pass

            except UnicodeDecodeError:
                print(f'Error could not read file: {file}')
                pass

            except ValueError:
                print(f'Error could not read file: {file}')
                pass

    if "results" not in os.listdir():
        os.mkdir("results")
        print('results directory created')

    current_working_directory = os.getcwd()
    directory_list = ' '.join(str(ele) for ele in os.listdir())  # Generate string to search for logs directories

    result = re.finditer(r"logs-[0-9]*[0-9]*[0-9]", directory_list)  # Identify logs directories within pwd

    log_dirs = []
    [log_dirs.append(val.group(0)) for val in result]  # store names of log directories in a list

    log_list = []  # store rows of data extracted from log files

    # Access and collect log data from log files in each directory
    for directory in log_dirs:
        os.chdir(directory)
        print(f'Extracting Log data from {directory}...')
        [extract_data(file, i) for file in os.listdir() for i in range(25, 35, 1)]
        print(f'Log data extracted from {directory}...')
        os.chdir(current_working_directory)

    log_array = array(log_list)  # convert collected data into a 2D NumPy array

    # convert 2D NumPy array to DataFrame
    log_df = pd.DataFrame(log_array, columns=['ligand', 'seed', 'binding mode', 'affinity (kcal/mol)',
                                              'distance from best mode rmsd l.b', 'distance from best mode rmsd u.b'])

    path = f'{current_working_directory}/results/binding-affinity-data.csv'  # generate file name for csv file
    log_df.to_csv(path, index=False, header=True)  # Save DataFrame to CSV file
    print(f'Log data retrieved and saved as {path}')  # Tell user location of CSV file


def visualise_structures():
    directory_list = ' '.join(
        str(ele) for ele in os.listdir())  # Generate string to search for conformation directories

    result = re.finditer(r"conformations-[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]*[0-9]",
                         directory_list)  # Search for directories

    conformation_dirs = []
    [conformation_dirs.append(val.group(0)) for val in result]  # Store identified directories

    conformations_list = [receptor]  # list of all .pdbqt files to be visualised
    [conformations_list.append(f'{directory}/{file}') for directory in conformation_dirs for file in
     os.listdir(directory)]  #

    conformation_files = " ".join(conformations_list)

    pymol_command = f'/Applications/PyMOL.app/Contents/MacOS/PyMOL -cq {conformation_files} -d "save results/analysis.pse"'

    os.system(pymol_command)


# Run Script
if __name__ == '__main__':
    file_names = []  # Empty list for names of config files

    working_directory = get_working_directory()  # Ask for working directory for ava
    os.chdir(working_directory)  # change directory to input

    ligand_list = get_ligands()  # Generate a list of ligand files
    receptor = get_receptor()  # Receive file name of receptor
    coordinates = get_coords()  # Receive co-ordinates of box in format x y z
    box_size = get_box_size()  # Receive box size in format x y z
    seed_list = get_seeds()  # Receive list of seeds for docking experiments

    # Generate config files for AutoDock Vina
    [config_writer(x, receptor, coordinates, box_size, seeding=y) for y in seed_list for x in ligand_list]

    # Run AutoDock Vina using generated config files list
    [os.system(f'vina --config {config}') for config in file_names]

    get_binding_data_csv()  # Collect binding affinity data and save as a CSV file
    visualise_structures()  # Visualise the results of AutoDock Vina predictions for all experiments
