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
    print(fpartitionline[:4])
    if "<" not in fpartitionline:
        fpartitioncode = fpartitionline[0:6].replace("  ","00").replace(" ","0")
        if fpartitioncode.strip() != "":
            print(fpartitioncode)
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
footer = lines[-1:]  # Last line (HTML footer)
data_lines = lines[15:-1]  # Everything in between (data rows)

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
                     print(efile)

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
                     #print(x)
                     #print(y)

                     # Convertir listas a numpy arrays
                     x = np.array(x, dtype=float)
                     y = np.array(y, dtype=float)
                     x = np.log10(x)
                     y = np.log10(y)

                     # Extract lg(Q) values from the partition line
                     print(fpartitionline)
                     temp_labels = [300.0, 225.0, 150.0, 75.0, 37.5, 18.75, 9.375]
                     partition_values = fpartitionline[37:].split()[1:]
                     partition_array = np.array([float(val) if val != '---' else None for val in partition_values])
                     print(partition_array)

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
