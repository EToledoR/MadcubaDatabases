import os

with open('partition_function.html', 'r') as infile:
    lines = infile.readlines()

fpartition = open('partition_function.html', "r")
fpartitionlines = fpartition.readlines()
fpartition.close()

# Separate the HTML structure
header = lines[:15]  # First 15 lines (HTML header and column headers)
footer = lines[-5:]  # Last lines (HTML footer)
data_lines = lines[15:-5]  # Everything in between (data rows)

with open('output_partition_function.html', 'w') as outfile:

    # Loop principal
    for fpartitionline in fpartitionlines[15:]:
        if not fpartitionline.startswith("<"):
            tag = fpartitionline[0:6].replace("  ", "00").replace(" ", "0")
            if tag.strip():
                cfile = './catalog_ortho_para/c' + tag + '.cat'
                print(cfile)
                if os.path.isfile(cfile):
                    print("en el loop")
                    # Abre el archivo .out
                    out_file_path = f'./catalog_ortho_para/{tag}.out'
                    if os.path.isfile(out_file_path):
                        with open(out_file_path, 'r', encoding='latin-1') as efile:
                            lines = efile.readlines()
                        partition_values = []  # Lista para la tercera columna
                        record_values = False  # Bandera para empezar a capturar datos

                        # Procesar línea por línea
                        for line in lines:
                            line = line.strip()
                            # Verifica si la línea empieza con '300.000'
                            if line.startswith("300.000"):
                                record_values = True

                            # Si la bandera está activa, procesamos la línea
                            if record_values:
                                parts = line.split()
                                if len(parts) >= 3:  # Asegura que tenga al menos tres columnas
                                    third_column_value = float(parts[2])
                                    partition_values.append(third_column_value)

                        # Imprime o guarda la lista de valores
                        print(f"Valores de la tercera columna para {tag}:", partition_values)

                        # Escribe en un archivo de salida si lo deseas
                        outfile.write(f"{tag}: {partition_values}\n")
