wget -N https://cdms.astro.uni-koeln.de/classic/entries/partition_function.html
cd catalog
wget -r -nH --cut-dirs=2 --no-parent  -N https://cdms.astro.uni-koeln.de/classic/entries/catdir.html
cd ..

cd hfscatalog
wget -r -nH --cut-dirs=2 --no-parent  -A "*hfs.cat*" -N https://cdms.astro.uni-koeln.de/classic/predictions/daten/
wget -r -nH --cut-dirs=3 --no-parent  -A "*hfs.cat*" -N https://cdms.astro.uni-koeln.de/classic/predictions/catalog/
wget -r -nH --cut-dirs=3 --no-parent  -A "*hfs.cat*" -N https://cdms.astro.uni-koeln.de/classic/predictions/catalog/div/
wget -r -nH --cut-dirs=3 --no-parent  -A "*hfs.cat*" -N https://cdms.astro.uni-koeln.de/classic/predictions/catalog/archive/
#wget -A "*_hfs.cat*"
find `pwd` -name '*.cat' | grep -v 'i_hfs' | wc > allhfs.cat
cd ..

cd predictions
wget -r -nH --cut-dirs=2 --no-parent  -N https://cdms.astro.uni-koeln.de/classic/predictions/
cd ..

# TO DOWNLOAD AND CHECK DIFFERENCES? IN CASE IT IS NEEDED
#cd predictionsdaten
#wget -r -nH --cut-dirs=4 --no-parent  -N https://cdms.astro.uni-koeln.de/classic/predictions/daten/
#cd ..





