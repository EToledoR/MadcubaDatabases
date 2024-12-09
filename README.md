# MadcubaDatabases

This repository aims to hold all the tools needed to populate the software MADCUBA (https://cab.inta-csic.es/madcuba/). 

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

The order in which the datasets are retrieved does not affect the generation of the database in MADCUBA, the order provided in this README document is purely done to compile all the steps and give the person reading it a sense about how to to use the scripts and other tools in this README. 

