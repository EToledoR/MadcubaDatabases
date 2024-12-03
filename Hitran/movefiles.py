import os
import shutil

# Ruta del directorio principal
data_dir = "./data"
db_user_dir = "./db_user"
html_file_path = "partition_function_generated.html"

def check_and_create_directory(directory):
    if os.path.exists(directory):
        print(f"El directorio {directory} ya existe. Vaciarlo...")
        # Elimina el contenido del directorio
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        print(f"Creando el directorio {directory}...")
        os.makedirs(directory)

def move_files_to_db_user():
    # Verificar si el directorio db_user existe o crear/vaciar
    check_and_create_directory(db_user_dir)

    # Iterar sobre los subdirectorios en /data
    for subdir in os.listdir(data_dir):
        subdir_path = os.path.join(data_dir, subdir)

        if os.path.isdir(subdir_path):
            # Verificar si existe el archivo .cat en el subdirectorio
            cat_files = [f for f in os.listdir(subdir_path) if f.endswith('.cat')]
            if not cat_files:
                print(f"No se encontró archivo .cat en el directorio {subdir_path}.")
                continue

            # Mover los archivos .cat al directorio db_user
            for cat_file in cat_files:
                cat_file_path = os.path.join(subdir_path, cat_file)
                shutil.copy(cat_file_path, db_user_dir)
                print(f"Archivo {cat_file} movido a {db_user_dir}.")

    # Mover el archivo .html y renombrarlo
    if os.path.exists(html_file_path):
        new_html_file_path = os.path.join(db_user_dir, "partition_function.html")
        shutil.copy(html_file_path, new_html_file_path)
        print(f"Archivo HTML movido y renombrado a {new_html_file_path}.")
    else:
        print(f"El archivo HTML {html_file_path} no existe.")

if __name__ == "__main__":
    move_files_to_db_user()
