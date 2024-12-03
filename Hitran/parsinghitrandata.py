#! /usr/bin/env python


""" This is a script to convert the information retrieved by using HAPI from HITRAN
    into a format similar to the one used by CDMS and JPL.
    In order to achieve that, we work on the downloaded data stored under the local
    directory called data. This information has been downloaded by another script in
    this packaged called linebyline.py.
    This script goes through each of the data files downloaded with the previous script,
    copy them into a .cat file with the needed fields in the adequated format.
    More information about the formats is provided in the README.

    Initial development Jul24 by Eduardo Toledo Romero.
"""

__author__ = "Eduardo Toledo Romero"
__license__ = "MIT License"
__version__ = "0.0.1"
__maintainer__ = "Eduardo Toledo Romero"
__email__ = "etoledo@cab.inta-csic.es"

from pathlib import Path
import re
import math
import requests
import bs4

# Constantes físicas
h = 6.62607015e-34  # Constante de Planck en J·s
c = 2.99792458e8    # Velocidad de la luz en m/s
kB = 1.380649e-23   # Constante de Boltzmann en J/K
Ia = 1.0            # Interim solution

# URL used to get the metadata from HITRAN
url = "https://hitran.org/docs/iso-meta/";

# Function to get the relationship between the name of the molecule and the
# local id and the global id to generate the output file name. 
def get_globalid():
    # Dictionary to store the result
    molecules_dict = {}

    # Firstly, we get a list of the molecules from the headers
    req = requests.get(url);
    soup = bs4.BeautifulSoup(req.text, 'html.parser');
    molheaders = soup.find_all("h4");
    # Extracting all the tables in the url provided
    tables = soup.find_all("table");

    for molheader, table in zip(molheaders, tables):
        molecule_formula = molheader.text.strip()
        print(molecule_formula)
        for row in table.find_all('tr'):
            cols = row.find_all('td')

            if len(cols) == 0:
                continue
            # Extract globalid and localid
            globalid = cols[0].text.strip()
            localid = cols[1].text.strip()

            clean_formula = molecule_formula.split(": ")[-1]
            key = f"{clean_formula}_{localid}"
            molecules_dict[key] = globalid

    return molecules_dict

# Small interface to interrogate the above dictionary
def find_value_for_key(key):
    molecules_dict = get_globalid()
    return molecules_dict.get(key, "Key not found")

# Function to find all the files with a specific file extension in a specific
# directory. It makes use of the pathlib functionality from the Path library.
def find_files_with_extension(directory, extension):
    path = Path(directory)
    files = list(path.rglob(f'*{extension}'))
    return files

# Function to limit the force the length of the frequency
#def format_value_with_limited_decimals(value, total_length=13):
def format_value_with_limited_decimals(value, total_length):
    """
    Formatea el valor para que ocupe un máximo de total_length caracteres,
    ajustando los decimales según sea necesario.
    """
    # Convertir el valor a una cadena para contar la parte entera
    integer_part = str(int(value))
    max_decimals = total_length - len(integer_part) - 1  # 1 para el punto decimal

    # Si max_decimals es negativo, significa que el entero ya excede el total_length
    if max_decimals < 0:
        raise ValueError("El valor entero es demasiado grande para el formato especificado")

    # Formatear el valor con los decimales calculados
    format_string = f'{{:.{max_decimals}f}}'
    formatted_value = format_string.format(value)

    # Truncar si excede el total_length por un redondeo adicional
    if len(formatted_value) > total_length:
        formatted_value = formatted_value[:total_length]

    return formatted_value

'''
    Function to treat each of the variable types found in the Hitran data format
    those variables are correspondent to those originary for C/FORTRAN:
    A --> String
    F --> Floating point
    E --> Exponential
    I --> Integer
    We can also have a chain of integers with a defined lenght --> 6I1.
    The script returns a dictionary with the pairs field, value for every line. 
'''
def parse_fixed_width(line, field_formats):
    parsed_data = []
    current_pos = 0

    for field_name, field_format in field_formats:
        if 'I' in field_format:
            parts = field_format.split('I')
            if len(parts) == 2 and parts[0] and parts[1]:
                num_fields = int(parts[0])
                field_length = int(parts[1])
                total_length = num_fields * field_length
                field_data = line[current_pos:current_pos + total_length]
                for i in range(num_fields):
                    single_data = field_data[i*field_length:(i+1)*field_length].strip()
                    parsed_data.append((f"{field_name}_{i+1}", int(single_data) if single_data else 0))
                current_pos += total_length
                continue
            else:
                field_length = int(parts[1])
        elif 'F' in field_format or 'E' in field_format:
            field_length = int(field_format[1:field_format.index('.')])
        elif 'A' in field_format:
            field_length = int(field_format[1:])
        else:
            raise ValueError(f"Unknown field format: {field_format}")

        field_data = line[current_pos:current_pos + field_length].strip()

        if 'F' in field_format or 'E' in field_format:
            field_data = float(field_data) if field_data else 0.0
        elif 'I' in field_format:
            field_data = int(field_data) if field_data else 0
        else:
            # 'A' format remains as string
            pass

        parsed_data.append((field_name, field_data))
        current_pos += field_length
    return dict(parsed_data)


