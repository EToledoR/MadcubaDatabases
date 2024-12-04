import sys
import os
import wget  # requires pip install wget
import numpy as np
import matplotlib.pyplot as plt

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

                     # Fill gaps
                     filled_partition_array = partition_array.copy()
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
                         [float(val) if val != '---' else np.nan for val in filled_partition_array], dtype=np.float64
                     )

                     # Interpolate and extrapolate
                     if np.any(np.isnan(filled_partition_array)):
                         indices = np.arange(len(filled_partition_array))

                         # Interpolation when possible
                         interpolated_array = np.interp(
                             indices,  # Índices completos
                             indices[~np.isnan(filled_partition_array)],  # Índices no NaN
                             filled_partition_array[~np.isnan(filled_partition_array)]  # Valores no NaN
                         )

                         # Extrapolation for missing values at the beginning
                         first_valid_index = np.where(~np.isnan(filled_partition_array))[0][0]
                         if first_valid_index > 0:
                             # Use first two valid values to compute slope for extrapolation
                             second_valid_index = np.where(~np.isnan(filled_partition_array))[0][1]
                             slope_start = (
                                 filled_partition_array[second_valid_index] - filled_partition_array[first_valid_index]
                             ) / (second_valid_index - first_valid_index)
                             for i in range(first_valid_index):
                                 interpolated_array[i] = (
                                 filled_partition_array[first_valid_index] - slope_start * (first_valid_index - i)
                             )

                         # Extrapolation for missing values at the end
                         last_valid_index = np.where(~np.isnan(filled_partition_array))[0][-1]
                         if last_valid_index < len(filled_partition_array) - 1:
                             # Use last two valid values to compute slope for extrapolation
                             second_last_valid_index = np.where(~np.isnan(filled_partition_array))[0][-2]
                             slope_end = (
                                 filled_partition_array[last_valid_index] - filled_partition_array[second_last_valid_index]
                             ) / (last_valid_index - second_last_valid_index)
                             for i in range(last_valid_index + 1, len(filled_partition_array)):
                                 interpolated_array[i] = (
                                 filled_partition_array[last_valid_index] + slope_end * (i - last_valid_index)
                             )
                         filled_partition_array = np.round(interpolated_array, 4)

                     if tag == 'e033511':
                         print('After completing the values (after interpolation/extrapolation):', filled_partition_array)

                     # Format the updated line
                     updated_line = (
                         f'{fpartitionline[:24]} '
                         + '  '.join([f'{v:.4f}' if v is not None else '---' for v in filled_partition_array])
                         + '\n'
                     )
                     outfile.write(updated_line)

                     # Genera plots only if they don't exist
                     log_plot_path = f'./catalog_partitioncorrection/{tag}_part_log.png'
                     lin_plot_path = f'./catalog_partitioncorrection/{tag}_part_lin.png'
                     if not os.path.exists(log_plot_path) or not os.path.exists(lin_plot_path):
                         print('plotting')
                         # Plotting the values in logaritmic and linear scale to check them.
                         fit = np.polyfit(x, y ,5)
                         line = np.poly1d(fit)
                         y_new = line(x_new)
                         plt.figure(figsize=[20,14])
                         plt.plot(x, y, "sg-", x_new, y_new, "or")
                         plt.plot(x, line(x))
                         plt.xlabel("log10(T)")
                         plt.ylabel("log10(Q)")
                         plt.title("%s" %tag)
                         plt.savefig('./catalog_partitioncorrection/%s_part_log.png' %tag)
                         #print(10**y_new)
                         #print((10**y_new-10**y)/10**y*100)
                         #plt.gcf().clear()
                         plt.close()
                         plt.plot(10**x, 10**y, "sg-", 10**x_new, 10**y_new, "or");
                         plt.plot(10**x, 10**line(x))
                         plt.xlabel("T")
                         plt.ylabel("Q")
                         plt.title("%s" %tag)
                         plt.savefig('./catalog_partitioncorrection/%s_part_lin.png' %tag)
                         plt.close()

    # Write the footer
    outfile.writelines(footer)
