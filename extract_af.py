#################################################
#  File Name:extract_af.py
#  Author: Pengwei.Xing
#  Mail: xingwei421@qq.com,pengwei.xing@igp.uu.se,xpw1992@gmail.com
#  Created Time: Tue May  3 10:34:36 2022
#################################################

import sys

f1 = open(sys.argv[1],'r')##  pass.vcf file

for line in f1:
    line = line.strip()
    if not line.startswith('#'):
        line1 = line.split('\t')
        mychr = line1[0]
        mypos = line1[1]
        temp = line1[10]
        af = temp.split(':')[2]

        print(mychr,mypos,af,sep="\t")
        
