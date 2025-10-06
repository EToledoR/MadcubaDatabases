import requests
import bs4
import pandas as pd
import numpy as np
import periodictable
import re
import os
import math

# URLs we use to get the tabular information needed to obtain the hitran database
url = "https://hitran.org/docs/iso-meta/"
url2 ="https://hitran.org/lbl/2?1=on&2=on&3=on&4=on&5=on&6=on&7=on&8=on&9=on&10=on&11=on&12=on&13=on&14=on&15=on&16=on&17=on&18=on&19=on&20=on&21=on&22=on&23=on&24=on&25=on&26=on&27=on&28=on&29=on&31=on&32=on&33=on&34=on&36=on&37=on&38=on&39=on&40=on&41=on&43=on&44=on&45=on&46=on&47=on&48=on&49=on&50=on&51=on&52=on&53=on&54=on"

# Code to retrieve the molecules
molecules = []
req1 = requests.get(url)
soup1 = bs4.BeautifulSoup(req1.text, 'html.parser')
molheaders = soup1.find_all("h4")
for molheader in molheaders:
    molecules.append(molheader.text.strip())

# Code to retrieve all the tables in the url provided
req = requests.get(url)
soup = bs4.BeautifulSoup(req.text, 'html.parser')
tables = soup.find_all("table")

# Populate a list with all the information in the different tables in the url provided
data = []
for table in tables:
    for row in table.find_all('tr'):
       cols = row.find_all('td')

       # Extracting the table headers
       if len(cols) == 0:
           cols = row.find_all('th')

       cols = [ele.text.strip() for ele in cols]
       data.append([ele for ele in cols if ele])  # Get rid of empty values

# Preparing the pandas dataframe
headers = data.pop(0) # Removing the headers for the tables
df = pd.DataFrame(data, columns=headers)
#print(df)

# Temporary drop of the lines of certain molecules
excluded = ['86','126','127','128','96','136'] # Exclusions by June 2024
for e in excluded:
    i = df.loc[df['global ID'] == e].index
    df = df.drop(i)

# Filtering duplicated headers and unneeded columns
filtered_df = df[df['Formula'] != 'Formula']
filtered_df = filtered_df.drop(filtered_df.columns[[4,5,6,8]], axis=1)
#print(filtered_df)

# Creating a second df with the AFGL codes and the number of lines per molecule
req2 = requests.get(url2)
soup2 = bs4.BeautifulSoup(req2.text, 'html.parser')
tables2 = soup2.find_all("table")

# Populate a list with all the information in the different tables in the url provided
data2 = []
for table in tables2:
    for row in table.find_all('tr'):
       cols = row.find_all('td')

       # Extracting the table headers
       if len(cols) == 0:
           cols = row.find_all('th')

       cols = [ele.text.strip() for ele in cols]
       data2.append([ele for ele in cols if ele])  # Get rid of empty values

# Preparing the pandas dataframe
headers2 = data2.pop(0) # Removing the headers for the tables
df2 = pd.DataFrame(data2, columns=headers2)
#print(df2)

# Temporary drop of the lines of certain molecules
exclude = ['6'] # Exclusion list by June 2024
for el in exclude:
    j = df2.loc[df2['AFGL Code'] == el].index
    df2 = df2.drop(j)

# Filtering duplicated headers and unneeded columns
filtered_df2 = df2[df2['Formula'] != 'Formula']
filtered_df2 = filtered_df2.drop(filtered_df2.columns[[0,3,5,6,7,8]], axis=1)

# Combining both data frames into one and creating a list of molecules list from i
df_combined = pd.merge(filtered_df, filtered_df2, on='Formula', how='left')
list_combined_df = df_combined.values.tolist()

# Creating the header of the partition function file
header = "{:<6} {:<23} {:<39} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} \n".format(
    " tag", "molecule", "lines", "lg(Q(1000))", "lg(Q(500))", "lg(Q(300))", "lg(Q(150))", "lg(Q(75))", 
    "lg(Q(37.5))", "lg(Q(18.75))", "lg(Q(9.375))", "lg(Q(5))", "lg(Q(2.725))")
separator = "=" * 165 + "\n"

# Function to download all the qfiles locally to calculate the partition sum for each molecule
def get_qfiles():
    for molecule in list_combined_df:
        q_file ="https://hitran.org/data/Q/q"+molecule[0]+".txt"
        output_directory = 'Qfiles/'
        os.makedirs(output_directory, exist_ok=True)
        # Create a file path by joining the directory name with the desired file name
        file_path = os.path.join(output_directory, 'q'+molecule[0]+".txt")
        r = requests.get(q_file, allow_redirects=True)
        with open(file_path, 'wb') as output:
            output.write(r.content)

get_qfiles()

# Function for linear interpolation
def interpolate(x, x0, y0, x1, y1):
    return y0 + (y1 - y0) * ((x - x0) / (x1 - x0))

# Prepare the content to be included in the <pre> tag
content = header + separator
for molecule in list_combined_df:
    qfile = open('Qfiles/q'+molecule[0]+'.txt', 'r')
    Lines = qfile.readlines() # Buffer to read the lines
    values = []
    for line in Lines[0:1500]:
        temp = line.split()
        values.append(temp)

    # We create a dictionary from the previous list
    values_dict = {}
    for pair in values:
        key = int(float(pair[0]))
        value = float(pair[1].replace(',', '.'))
        values_dict[key] = value

    # List of temperatures to calculate the partition sum
    temp_list = [1000,500,300,225,150,75,37.5,18.75,9.375,5,2.725]
    temp_frac_list = [37.5,18.75,9.375,2.725]

    q_str = ""
    for T in temp_list:
        if T in temp_frac_list:
            lower_key = math.floor(T)
            upper_key = math.ceil(T)
            if lower_key in values_dict and upper_key in values_dict:
                lower_value = values_dict[lower_key]
                upper_value = values_dict[upper_key]
                q_str += "   " + "{:.4f}".format(math.log10(float(interpolate(T, lower_key, lower_value, upper_key, upper_value))))
                #q_str += "   " + "{:.4E}".format(math.log10(float(interpolate(T, lower_key, lower_value, upper_key, upper_value))))
        else:
            if T in values_dict:
                q_str += "   " + "{:.4f}".format(math.log10(float(values_dict[T])))
                #q_str += "   " + "{:.4E}".format(math.log10(float(values_dict[T])))

    q_values = q_str.split()
    line_str = "{:>6} {:>23} {:>39} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} {:<12} \n".format(
        molecule[0], molecule[2], molecule[6], q_values[0], q_values[1], q_values[2], q_values[3], q_values[4], 
        q_values[5], q_values[6], q_values[7], q_values[8], q_values[9])
    content += line_str

# Creating the HTML file
html_content = f"""<!DOCTYPE html>
<html lang="en"><head>
<body>
<main>
<small>
<pre>
{content}
</pre>
</small>
</main>
</body>
</html>
"""

with open("partition_function_generated.html", "w") as file:
    file.write(html_content)
