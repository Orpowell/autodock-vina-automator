#!/usr/bin/python3

import os


def get_ligands():
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


def get_receptor():
    receptor_file = input('Receptor file: ')

    if os.path.isfile(receptor_file):
        print('Receptor file accepted...')
        return receptor_file

    else:
        print(f'Error: {receptor_file} not found')
        print('Please check filenames and re-enter')
        retry = get_receptor()
        return retry


def get_coords():
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    coordinates_input = input('Grid co-ordinates: ')
    coord = coordinates_input.split()
    coord_map = map(is_float, coord)

    if len(coord) != 3:
        print('Error: Please enter exactly 3 coordinates separated by a space')
        retry = get_coords()
        return retry

    if not all(coord_map):
        print('Error not all values are not numbers')
        retry = get_coords()
        return retry

    else:
        print('Coordinates accepted...')
        return coord


def get_box_size():
    def check_pos(value):

        n = int(value)

        if n > 0:
            return True

        else:
            return False

    box_size_input = input('Box size: ')
    box = box_size_input.split()
    box_map = map(int, box)

    if len(box) != 3:
        print('Error: Please enter exactly 3 coordinates separated by a space')
        retry = get_box_size()
        return retry

    try:
        all(box_map)

    except ValueError:
        print('Error: Box values must be positive integers greater than 0')
        retry = get_box_size()
        return retry

    if not all([check_pos(n) for n in box]):
        print('Error: Box values must be positive integers greater than 0')
        retry = get_box_size()
        return retry

    else:
        print('Box parameters accepted...')
        return box


def get_seeds():
    seed = input('Seed (optional): ')  # Receive seeds in format 1 2 3
    seed_list_input = seed.split()  # separate seeds into list

    try:
        seed_map = map(int, seed_list_input)  # generate a list of seeds as integers

        if len(seed_list_input) < 1:
            return [0]

        else:
            print('Seed(s) accepted...')
            return list(seed_map)

    except ValueError:
        print('Error: seed(s) must be an integer')
        retry = get_seeds()
        return retry


# Write a basic  config file for AutoDock Vina - ligands, receptors, outputs, seed (0), grid size and coordinates.
def config_writer(ligands, receptor_input, coord, box, seeding=0):
    conformations_directory = f'conformations-{seeding}'
    logs_directory = f'logs-{seeding}'
    file_name = f'{ligands[:-6]}-vina-config-{seeding}.txt'
    receptor_file = receptor_input
    ligand_file = ligands
    output_file = f'{conformations_directory}/{ligands[:-6]}-vina-{seeding}.pdbqt'
    log_file = f'{logs_directory}/{ligands[:-6]}-vina-log-{seeding}.txt'

    # Check for existing and generate directories for docking files and logs
    if conformations_directory not in os.listdir():
        os.mkdir(conformations_directory)
        print('confirmations directory created')

    if logs_directory not in os.listdir():
        os.mkdir(logs_directory)
        print('logs directory created')

    else:
        print('Directories already present')

    # Generate the config file using inputs
    with open(file_name, 'w') as config:

        config.write(f'receptor = {receptor_file}\n'  # receptor file
                     f'ligand = {ligand_file}\n\n'  # ligand file
                     f'center_x = {coord[0]}\n'  # grid coordinates for box
                     f'center_y = {coord[1]}\n'
                     f'center_z = {coord[2]}\n\n'
                     f'size_x = {box[0]}\n'  # box size  
                     f'size_y = {box[1]}\n'
                     f'size_z = {box[2]}\n\n'
                     f'out = {output_file}\n'  # Docking confirmation output
                     f'log = {log_file}\n\n'  # Log file output
                     f'seed = {seeding}'
                     )

        file_names.append(file_name)  # append file name to list for automatic docking


# Run Script
if __name__ == '__main__':
    file_names = []  # Empty list for names of config files
    ligand_list = get_ligands()  # Generate a list of ligand files
    receptor = get_receptor()  # Receive file name of receptor
    coordinates = get_coords()  # Receive co-ordinates of box in format x y z
    box_size = get_box_size()  # Receive box size in format x y z
    seed_list = get_seeds()

    # Generate config files for AutoDock Vina
    [config_writer(x, receptor, coordinates, box_size, seeding=y) for y in seed_list for x in ligand_list]

    print(file_names)

    # Run AutoDock Vina using generated config files list
    [os.system(f'vina --config {config}') for config in file_names]
