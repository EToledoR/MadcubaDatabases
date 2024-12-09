import sys
import os
import wget  # requires pip install wget
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# Sanity check: Verificar monotonía decreciente
def check_monotonicity(values, line_number):
    """
    Check that an array in monotonically decreasing and replace the
    values breaking the monotony by a None to be replaced once more
    by interpolation at a later stage.

    parameters:
    values: array with the partition function values to evaluate
    line number: string with the id of the line for further reference

    return:
    corrected_values: an array with the partition function values that
        follow monotony and None in the ones breaking it. 
    violations: an array with the lines that has monotony violations on
        it.
    """
    corrected_values = values.copy()
    violations = []

    # Clean non numerical values
    cleaned_values = [
        (i, v) for i, v in enumerate(corrected_values) if v not in [None, '---', np.nan]
    ]

    # Extract vlid values and their indeces
    valid_indices, valid_values = zip(*cleaned_values) if cleaned_values else ([], [])

    # Check monotony
    for i in range(1, len(valid_values)):
        if valid_values[i] > valid_values[i-1]:  # Broken monotony
            violations.append(valid_indices[i])
            corrected_values[valid_indices[i]] = None  # Creating a gap

    return corrected_values, violations

fpartition = open('partition_function.html',"r")
fpartitionlines = fpartition.readlines()
fpartition.close()

# Create a directory to storage the efiles in case 
# it already doesn't exsists
if not os.path.isdir('catalog_partitioncorrection'):
    os.mkdir('catalog_partitioncorrection')

# Read the entire partition file
# And split it header, content and footer
# to generate the new partition file.
with open('partition_function.html', 'r') as infile:
    lines = infile.readlines()

# Loop to get all the efiles for the species in the partition
# function file
for fpartitionline in fpartitionlines[15:]:
    if "<" not in fpartitionline:
        fpartitioncode = fpartitionline[0:6].replace("  ","00").replace(" ","0")
        if fpartitioncode.strip() != "":
            filepath = f'./catalog_partitioncorrection/e{fpartitioncode}.cat'
            if not os.path.exists(filepath):
                downloadedfilename = wget.download(
                    f'https://cdms.astro.uni-koeln.de/cgi-bin/cdmsinfo?file=e{fpartitioncode}.cat', 
                      out=filepath
                )
            else:
                print(f"File {filepath} already exists. Skipping download.")


# Separate the HTML structure
header = lines[:15]  # First 15 lines (HTML header and column headers)
footer = lines[-5:]  # Last lines (HTML footer)
data_lines = lines[15:-5]  # Everything in between (data rows)

