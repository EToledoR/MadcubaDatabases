import sys
import os
import wget  # requires pip install wget
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

# Sanity check: Verificar monotonía decreciente
def check_monotonicity(values, line_number):
    """
    Verifica si los valores son monotonamente decrecientes.
    Si no lo son, corrige los valores reemplazando los incorrectos por None.
    """
    corrected_values = values.copy()
    violations = []  # Para registrar los índices que rompen la monotonía

    # Limpiar valores no numéricos
    cleaned_values = [
        (i, v) for i, v in enumerate(corrected_values) if v not in [None, '---', np.nan]
    ]

    if 4.1069 in corrected_values:
        print('Array limpio: ', cleaned_values)
    # Extraer solo los valores válidos y sus índices
    valid_indices, valid_values = zip(*cleaned_values) if cleaned_values else ([], [])

    # Comprobar monotonía decreciente
    for i in range(1, len(valid_values)):
        if valid_values[i] > valid_values[i-1]:  # Monotonía rota
            violations.append(valid_indices[i])
            corrected_values[valid_indices[i]] = None  # Marcamos como hueco


    #for i in range(1, len(values)):
        #if corrected_values[i] is not None and corrected_values[i-1] is not None:
            #if corrected_values[i] > corrected_values[i-1]:  # Monotonía rota
                #violations.append(i)
                #corrected_values[i] = None  # Marcamos como hueco

    return corrected_values, violations

fpartition = open('partition_function.html',"r")
fpartitionlines = fpartition.readlines()
fpartition.close()

if not os.path.isdir('catalog_partitioncorrection'):
    os.mkdir('catalog_partitioncorrection')

# Read the entire partition file
# And split it header, content and footer
# to generate the new partition file.
with open('partition_function.html', 'r') as infile:
    lines = infile.readlines()

# Process each line in the original partition file
for fpartitionline in fpartitionlines[15:]:
    #print(fpartitionline[:4])
    if "<" not in fpartitionline:
        fpartitioncode = fpartitionline[0:6].replace("  ","00").replace(" ","0")
        if fpartitioncode.strip() != "":
            #print(fpartitioncode)
            filepath = f'./catalog_partitioncorrection/e{fpartitioncode}.cat'
            if not os.path.exists(filepath):
                downloadedfilename = wget.download(
                    f'https://cdms.astro.uni-koeln.de/cgi-bin/cdmsinfo?file=e{fpartitioncode}.cat', 
                      out=filepath
                )
            else:
                print(f"File {filepath} already exists. Skipping download.")
        #downloadedfilename=wget.download(
            #'https://cdms.astro.uni-koeln.de/cgi-bin/cdmsinfo?file=e%s.cat' %fpartitioncode, 
            #out='./catalog_partitioncorrection/e%s.cat'%fpartitioncode
        #)

# Separate the HTML structure
header = lines[:15]  # First 15 lines (HTML header and column headers)
footer = lines[-5:]  # Last line (HTML footer)
data_lines = lines[15:-5]  # Everything in between (data rows)