'''
    Create a function to return the value of the degree of freedom of the molecule depending on its formula. 
    As a first iteration we use an approximation as follows:
        0 for atoms
        2 for diatomic molecules
        3 for the others
    Further down the line a dictionary of molecules and their linearility will be implemented.
'''
def get_degree_freedom(input_file):
    molecule_name = str(file)[:-5];
    molecule_name = molecule_name.split('/')[-1]
    elements = re.findall(r'[A-Z][a-z]?', molecule_name);

    if len(elements) == 1:
        degree_freedom = 0;
    elif len(elements) == 2:
        degree_freedom = 2;
    else:
        degree_freedom = 3;

    return degree_freedom;

'''
    Create a function to return the parameter n, related to the linearility of the molecule
    in order to convert the intensity from the HITRAN format to a format more aligned with
    CDMS/JPL standards. 
    As a first approach until the dictionary of linearility of molecules is built, we are
    implementing the following rule:
        Atomic and diatomic molecules n=1
        The others n=3/2 
'''
def get_n(input_file):
    molecule_name = str(file)[:-5];
    molecule_name = molecule_name.split('/')[-1]
    elements = re.findall(r'[A-Z][a-z]?', molecule_name);

    if len(elements) == 1 or len(elements) == 2:
        n = 1;
    else:
        n = 3/2;

    return n;

'''
    Create a function to generate the degree of freedom for each of the molecules 
    in HITRAN. This function is just an approximation, it needs to be further
    developed. This is the currrent approximation (July 2024). 
    0 --> atoms
    2 --> linear molecules
    3 --> non linear molecules
'''

# Dictionary to handle the values of the uncertainity
uncertainity = {
    '0': 1,
    '1': 1,
    '2': 0.1,
    '3': 0.01,
    '4': 0.001,
    '5': 0.0001,
    '6': 0.00001,
    '7': 0.000001,
    '8': 0.0000001,
    '9': 0.00000001 
}

# Define the field formats based in the information provided in the HITRAN webpage
field_formats = [
    ('Molecule ID', 'I2'),          # I2
    ('Isotopologue ID', 'I1'),      # I1
    ('ν', 'F12.6'),                 # F12.6
    ('S', 'E10.3'),                 # E10.3
    ('A', 'E10.3'),                 # E10.3
    ('γair', 'F5.4'),               # F5.4
    ('γself', 'F5.3'),              # F5.3
    ('E"', 'F10.4'),                # F10.4
    ('nair', 'F4.2'),               # F4.2
    ('δair', 'F8.6'),               # F8.6
    ('Global upper quanta', 'A15'), # A15
    ('Global lower quanta', 'A15'), # A15
    ('Local upper quanta', 'A15'),  # A15
    ('Local lower quanta', 'A15'),  # A15
    ('Error indices', '6I1'),       # 6I1
    ('References', '6I2'),          # 6I2
    ('Line mixing flag', 'A1'),     # A1
    ('g\'', 'F7.1'),                # F7.1
    ('g"', 'F7.1')                 # F7.1
]

# Fields to extract with their output formats
#fields_to_extract_with_format = {
    #'ν': '{:13.4f}',
    #'ν': '{<13}',
    #'Error indices_1': '{:<8.5f}',
    #'S': '{:8.4f}',
    #'Degree of Freedom': '{:2d}',
    #'E"': '{:8.4f}',
    #'g\'': '{:>03d}',
    #'Molecule ID': '{:7d}',
    #'Quantum Numbers': '{:04d} {:02d}{:02d}{:02d}{:02d}{:02d}{:02d} {:02d}{:02d}{:02d}{:02d}{:02d}{:02d}'
#}

