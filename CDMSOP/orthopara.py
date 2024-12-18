import os
import requests
import re

# Directorio de destino
output_dir = "./catalog_ortho_para/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

base_url = "https://cdms.astro.uni-koeln.de"

fpartition = open('partition_function.html',"r")
fpartitionlines = fpartition.readlines()
fpartition.close()

# Archivo de salida para moleculas
molecule_files_path = "molecule_files.txt"
with open(molecule_files_path, 'w') as molecule_file:

    # Loop principal
    for fpartitionline in fpartitionlines[15:]:
        if not fpartitionline.startswith("<"):
            tag = fpartitionline[0:6].replace("  ", "00").replace(" ", "0")
            molecule = fpartitionline[6:24]
            if tag.strip():
                tag = 'e' + tag
                with open(f'../CDMS/catalog_partitioncorrection/{tag}.cat', 'r', encoding='latin-1') as efile:
                    lines = efile.readlines()

                if any("ortho" in line for line in lines):
                        for i, line in enumerate(lines):
                            if "Separate" in line:
                                print(f"Procesando {tag}: Encontrado posible ortho y para")

                                # Línea 2 después (para)
                                para_tag_line = lines[i+2]
                                if '<i>' in para_tag_line and 'para' in para_tag_line:
                                    para_url_line = lines[i+1]
                                    para_href = para_url_line.split('href="')[1].split('"')[0]
                                    para_url = base_url + para_href
                                    para_filename = os.path.join(output_dir, para_href.split('/')[-1])

                                    # Descargar archivo .cat para 'para'
                                    print(f"Descargando {para_url} -> {para_filename}")
                                    response = requests.get(para_url)
                                    with open(para_filename, 'wb') as file:
                                        file.write(response.content)
                                    # Contar el número de líneas en el archivo descargado
                                    with open(para_filename, 'r', encoding='latin-1') as file:
                                        num_para_lines = len(file.readlines())

                                # Línea 4 después (ortho)
                                ortho_tag_line = lines[i+4]
                                if '<i>' in ortho_tag_line and 'ortho' in ortho_tag_line:
                                    ortho_url_line = lines[i+3]
                                    ortho_href = ortho_url_line.split('href="')[1].split('"')[0]
                                    ortho_url = base_url + ortho_href
                                    ortho_filename = os.path.join(output_dir, ortho_href.split('/')[-1])

                                    # Descargar archivo .cat para 'ortho'
                                    print(f"Descargando {ortho_url} -> {ortho_filename}")
                                    response = requests.get(ortho_url)
                                    with open(ortho_filename, 'wb') as file:
                                        file.write(response.content)
                                    # Contar el número de líneas en el archivo descargado
                                    with open(ortho_filename, 'r', encoding='latin-1') as file:
                                        num_ortho_lines = len(file.readlines())

                                # Línea 8 (para) y línea 7 (url)
                                # O línea 7 (para) y línea 8 (url)
                                para_out_line = lines[i+8]
                                alt_para_out_line = lines[i+7]
                                alt2_para_out_line = lines[i+6]
                                alt3_para_out_line = lines[i+5]

                                if 'para' in para_out_line:
                                    para_out_url_line = lines[i+7]
                                    print(para_out_url_line)
                                    para_out_href = para_out_url_line.split('href="')[1].split('"')[0]
                                    para_out_url = base_url + para_out_href
                                    para_out_filename = os.path.join(output_dir, para_out_href.split('/')[-1])
                                    para_tag = re.search(r"/c0*(\d+)\.out", para_out_url_line)
                                    para_tag = para_tag.group(1).lstrip("0")

                                    # Descargar archivo .out para 'para'
                                    print(f"Descargando {para_out_url} -> {para_out_filename}")
                                    response = requests.get(para_out_url)
                                    with open(para_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{para_tag} {molecule} {num_para_lines}  {para_out_filename} para\n")

                                if 'para' in alt_para_out_line:
                                    para_out_url_line = lines[i+6]
                                    para_out_href = para_out_url_line.split('href="')[1].split('"')[0]
                                    para_out_url = base_url + para_out_href
                                    para_out_filename = os.path.join(output_dir, para_out_href.split('/')[-1])
                                    para_tag = re.search(r"/c0*(\d+)\.out", para_out_url_line)
                                    para_tag = para_tag.group(1).lstrip("0")

                                   # Descargar archivo .out para 'para'
                                    print(f"Descargando {para_out_url} -> {para_out_filename}")
                                    response = requests.get(para_out_url)
                                    with open(para_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{para_tag} {molecule} {num_para_lines} {para_out_filename} para\n")

                                if 'para' in alt2_para_out_line and 'para' not in alt_para_out_line and 'para' not in para_out_line:
                                    para_out_url_line = lines[i+5]
                                    para_out_href = para_out_url_line.split('href="')[1].split('"')[0]
                                    para_out_url = base_url + para_out_href
                                    para_out_filename = os.path.join(output_dir, para_out_href.split('/')[-1])
                                    para_tag = re.search(r"/c0*(\d+)\.out", para_out_url_line)
                                    para_tag = para_tag.group(1).lstrip("0")

                                    # Descargar archivo .out para 'para'
                                    print(f"Descargando {para_out_url} -> {para_out_filename}")
                                    response = requests.get(para_out_url)
                                    with open(para_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{para_tag} {molecule} {num_para_lines} {para_out_filename} para\n")

                                if 'para' in alt3_para_out_line and 'para' not in alt2_para_out_line and 'para' not in alt_para_out_line and 'para' not in para_out_line:
                                   para_out_url_line = lines[i+4]
                                   para_out_href = para_out_url_line.split('href="')[1].split('"')[0]
                                   para_out_url = base_url + para_out_href
                                   para_out_filename = os.path.join(output_dir, para_out_href.split('/')[-1])
                                   para_tag = re.search(r"/c0*(\d+)\.out", para_out_url_line)
                                   para_tag = para_tag.group(1).lstrip("0")

                                   # Descargar archivo .out para 'para'
                                   print(f"Descargando {para_out_url} -> {para_out_filename}")
                                   response = requests.get(para_out_url)
                                   with open(para_out_filename, 'wb') as file:
                                       file.write(response.content)
                                   molecule_file.write(f"{para_tag} {molecule} {num_para_lines} {para_out_filename} para\n")


                                # Línea 10 (ortho) y línea 9 (url)
                                # O linea 8 (ortho) y linea 9 (url)
                                ortho_out_line = lines[i+10]
                                alt_ortho_out_line = lines[i+9]
                                alt2_ortho_out_line = lines[i+8]
                                alt3_ortho_out_line = lines[i+7]

                                if 'ortho' in ortho_out_line and 'ortho' not in alt_ortho_out_line and 'ortho' not in alt2_ortho_out_line and 'ortho' not in alt3_ortho_out_line:
                                    print("first ortho")
                                    ortho_out_url_line = lines[i+9]
                                    ortho_out_href = ortho_out_url_line.split('href="')[1].split('"')[0]
                                    ortho_out_url = base_url + ortho_out_href
                                    ortho_out_filename = os.path.join(output_dir, ortho_out_href.split('/')[-1])
                                    ortho_tag = re.search(r"/c0*(\d+)\.out", ortho_out_url_line)
                                    ortho_tag = ortho_tag.group(1).lstrip("0")

                                    # Descargar archivo .out para 'ortho'
                                    print(f"Descargando {ortho_out_url} -> {ortho_out_filename}")
                                    response = requests.get(ortho_out_url)
                                    with open(ortho_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{ortho_tag} {molecule} {num_ortho_lines} {ortho_out_filename} ortho\n")

                                if 'ortho' in alt_ortho_out_line and 'ortho' not in alt2_ortho_out_line:
                                    print("second ortho")
                                    ortho_out_url_line = lines[i+8]
                                    ortho_out_href = ortho_out_url_line.split('href="')[1].split('"')[0]
                                    ortho_out_url = base_url + ortho_out_href
                                    ortho_out_filename = os.path.join(output_dir, ortho_out_href.split('/')[-1])
                                    ortho_tag = re.search(r"/c0*(\d+)\.out", ortho_out_url_line)
                                    ortho_tag = ortho_tag.group(1).lstrip("0")

                                    # Descargar archivo .out para 'ortho'
                                    print(f"Descargando {ortho_out_url} -> {ortho_out_filename}")
                                    response = requests.get(ortho_out_url)
                                    with open(ortho_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{ortho_tag} {molecule} {num_ortho_lines} {ortho_out_filename} ortho\n")

                                if 'ortho' in alt2_ortho_out_line:
                                    print("third ortho")
                                    ortho_out_url_line = lines[i+7]
                                    ortho_out_href = ortho_out_url_line.split('href="')[1].split('"')[0]
                                    ortho_out_url = base_url + ortho_out_href
                                    ortho_out_filename = os.path.join(output_dir, ortho_out_href.split('/')[-1])
                                    ortho_tag = re.search(r"/c0*(\d+)\.out", ortho_out_url_line)
                                    ortho_tag = ortho_tag.group(1).lstrip("0")

                                    # Descargar archivo .out para 'ortho'
                                    print(f"Descargando {ortho_out_url} -> {ortho_out_filename}")
                                    response = requests.get(ortho_out_url)
                                    with open(ortho_out_filename, 'wb') as file:
                                        file.write(response.content)
                                    molecule_file.write(f"{ortho_tag} {molecule} {num_ortho_lines} {ortho_out_filename} ortho\n")

                                if 'ortho' in alt3_ortho_out_line and 'ortho' not in alt2_ortho_out_line and 'ortho' not in alt_ortho_out_line and 'ortho' not in ortho_out_line:
                                     print("fourth ortho")
                                     ortho_out_url_line = lines[i+6]
                                     ortho_out_href = ortho_out_url_line.split('href="')[1].split('"')[0]
                                     ortho_out_url = base_url + ortho_out_href
                                     ortho_out_filename = os.path.join(output_dir, ortho_out_href.split('/')[-1])
                                     ortho_tag = re.search(r"/c0*(\d+)\.out", ortho_out_url_line)
                                     ortho_tag = ortho_tag.group(1).lstrip("0")

                                     # Descargar archivo .out para 'ortho'
                                     print(f"Descargando {ortho_out_url} -> {ortho_out_filename}")
                                     response = requests.get(ortho_out_url)
                                     with open(ortho_out_filename, 'wb') as file:
                                         file.write(response.content)
                                     molecule_file.write(f"{ortho_tag} {molecule} {num_ortho_lines} {ortho_out_filename} ortho\n")

