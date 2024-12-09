# MadcubaDatabases

## Introduction
This repository aims to hold all the tools needed to populate the software MADCUBA (https://cab.inta-csic.es/madcuba/) and provide an overview in the process needed to regenerate the MADCUBA database.

At the end of the README further insights would be provided to help with the inclusion of new databases.

These instructions are aimed to be run in a Linux or Linux-based(Mac OS) environment. 

## Content
- README.md
- BigLovasOriginal.txt
- SmallLovasOriginal.txt
- SmallLovasOriginal_2003.txt
- CDMS
    - getCDMS.sh
    - modificados.txt
    - hfscatalog_search.sh
    - hfscatalog_createpartitionfile.ipynb
    - correctpartition.py
    - checkpartition.py
- Hitran
    - partitionfunctiontohtml.py
    - linebyline.py
    - parsinghitrandata.py
    - movefiles.py
 - JPL
    - getJPL.sh
    - modificados.txt
    - c017009.cat
- LSD
    - getLILLE.ipynb

## Datasets included
At the moment of writing the first version of this README we are populating the databases with the following data sets:

- **JPL (Jet Propulsion Laboratory) molecular spectroscopy catalog**
    - [https://spec.jpl.nasa.gov/](https://spec.jpl.nasa.gov/)
- **CDMS (The Cologne Database for Molecular Spectroscopy)**
    - [https://cdms.astro.uni-koeln.de](https://cdms.astro.uni-koeln.de)
- **Lille Spectroscopy Database Project**
    - [https://lsd.univ-lille.fr/](https://lsd.univ-lille.fr/)
- **Hitran (High Resolution Transmission molecular absortion) catalog**
    - [https://hitran.org/](https://hitran.org/)
- **Lovas (Frank J. Lovas), Observed Interstellar Molecular Microwave transitions**
    - [https://www.nist.gov/pml/observed-interstellar-molecular-microwave-transitions](https://www.nist.gov/pml/observed-interstellar-molecular-microwave-transitions)

## Procedure
In order to be processed by MADCUBA this directory structure as it is displayed in the beginning of this README document needs to be replicated locally in the computer where you are running the MADCUBA database update. There should be an "umbrella directory" something like: /home/user/dbMADCUBA and underneath the directory structure presents here with all the files needed. 

The steps provided aiming to rerun the process without any need to clean or prepare the directory. The scripts will check for incremental changes in the datasets and update accordingly the needed files.

The files needed to process the data for the Lovas' databases are static and provided in this directory, there is nothing further to be done with them and the MADCUBA codebase is ready to ingest the files as they are.

The order in which the datasets are retrieved does not affect the generation of the database in MADCUBA, the order provided in this README document is purely done to compile all the steps and give the person reading it a sense about how to to use the scripts and other tools in this README. 

### Step 1 - JPL
For JPL you just need to run the bash script getJPL.sh (you need to ensure beforehand that the script has execution permissions using the command chmod). 
The execution of that script will create the following directory structure inside the JPL directory:

- JPL
    - catdir.cat
    - catalog
        - *.cat files

A catdir.cat that is the partition function file with all the information related to the partition function at different temperatures for the species in the catalog. 
A catalog directory with all the cat files for each of the species in the catalog. 

Once this data is populated is time to manually execute all the changes compiled in the modificados.txt file. On that txt file are a series of steps that needs to be executed to correct typos or misplacement in both the partition function file and some of the cat files. At the end of this file there is a section of SOLVED ISSUES that is kept for historical reasons. 

### Step 2 - LSD
By executing the jupyter notebook named getLILLE.ipynb we got in this order:

- A file named entries (a JSON object description).
- If we already had an entries files (from a previous database update) an entries.bck file.
- A series of *.cat.zip files, files with different information for each of the species.
- A catalog directory with the content expanded from the previous zip files. For each species we will have a .cat, .bib, and .txt file
- Also in the catalog directory a series of plots to help reviewing the partition function data retrieved.
- And outside of the catalog folder a partition function file generated with the data unzipped from the previous steps.

- LSD
    - *.cat.zip files
    - entries
    - entries.bck
    - getLILLE.ipynb
    - partition_function.html
    - catalog
        - *.cat
        - *.bib
        - readme_*.txt

In the case of LSD there is no need to add manual steps once the data is generated and ready in the directory.

### Step 3 - CDMS


### Step 4 - Hitran
