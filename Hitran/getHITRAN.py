
from hapi import *

mol_id = ['1 = H2O','2 = CO2','3 = O3','4 = N2O','5 = CO','6 = CH4','7 = O2',
'8 = NO','9 = SO2','10 = NO2','11 = NH3','12 = HNO3','13 = OH','14 = HF','15 = HCl',
'16 = HBr','17 = HI','18 = ClO','19 = OCS','20 = H2CO','21 = HOCl','22 = N2','23 = HCN',
'24 = CH3Cl','25 = H2O2','26 = C2H2','27 = C2H6','28 = PH3','29 = COF2','31 = H2S',
'32 = HCOOH','33 = HO2','no 34     ','36 = NO+','37 = HOBr','38 = C2H4','39 = CH3OH',
'40 = CH3Br','41 = CH3CN','43 = C4H2','44 = HC3N','45 = H2','46 = CS','47 = SO3','48=C2N2',
'49=COCl2','50=SO','51=CH3F','52=GeH4','53=CS2','54=CH3I','56=C3H4','57=CH3',]

molecules = [' ','H2O   ','CO2   ','O3    ','N2O   ','CO    ','CH4   ','O2    ',
'NO    ','SO2   ','NO2   ','NH3   ','HNO3  ','OH    ','HF    ','HCl   ',
'HBr   ','HI    ','ClO   ','OCS   ','H2CO  ','HOCl  ','N2    ','HCN   ',
'CH3Cl ','H2O2  ','C2H2  ','C2H6  ','PH3   ','COF2  ','H2S   ',
'HCOOH ','HO2   ','O     ','NO+   ','HOBr  ','C2H4  ','CH3OH ',
'CH3Br ','CH3CN ','C4H2  ','HC3N  ','H2    ','CS    ','SO3   ','C2N2  ', 
'COCl2 ','SO    ','CH3F  ','GeH4  ','CS2   ','CH3I   ','C3H4  ','CH3   ']

niso = [0,7,12,5,5,6,4,3,3,4,2,2,2,
3,2,4,4,2,2,6,3,2,3,3,2,1,3,3,1,
2,1,3,1,1,1,2,1,2,3,1,2,4,1,1,6,2,4,1,2,2,3,1,5,4,2,1,1,1]

isotopologue = list()
isotopologue = ['     ',\
#1  H2O
'1=1, 2=2, 3=3, 4=4, 5=5, 6=6, 7=129',\
#2  CO2
' 1=7, 2=8, 3=9, 4=10,  5=11,  6=12,  7=13,  8=14,\
 9=121, 10=15, 11=120, 12=122',
#3  O3
' 1=16, 2=17, 3=18, 4=19, 5=20',
#4  N2O
' 1=21, 2=22, 3=23, 4=24, 5=25',
#5   CO
' 1=26, 2=27, 3=28, 4=29, 5=30, 6=31',
#6   CH4
' 1=32, 2=33, 3=34, 4=35',
#7   O2
' 1=36, 2=37, 3=38',
#8   NO
' 1=39, 2=40, 3=41',
#9   SO2
' 1=42, 2=43, 3=137, 4=138',
#10   NO2
' 1=44, 2=130',
#11   NH3
' 1=45, 2=46',
#12   HNO3
' 1=47, 2=117',
#13   OH
' 1=48, 2=49, 3=50',
#14   HF
' 1=51, 2=110',
#15   HCl
' 1=52, 2=53, 3=107, 4=108',
#16   HBr
' 1=54, 2=55, 3=111, 4=112',
#17   HI
' 1=56, 2=113',
#18   ClO
' 1=57, 2=58',
#19   OCS
' 1=59, 2=60, 3=61, 4=62, 5=63, 6=135',
#20   H2CO
' 1=64, 2=65, 3=66',
#21   HOCl
' 1=67, 2=68',
#22   N2
' 1=69, 2=118',
#23   HCN
' 1=70, 2=71, 3=72',
#24   CH3Cl
' 1=73, 2=74',
#25   H2O2
' 1=75',
#26   C2H2
' 1=76, 2=77, 3=105',
#27   C2H6
' 1=78, 2=106',
#28   PH3
 '1=79',
#29   COF2
' 1=80, 2=119',
#30   SF6
' 1=126',
#31   H2S
' 1=81, 2=82, 3=83',
#32   HCOOH
' 1=84',
#33   HO2
' 1=85',
#34   O
' 1=86',
#35   ClONO2
'1=127, 2=128',
#36   NO+
' 1=87',
#37   HOBr
' 1=88, 2=89',
#38   C2H4
' 1=90, 2=91',
#39   CH3OH
' 1=92',
#40   CH3Br
' 1=93, 2=94',
#41   CH3CN
' 1=95',
#42   CF4
' 1=96',
#43   C4H2
' 1=116',
#44   HC3N
' 1=109',
#45   H2
' 1=103, 2=115',
#46   CS
' 1=97, 2=98, 3=99, 4=100',
#47   SO3
' 1=114',
#48   C2N2
' 1=123',
#49   COCl2
'1=124, 2=125',
#50   SO
'1=146, 2=147, 3=148',
#51   CH3F
'1=144',
#52 GeH4
'1=139, 2=140, 3=141, 4=143',
#53   CS2
'1=131, 2=132, 3=133, 4=134',
#54   CH3I
'1=145',
#55   NF3
'1=136']

for val in mol_id:
    count = val.count("=");
    if count != 0:
        mol_num = val.split('=')[0];
        mol_n = mol_num.strip();
        print(mol_num);
        mol_num = int(mol_num);
        if mol_num < len(isotopologue):
            print (isotopologue[mol_num])
            mol_name = val.split('=')[1].strip();
            iso_list = isotopologue[mol_num].split(',');
            for iso in iso_list:
                count_iso = iso.count("=");
                print('test')
                if count_iso != 0:
                    print('test1')
                    iso_num = iso.split('=')[0];
                    print(iso_num);
                    iso_n = iso_num.strip();
                    iso_num = int(iso_num);
                    global_id = iso.split('=')[1]
                    print(global_id)
                    global_id = global_id.strip()
                    global_id = int(global_id)
                    output_directory = 'data/'
                    os.makedirs(output_directory, exist_ok=True)
                    print('data/' + mol_name + '_' + iso_n)
                    #print('data/' + mol_name + '_' + iso_n)
                    db_begin('data/' + mol_name + '_' + iso_n);
                    #print('test2')
                    #print(mol_name + str(iso_num))
                    fetch_by_ids(mol_name,[global_id],0,100000);