# Prepare the output file
with open('output_partition_function.html', 'w') as outfile:
    # Write the header first
    outfile.writelines(header)

    x_new=np.array([300.0,225.0,150.0,75.0,37.5,18.75,9.375])
    x_new=np.log10(x_new)

    sanity_check_violations = []

    # LOOP HERE
    # Eduardo Toledo 2 Dec 2024
    # Process each line in the original partition file
    for fpartitionline in fpartitionlines[15:]:
        if "<" not in fpartitionline:
             tag = fpartitionline[0:6].replace("  ","00").replace(" ","0")
             if tag.strip() != "":
                 tag = 'e' + tag
                 with open('./catalog_partitioncorrection/%s.cat' %tag, 'r', encoding='latin-1') as efile:
                     #print(efile)

                     x = []
                     y = []

                     for lines in efile.readlines():
                         if "Q(" in lines:
                             #print(lines)
                             x =np.append(x,lines.split("Q(")[1].split(")")[0])
                             if ('(' in lines.split("right>")[1].split("<")[0]):
                                 y =np.append(y,lines.split("right>")[1].split(" (")[0])
                             else:
                                 y =np.append(y,lines.split("right>")[1].split("<")[0])
                     if tag == 'e033511':
                         print('Temps from efile: ',x)
                     #print('Values of Q from efile: ',y)

                     # Convertir listas a numpy arrays
                     x = np.array(x, dtype=float)
                     y = np.array(y, dtype=float)
                     x = np.log10(x)
                     y = np.log10(y)
                     #print('Tag :', tag)
                     if tag == 'e033511':
                         print('Values of log(Q) from the efile: ',y)
                     # Extract lg(Q) values from the partition line
                     #print(fpartitionline)
                     temp_labels = [1000.0, 500.0, 300.0, 225.0, 150.0, 75.0, 37.5, 18.75, 9.375, 5.000, 2.725]
                     partition_values = fpartitionline[37:].split()[1:]
                     partition_array = np.array([float(val) if val != '---' else None for val in partition_values])
                     if tag == 'e033511':
                         print('Values log(Q) from partition file: ',partition_array)
                     #print(y)
                     #print(x)


                     # Correct the partition array from all the violations of monotonicity
                     if tag == 'e033511':
                         print('Checking monotonicity: ', partition_array)
                     corrected_partition_array, violations = check_monotonicity(partition_array, fpartitionline)
                     if violations:
                         sanity_check_violations.append((fpartitionline.strip(), violations))

                     # Fill gaps
                     filled_partition_array = corrected_partition_array.copy()
                     #filled_partition_array = partition_array.copy()
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
                     if tag == 'e033511':
                         print('After completing the values: ', filled_partition_array)

                     # Make the filled_partition_array a numpy array to play with it
                     filled_partition_array = np.array(
                         #[float(val) if val != '---' else np.nan for val in filled_partition_array], dtype=np.float64
                         #[float(val) if val is not None else np.nan for val in filled_partition_array], dtype=np.float64
                         [float(val) if val not in [None, '---'] else np.nan for val in filled_partition_array], dtype=np.float64
                     )

                     # Interpolate and extrapolate
                     # Interpolate using PCHIP (monotonic interpolation)
                     if np.any(np.isnan(filled_partition_array)):
                         indices = np.arange(len(filled_partition_array))
                         valid_indices = indices[~np.isnan(filled_partition_array)]
                         valid_values = filled_partition_array[~np.isnan(filled_partition_array)]

                         # PCHIP interpolator (ensures monotonicity)
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
                             if interpolated_array[i] >= interpolated_array[i-1]:  # Monotonía rota
                                 interpolated_array[i] = interpolated_array[i-1] - 0.0001

                         filled_partition_array = np.round(interpolated_array, 4)

                     if tag == 'e033511':
                         print('After completing the values (after interpolation/extrapolation):', filled_partition_array)

                     # Format the updated line
                     #updated_line = (
                         #f'{fpartitionline[:38]} '
                         #+ '  '.join([f'{v:.4f}' if v is not None else '---' for v in filled_partition_array])
                         #+ '\n'
                     #)
                     updated_line = (
                         f'{fpartitionline[:38]} '
                         + ''.join([f'{(f"{v:.4f}" if v is not None else "---"):>13}' for v in filled_partition_array])
                         + '\n'
                     )
                     outfile.write(updated_line)

                     # Genera plots only if they don't exist
                     log_plot_path = f'./catalog_partitioncorrection/{tag}_part_log.png'
                     lin_plot_path = f'./catalog_partitioncorrection/{tag}_part_lin.png'
                     if not os.path.exists(log_plot_path) or not os.path.exists(lin_plot_path):
                         print('plotting')

                         # Filtrar valores no válidos
                         partition_array_clean = np.array(
                             [val if val not in [None, '---', np.nan] else np.nan for val in partition_array], dtype=np.float64
                         )
                         filled_partition_array_clean = np.array(
                             [val if val not in [None, '---', np.nan] else np.nan for val in filled_partition_array], dtype=np.float64
                         )

                         # Filtrar temperaturas y valores correspondientes
                         valid_partition_indices = ~np.isnan(partition_array_clean)
                         valid_filled_indices = ~np.isnan(filled_partition_array_clean)

                         temp_labels_partition = np.array(temp_labels[:len(partition_array)])[valid_partition_indices]
                         partition_values_clean = partition_array_clean[valid_partition_indices]

                         temp_labels_filled = np.array(temp_labels[:len(filled_partition_array)])[valid_filled_indices]
                         filled_values_clean = filled_partition_array_clean[valid_filled_indices]

                         # Realizar ajuste polinómico de grado 5
                         fit = np.polyfit(x, y, 5)
                         poly_line = np.poly1d(fit)
                         y_fit_log = poly_line(x)
                         y_fit_lin = poly_line(np.log10(temp_labels[:len(filled_partition_array)]))

                         # Plot log scale
                         plt.figure(figsize=[20, 14])
                         plt.plot(x, y, "sg-", label="Values from efile")
                         plt.plot(np.log10(temp_labels_partition), np.log10(partition_values_clean), "ob-", label="Original partition values")
                         plt.plot(np.log10(temp_labels_filled), np.log10(filled_values_clean), "xr-", label="Completed values")
                         plt.plot(x, y_fit_log, "c--", label="Polynomial fit (degree 5)")
                         plt.xlabel("log10(T)")
                         plt.ylabel("log10(Q)")
                         plt.title(f"Partition Function (Log Scale) - {tag}")
                         plt.legend()
                         plt.savefig(log_plot_path)
                         plt.close()

                         # Plot linear scale
                         plt.figure(figsize=[20, 14])
                         plt.plot(10**x, 10**y, "sg-", label="Values from efile")
                         plt.plot(temp_labels_partition, partition_values_clean, "ob-", label="Original partition values")
                         plt.plot(temp_labels_filled, filled_values_clean, "xr-", label="Completed values")
                         plt.plot(temp_labels[:len(filled_partition_array)], 10**y_fit_lin, "c--", label="Polynomial fit (degree 5)")
                         plt.xlabel("T")
                         plt.ylabel("Q")
                         plt.title(f"Partition Function (Linear Scale) - {tag}")
                         plt.legend()
                         plt.savefig(lin_plot_path)
                         plt.close()


                         # Plotting the values in logaritmic and linear scale to check them.
                         #fit = np.polyfit(x, y ,5)
                         #line = np.poly1d(fit)
                         #y_new = line(x_new)
                         #plt.figure(figsize=[20,14])
                         #plt.plot(x, y, "sg-", x_new, y_new, "or")
                         #plt.plot(x, line(x))
                         #plt.xlabel("log10(T)")
                         #plt.ylabel("log10(Q)")
                         #plt.title("%s" %tag)
                         #plt.savefig('./catalog_partitioncorrection/%s_part_log.png' %tag)
                         #print(10**y_new)
                         #print((10**y_new-10**y)/10**y*100)
                         #plt.gcf().clear()
                         #plt.close()
                         #plt.plot(10**x, 10**y, "sg-", 10**x_new, 10**y_new, "or");
                         #plt.plot(10**x, 10**line(x))
                         #plt.xlabel("T")
                         #plt.ylabel("Q")
                         #plt.title("%s" %tag)
                         #plt.savefig('./catalog_partitioncorrection/%s_part_lin.png' %tag)
                         #plt.close()

    # Write the footer
    outfile.writelines(footer)

    print("Sanity Check Report:")
    print("=====================")
    print(f"Total lines with monotonicity issues: {len(sanity_check_violations)}")
    for line, indices in sanity_check_violations:
        print(f"Line: {line}")
        print(f"Indices fixed: {indices}")