# Prepare the output file
with open('check_partition_function.html', 'w') as outfile:
    # Write the header first
    outfile.writelines(header)

    x_new=np.array([300.0,225.0,150.0,75.0,37.5,18.75,9.375])
    x_new=np.log10(x_new)

    # Variables declaration to manage the data for each molecule
    sanity_check_violations = []
    complete_array = []
    complete = 0

    # Lista para almacenar los tags que superan el umbral
    tags_exceeding_threshold = []
    threshold = 5.0  # Umbral en porcentaje

    # LOOP HERE
    # Eduardo Toledo 2 Dec 2024
    # Process each line in the original partition file
    for fpartitionline in fpartitionlines[15:]:
        #if "<" not in fpartitionline:
         if not fpartitionline.startswith("<"):
             tag = fpartitionline[0:6].replace("  ","00").replace(" ","0")
             if tag.strip() != "":
                 tag = 'e' + tag
                 with open('./catalog_partitioncorrection/%s.cat' %tag, 'r', encoding='latin-1') as efile:

                     x = []
                     y = []
                     counter = 0

                     for lines in efile.readlines():
                         if "Q(" in lines:
                             x =np.append(x,lines.split("Q(")[1].split(")")[0])
                             e_temp = np.append(x,lines.split("Q(")[1].split(")")[0])
                             if ('(' in lines.split("right>")[1].split("<")[0]):
                                 y =np.append(y,lines.split("right>")[1].split(" (")[0])
                             else:
                                 y =np.append(y,lines.split("right>")[1].split("<")[0])

                     # Convert lists to numpy arrays
                     x = np.array(x, dtype=float)
                     y = np.array(y, dtype=float)
                     x = np.log10(x)
                     y = np.log10(y)

                     # Extract lg(Q) values from the partition line
                     temp_labels = [1000.0, 500.0, 300.0, 225.0, 150.0, 75.0, 37.5, 18.75, 9.375, 5.000, 2.725]
                     partition_values = fpartitionline[37:].split()[1:]
                     partition_array = np.array([float(val) if val != '---' else None for val in partition_values])

                     #print(y)
                     #print(x)

                     # First, check for monotony issues and remove them from the array
                     corrected_partition_array, violations = check_monotonicity(partition_array, fpartitionline)
                     if violations:
                         sanity_check_violations.append((fpartitionline.strip(), violations))

                     # Fill gaps with data from the efiles
                     filled_partition_array = corrected_partition_array.copy()
                     for i, val in enumerate(partition_array):
                         if val is None:
                             # Get the temperature value correspondent
                             temp_value = temp_labels[i]
                             # Check if that value exists in the array populated from the efiles.
                             if temp_value in x:
                                 # Get the index from x and therefore from y
                                 idx = x.index(temp_value)
                                 filled_partition_array[i] = y[idx]
                             else:
                                 filled_partition_array[i] = '---'

                     # Make the filled_partition_array a numpy array to play with it
                     filled_partition_array = np.array(
                         [float(val) if val not in [None, '---'] else np.nan for val in filled_partition_array], dtype=np.float64
                     )

                     # Interpolate and extrapolate
                     # Interpolate using PCHIP (monotonic interpolation)
                     if np.any(np.isnan(filled_partition_array)):
                         indices = np.arange(len(filled_partition_array))
                         valid_indices = indices[~np.isnan(filled_partition_array)]
                         valid_values = filled_partition_array[~np.isnan(filled_partition_array)]

                         # PCHIP interpolator (ensures monotony)
                         pchip_interpolator = PchipInterpolator(valid_indices, valid_values, extrapolate=False)
                         interpolated_array = pchip_interpolator(indices)

                         # Handle extrapolation manually
                         first_valid_index = valid_indices[0]
                         last_valid_index = valid_indices[-1]

                         # Extrapolate before the first valid index
                         slope_start = (valid_values[1] - valid_values[0]) / (valid_indices[1] - valid_indices[0])
                         for i in range(first_valid_index):
                             interpolated_array[i] = valid_values[0] + slope_start * (i - first_valid_index)

                         # Extrapolate after the last valid index
                         slope_end = (valid_values[-1] - valid_values[-2]) / (valid_indices[-1] - valid_indices[-2])
                         for i in range(last_valid_index + 1, len(filled_partition_array)):
                             interpolated_array[i] = valid_values[-1] + slope_end * (i - last_valid_index)

                         # Ensure monotonicity for extrapolated values
                         for i in range(1, len(interpolated_array)):
                             if interpolated_array[i] >= interpolated_array[i-1]:  # Broken monotony
                                 interpolated_array[i] = interpolated_array[i-1] - 0.0001 # To be improved (but how?) ET Dec2024

                         filled_partition_array = np.round(interpolated_array, 4)

                     # Creating the line to populate the new partition function file with the corrected values
                     updated_line = (
                         f'{fpartitionline[:38]}'
                         + ''.join([f'{(f"{v:.4f}" if v is not None else "---"):>13}' for v in filled_partition_array])
                         + '\n'
                     )

                     # Calcular diferencias porcentuales y valores coincidentes para temperaturas coincidentes
                     differences = []
                     efile_values_line = []

                     # Convertir e_temp a float para asegurar comparación válida
                     e_temp = np.array(e_temp, dtype=float)

                     # Variable para controlar si algún valor supera el umbral
                     exceeds_threshold = False

                     # Iterar sobre las temperaturas y valores del partition_array
                     for temp, orig in zip(temp_labels[:len(partition_array)], partition_array):
                         # Buscar coincidencias en e_temp
                         if temp in e_temp and orig not in [None, '---', np.nan]:
                             idx = np.where(e_temp == temp)[0][0]  # Índice de la temperatura coincidente en e_temp
                             efile_val = y[idx]  # Valor correspondiente en y (efiles)

                             if efile_val not in [None, '---', np.nan] and orig != 0:
                                 # Calcular diferencia porcentual
                                 diff = ((efile_val - orig) / orig) * 100
                                 differences.append(f"{diff:.1f}%")
                                 efile_values_line.append(f"{efile_val:.4f}")

                                 # Comprobar si supera el umbral
                                 if abs(diff) > threshold:
                                     exceeds_threshold = True
                             elif orig == 0:  # Evitar división por cero
                                 differences.append("INF")  # Diferencia infinita o indicar con un marcador
                                 efile_values_line.append(f"{efile_val:.4f}" if efile_val not in [None, '---', np.nan] else "----")
                             else:
                                 differences.append("----")
                                 efile_values_line.append("----")
                         else:
                             differences.append("----")
                             efile_values_line.append("----")

                     # Si alguna diferencia supera el umbral, guardar el tag
                     if exceeds_threshold:
                         tags_exceeding_threshold.append(tag)

                     # Crear las líneas adicionales
                     difference_line = (
                         f'{"":38}'  # Dejar espacio inicial
                         + ''.join([f'{value:>13}' for value in differences])  # Alinear diferencias porcentuales
                         + '\n'
                     )

                     efile_values_line_formatted = (
                         f'{"":38}'  # Dejar espacio inicial
                         + ''.join([f'{value:>13}' for value in efile_values_line])  # Alinear valores coincidentes de efiles
                         + '\n'
                     )

                     outfile.write(updated_line)
                     outfile.write(fpartitionline)
                     outfile.write(efile_values_line_formatted)
                     outfile.write(difference_line)

    # Write the footer
    outfile.writelines(footer)

    # Mostrar los tags con diferencias superiores al umbral
    if tags_exceeding_threshold:
        print(f"Tags con diferencias superiores al {threshold}%:")
        print(", ".join(tags_exceeding_threshold))
    else:
        print(f"Ningún tag tiene diferencias superiores al {threshold}%.")
