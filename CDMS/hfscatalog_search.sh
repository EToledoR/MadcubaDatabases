cd catalog_hfs
rm *

# WE TAKE ONLY hfs files, not 3 hfs (c028501_3hfs.cat H13CN)
find ../hfscatalog/daten/ -name "*_hfs.cat" -and -not -name "*i_*.cat" -and -not -name "*_nohfs.cat" | wc
find ../hfscatalog/daten/ -name "*_hfs.cat" -and -not -name "*i_*.cat" -and -not -name "*_nohfs.cat" -exec ln -s {} \;

# Force duplicated  (4 corrected) 
rm c041505_hfs.cat
ln -s ../hfscatalog/daten/CH3CN/CH3CN/gs/c041505_hfs.cat
rm c030501_hfs.cat
ln -s ../hfscatalog/daten/H2CO/H2CO/c030501_hfs.cat
rm c046209_hfs.cat
ln -s ../hfscatalog/daten/H2CS/2019/H2CS/c046209_hfs.cat
rm c061508_hfs.cat
ln -s ../hfscatalog/daten/SiS/c061508_hfs.cat

find ../predictions/ -name "*_hfs.cat" -and -not -name "*i_*.cat" -and -not -name "*_nohfs.cat" | wc
find ../predictions/ -name "*_hfs.cat" -and -not -name "*i_*.cat" -and -not -name "*_nohfs.cat" -exec ln -s {} \;


# Force duplicated  (12 accounted for)
rm c045511_hfs.cat
ln -s ../predictions/catalog/archive/PN/c045511_hfs.cat
rm c046512_hfs.cat
ln -s ../predictions/catalog/archive/FA/13C/c046512_hfs.cat
rm c067502_hfs.cat
ln -s ../predictions/catalog/archive/NCHCCO/c067502_hfs.cat
rm c030512_hfs.cat
ln -s ../predictions/catalog/archive/NO+/c030512_hfs.cat

# Other duplicated from daten
#ln: failed to create symbolic link './c052509_hfs.cat': File exists
#ln: failed to create symbolic link './c052511_hfs.cat': File exists
#ln: failed to create symbolic link './c051501_hfs.cat': File exists
#ln: failed to create symbolic link './c052510_hfs.cat': File exists
#ln: failed to create symbolic link './c099501_hfs.cat': File exists

#This is duplicated but ok
#c045512_hfs.cat -> ../predictions/catalog/archive/FA/main/c045512_hfs.cat
#c029518_hfs.cat -> ../predictions/catalog/archive/H2CNH/main.vers2/c029518_hfs.cat
#en este la web apunta a https://cdms.astro.uni-koeln.de/classic/predictions/pickett/beispiele/AAN/gs/c056507_hfs.cat
# pero es el mismo que este de abajo
# c056507_hfs.cat -> ../predictions/catalog/archive/H2NCH2CN/gs_vers.2/c056507_hfs.cat




# WRONG ENTRIES

# ENTRY c046209_hfs.cat H2CS should be c046509_hfs.cat
mv c046209_hfs.cat c046509_hfs.backup
sed 's/46209/46509/g' c046509_hfs.backup > c046509_hfs.cat
# ENTRY c042201_hfs.cat H2CCO should be c042501_hfs.cat
mv c042201_hfs.cat c042501_hfs.backup
sed 's/42201/42501/g' c042501_hfs.backup > c042501_hfs.cat

mv c044519_hfs.cat c044519_hfs.backup
sed 's/44518/44519/g' c044519_hfs.backup > c044519_hfs.cat
mv c053505_hfs.cat c053505_hfs.backup
sed 's/53502/53505/g' c053505_hfs.backup > c053505_hfs.cat

cd ..
ls catalog_hfs | wc

