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
with open('output_partition_function.html', 'w') as outfile:
    # Write the header first
    outfile.writelines(header)

    x_new=np.array([300.0,225.0,150.0,75.0,37.5,18.75,9.375])
    x_new=np.log10(x_new)

    # Variables declaration to manage the data for each molecule
    sanity_check_violations = []
    complete_array = []
    complete = 0

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


                     # Check if a line has all the values needed to be ingested in MADCUBA, between 300
                     # and 9.375 If the do, don't process them any further.
                     if all(partition_array[i] not in [None, '---', np.nan] for i in range(2, 9)):
                         complete_array.append(tag)
                         complete += 1
                         outfile.write(fpartitionline)
                     # Otherwise complete the values from the efiles and then interpolate and extrapolate the rest of
                     # values.
                     else:
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

                         outfile.write(updated_line)

                         # Generate plots only if they don't exist
                         log_plot_path = f'./catalog_partitioncorrection/{tag}_part_log.png'
                         lin_plot_path = f'./catalog_partitioncorrection/{tag}_part_lin.png'
                         if not os.path.exists(log_plot_path) or not os.path.exists(lin_plot_path):
                             #print('plotting')

                             # Filter non valid values to plot
                             partition_array_clean = np.array(
                                 [val if val not in [None, '---', np.nan] else np.nan for val in partition_array], dtype=np.float64
                             )
                             filled_partition_array_clean = np.array(
                                 [val if val not in [None, '---', np.nan] else np.nan for val in filled_partition_array], dtype=np.float64
                             )

                             # Filter temperatures and correspondent values
                             valid_partition_indices = ~np.isnan(partition_array_clean)
                             valid_filled_indices = ~np.isnan(filled_partition_array_clean)

                             temp_labels_partition = np.array(temp_labels[:len(partition_array)])[valid_partition_indices]
                             partition_values_clean = partition_array_clean[valid_partition_indices]

                             temp_labels_filled = np.array(temp_labels[:len(filled_partition_array)])[valid_filled_indices]
                             filled_values_clean = filled_partition_array_clean[valid_filled_indices]

                             print(x)
                             print(y)

                             # Polynomic it grade 5
                             fit = np.polyfit(x, y, 5)
                             poly_line = np.poly1d(fit)
                             y_fit_log = poly_line(x)
                             y_fit_lin = poly_line(np.log10(temp_labels[:len(filled_partition_array)]))

                             # Plot log scale
                             plt.figure(figsize=[20, 14])
                             plt.plot(x, y, "sg-", label="Values from efile")
                             plt.plot(np.log10(temp_labels_partition), np.log10(partition_values_clean), "ob-", label="Original partition values")
                             #plt.plot(np.log10(temp_labels_filled), np.log10(filled_values_clean), "xr-", label="Completed values")
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
                             #plt.plot(temp_labels_filled, filled_values_clean, "xr-", label="Completed values")
                             plt.plot(temp_labels[:len(filled_partition_array)], 10**y_fit_lin, "c--", label="Polynomial fit (degree 5)")
                             plt.xlabel("T")
                             plt.ylabel("Q")
                             plt.title(f"Partition Function (Linear Scale) - {tag}")
                             plt.legend()
                             plt.savefig(lin_plot_path)
                             plt.close()


    # Write the footer
    outfile.writelines(footer)

# Generating report of what happened with the data and generating the files 
# with the different issues found.
print("Sanity Check Report:")
print("=====================")
print(f"Total lines with monotonicity issues: {len(sanity_check_violations)}")
with open("monotonyissues.txt", "w") as file:
    for line, indices in sanity_check_violations:
        file.write(line[:32] + "\n")
print("A file named monotonyissues.txt has been generated with these issues.")

print("Hay ",complete, "Ids with a complete partition function array of values valid for MADCUBA.")
with open("unalteredids.txt", "w") as file:
    file.write(", ".join(complete_array))
print("A file named unalteredids.txt has been generated with these ids.")
