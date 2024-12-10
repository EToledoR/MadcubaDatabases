# MadcubaDatabases

## Introduction
This repository aims to hold all the tools needed to populate the software MADCUBA (https://cab.inta-csic.es/madcuba/) and provide an overview in the process needed to regenerate the MADCUBA database.

At the end of the README further insights would be provided to help with the inclusion of new databases.

These instructions are aimed to be run in a Linux or Linux-based(Mac OS) environment. 

## Content of the repository
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

The order in which the datasets are retrieved does not affect the generation of the database in MADCUBA, the order provided in this README document is purely done to compile all the steps and give the person reading it a sense about how to to use the scripts and other tools in this README. However follow the order in which the different scripts are presented for each dataset is mandatory, as some of them are dependent on the output of the previous ones. 

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

One of the manual fixes in the modificados text file is to move an old cat file that is no longer in the latest versions of the JPL catalog, c017009.cat. This file is also included in this repository as one of the tools to generate the db.

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

For CDMS we have these scripts:

- getCDMS.sh  A bash script that create the directory structure that will be explained a bit later in this paragraph and download the partition function file and the cat files correspondent.
- modificados.txt  A text file that , as previously in JPL, it contains a series of manual steps in order to fix issues in the partition function file or some of the cat files, mostly typos.
- correctpartition.py A python script that complete the gaps in the partition function file. It retrieves the efiles (a series of html files, one per species with information about it including partition function information), complete possible gaps in the lines of the partition function file and then by interpolation and extrapolation complete all the gaps on the range of temperatures presented in the partition function file. As additional checks the script present a short report at the end of it with the number of lines modify and the reasons why they have been modified and it also generate two files with the ids of the species in each group: monotonyissues.txt, unalteredids.txt. The main output of this script is a file named outfile_partition_file.html.
- checkpartition.py Is another python script, a small alteration of the previous one that generate a fake partition function with four lines per species: the original line from the partition function file that we have downloaded with getCDMS, another line with the data from the efiles in the case that we have them for the specifics temperatures in the partition function, the differences between both of them in percentage, and a forth line that represent the output of the species after filling the gaps and interpolate and extrapolate the missed data. The ouput of this script is a file named check_partition_function.html for review. Additionally and to help with the review, when the script runs there is a little report at the end that highlight the ids of the species that have a biger difference of a threshold (right now, it is the 5%). This script also generate a series of comparative plots stored in the directory catalog_partitioncorrection together with the efiles donwloaded. 

When all these scripts have run, we need to rename the file output_partition_function.html and named it partition_function.html. 
We recommend to make a backup of the original partition function file. 
After this the records and the partition function file are ready to be ingested by MADCUBA. 

This is how the CDMS directory will look after running all the scripts:

- CDMS
  - getCDMS.sh
  - modificados.txt
  - correctpartition.py
  - checkpartition.py
  - hfscatalog_createpartitionfile.ipynb
  - catalog
    - *.cat
  - catalog_hfs
    - *_hfs.cat
  - catalog_partitioncorrection
    - e*.cat
    - *.png
  - hfscatalog
  - predictions

#### Step 3a. CDMS HFS (Hyperfine structure)

The Hyperfine Structure dataset is built together with the CDMS datasets. They are entries from the CDMS database that are representing hyperfine structure transitions for some of the species in the CDMS catalog. 

This catalog is ingested and presented in MADCUBA as totally separated catalog from CDMS, it is called HFSCDMS.

The cat files needed for the generation of the database are obtained in the previous step while running the getCDMS script and they are stored in the hfscatalog. 

We will need a separte partition function file for this dataset, partition_function_hfs.html, to generate it:

- hfscatalog_createpartitionfile.ipynb  A Jupyter notebook that scan the different folders created with the getCDMS script in order to retrieve the information related to hyperfine structure transitions and generate a specific partition function file.

After this the cat files will be in the catalog_hfs and the partition file ready to be ingested by MADCUBA. 

### Step 4 - Hitran





## Additional notes on the management of the db

### Querying the db


## The DBHSLQDBCreate.java class in MADCUBA codebase

## TODO
- Review which are the the files used for the hfs catalog.