fields_to_extract_with_format = {
    'ν': '{:>13.4f}',            # F13.4
    'Error indices_1': '{:>8.4f}', # F8.4
    'S': '{:>8.4f}',              # F8.4
    'Degree of Freedom': '{:>2d}', # I2
    'E"': '{:>10.4f}',            # F10.4
    #'g\'': '{:>03d}',             # I3
    'g\'': '{:>04d}',             # I4
    'Molecule ID': '{:>7d}',      # I7
    'Quantum Numbers': '{:>04d} {:>02d}{:>02d}{:>02d}{:>02d}{:>02d}{:>02d} {:>02d}{:>02d}{:>02d}{:>02d}{:>02d}{:>02d}'
}


# Order of fields to extract, including the hardcoded fields in their specific positions
fields_to_extract = [
    'ν',
    'Error indices_1',
    'S',
    'Degree of Freedom',  # Insert Degree of Freedom after 'S'
    'E"',
    'g\'',
    'Molecule ID',
    'Quantum Numbers'  # Insert Quantum Numbers after 'Molecule ID'
]

'''
    Create a function to convert the intensity from HITRAN into the intensity used in
    CDMS and JPL.
    As a first approximation we use the point 5. Approximate Temperature adjustment 
    provided here: https://hitran.org/docs/jpl-cdms-conversion/ 
'''
def transform_S(S, E_double_prime, n):
    #T_ref = 296.0  # Reference temperature in K
    #T_new = 300.0  # New temperature in K
    #factor = (T_new / T_ref) ** (n + 1)
    #exponent = math.exp(((-h * c * E_double_prime) / kB) * ((1 / T_new) - (1 / T_ref)))
    #I = S * (2.99792458e18 / Ia) / exponent / factor
    tr = (S * 2.99792458e18) / (Ia * (300/296)**(n+1) * math.exp(-(h * c * E_double_prime / kB) * (1/300 - 1/296)))
    I = math.log10(tr)
    #print(f"Intermediate Values -> factor: {factor}, exponent: {exponent}, I: {I}")
    return I

directory = 'data/'
extension = '.data'


# We go through all the .data files in the directory /data and all its subdirectories
files = find_files_with_extension(directory, extension)
for file in files:
    print(file)
    subdirectory = file.parent.name
    print(subdirectory)
    file_globalid = find_value_for_key(file.parent.name)
    print(file_globalid)
    file_globalid_str = str(file_globalid)
    file_globalid_padded = file_globalid_str.zfill(6)
    # Value to convert the transition wavenumber (cm-1) into frequency (MHz)
    nu_multiplication_factor = 29979.2458
    #nu_multiplication_factor = 2.99792458E10
    input_file = file

    #Naming the output file with the CDMS extension
    output_file = str(file.parent) + '/' + 'c' + file_globalid_padded + '.cat' 
    print(output_file)

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        print('Populando el fichero de salida')
        for line in infile:
            parsed_data = parse_fixed_width(line, field_formats)
            selected_data = []

            # Add hardcoded value for quantum numbers
            quantum_numbers = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            parsed_data['Quantum Numbers'] = quantum_numbers

            # Add value for degree of freedom
            parsed_data['Degree of Freedom'] = get_degree_freedom(input_file)

            # Add value for molecule id
            parsed_data['Molecule ID'] = int(file_globalid)

            for field in fields_to_extract:
                if field in parsed_data:
                    value = parsed_data[field]
                    if field == 'Quantum Numbers':
                        selected_data.append(fields_to_extract_with_format[field].format(*value))
                    else:
                        if field == 'g\'':
                            g_value = int(value)
                            formatted_g_value = fields_to_extract_with_format[field].format(g_value)
                            selected_data.append(formatted_g_value)
                        elif field == 'Error indices_1':
                            key = int(value)
                            uncertainity_value = uncertainity.get(str(key), None)
                            formatted_value = fields_to_extract_with_format[field].format(uncertainity_value)
                            selected_data.append(formatted_value)
                        elif field == 'S':
                            # Transform S using the provided formula
                            E_double_prime = parsed_data['E"']
                            n = get_n(input_file)
                            transformed_S = transform_S(value, E_double_prime, n)
                            formatted_S = fields_to_extract_with_format[field].format(transformed_S)
                            selected_data.append(formatted_S)
                        elif field == 'ν':
                            value *= nu_multiplication_factor
                            formatted_value = format_value_with_limited_decimals(value, 13)
                            selected_data.append(formatted_value)
                        else:
                            selected_data.append(fields_to_extract_with_format[field].format(value))
                else:
                    selected_data.append(' ')

            #outfile.write(' '.join(selected_data) + '\n')
            outfile.write(''.join(selected_data) + '\n')
