#################################################
#  File Name:generate_pon_json.py
#  Author: Pengwei.Xing
#  Mail: xingwei421@qq.com,pengwei.xing@igp.uu.se,xpw1992@gmail.com
#  Created Time: Fri May 13 11:01:05 2022
#################################################

import sys
import json
import argparse
import collections
import os

alldict = \
{
	"Mutect2_Panel.pon_name":"panel_of_normal",
	"Mutect2_Panel.normal_bams":"",
	"Mutect2_Panel.normal_bais":"",
	"Mutect2_Panel.ref_fasta":"",
	"Mutect2_Panel.ref_fai":"",
	"Mutect2_Panel.ref_dict":"",
	"Mutect2_Panel.scatter_count":10,
	"Mutect2_Panel.intervals":""
}
def fargv():
    parser = argparse.ArgumentParser(usage="python ")
    parser.add_argument('-l',"--list",help="the sample list ", default='sample.list')
    parser.add_argument('-g',"--reference",help="the version of reference genome, hg19 or hg38 ", default='hg38')
    parser.add_argument('-ref',"--ref_fa",help="the output directory", required=True)
    parser.add_argument('-dict',"--ref_dict",help="the path of funcotator", required=True)
    parser.add_argument('-fai',"--ref_fai",help="the path of funcotator", required=True)
    args = parser.parse_args()
    return args


def main(kwargs):
    args = kwargs
    sample_list = args.list
    alldict['Mutect2_Panel.ref_fasta'] = args.ref_fa
    alldict['Mutect2_Panel.ref_fai'] = args.ref_fai
    alldict['Mutect2_Panel.ref_dict'] = args.ref_dict
    tumor_list = []
    with open(sample_list,'r') as f:
        for line in f:
            line = line.strip()
            line1 = line.split()
            tumor_list.append(line1[1])
    alldict['Mutect2_Panel.normal_bams'] = tumor_list
    tumor_bai = [each+'.bai' for each in tumor_list]
    alldict['Mutect2_Panel.normal_bais'] = tumor_bai
    main_dir = (os.path.split(os.path.realpath(__file__))[0])

    if args.reference == 'hg38':
        alldict['Mutect2_Panel.intervals'] = main_dir+"/wgs_calling_regions.hg38.intervals"
    elif args.reference == 'hg19':
        alldict['Mutect2_Panel.intervals'] = main_dir+"/b37_wgs_consolidated_calling_intervals.list"
    elif args.reference == 'CHM13':
        alldict['Mutect2_Panel.intervals'] = main_dir+"/CHM13.interval.txt"
    else:
        raise RuntimeError("the reference genonme should be hg38 or hg19 or CHM13")

    alldict2 = json.dumps(alldict,indent=4)
    print(alldict2)
if __name__ == "__main__":
    kwargs = fargv()
    main(kwargs)
