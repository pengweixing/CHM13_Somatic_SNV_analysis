"""
sample.list format :
sample_name Tumor.bam   Normal.bam

The bam file should be indexed
The bam file should contain @RG\tID:foo\tSM:CEM-0040\tLB:library1 field. It could be specifed in bwa command by -R

"""

import sys
import json
import argparse
import collections
import os

alldict = {'Mutect2.intervals': '',
'Mutect2.scatter_count': 30,
'Mutect2.outdir': '',
'Mutect2.m2_extra_args': '--downsampling-stride 20 --max-reads-per-alignment-start 6 --max-suspicious-reads-per-alignment-start 6',
'Mutect2.filter_funcotations': 'True',
'Mutect2.funco_reference_version': 'hg38',
'Mutect2.funco_data_sources_path': '',
'Mutect2.run_funcotator': True,
'Mutect2.ref_fasta': '',
'Mutect2.ref_dict': '',
'Mutect2.ref_fai': '',
'Mutect2.normal_reads': 'normal.bam',
'Mutect2.normal_reads_index': 'normal.bam.bai',
'Mutect2.tumor_reads': 'tumor.bam',
'Mutect2.tumor_reads_index': 'tumor.bam.bai'}
    
def fargv():
    parser = argparse.ArgumentParser(usage="python ")
    parser.add_argument('-l',"--list",help="the sample list ", default='sample.list')
    parser.add_argument('-g',"--reference",help="the version of reference genome, hg19 or hg38 ", default='hg38')
    parser.add_argument('-t',"--threads",help="the cpu number", default=30,type=int)
    parser.add_argument('-o',"--output",help="the output directory", default='./')
    parser.add_argument('-ref',"--ref_fa",help="the output directory", required=True)
    parser.add_argument('-fun',"--funcotator",help="Do funcotator or not", default=True,type=bool)
    parser.add_argument('-fun_path',"--funcotator_path",help="the path of funcotator", required=True)
    parser.add_argument('-dict',"--ref_dict",help="the path of funcotator", required=True)
    parser.add_argument('-fai',"--ref_fai",help="the path of funcotator", required=True)
  
    args = parser.parse_args()
    return args

def init_json(args,main_dir):
    
    output = args.output

    if output == './':
        output = os.getcwd()
    alldict['Mutect2.outdir'] = output
    alldict['Mutect2.scatter_count'] = args.threads
    alldict['Mutect2.funco_data_sources_path'] = args.funcotator_path
    alldict['Mutect2.ref_fasta'] = args.ref_fa
    alldict['Mutect2.ref_dict'] = args.ref_dict
    alldict['Mutect2.ref_fai'] = args.ref_fai

    if args.funcotator:
        alldict['Mutect2.run_funcotator'] = 'True'
    else:
        alldict['Mutect2.run_funcotator'] = 'False'

    if args.reference == 'hg38':
        alldict['Mutect2.intervals'] = main_dir+"/wgs_calling_regions.hg38.intervals"
    elif args.reference == 'hg19':
        alldict['Mutect2.intervals'] = main_dir+"/b37_wgs_consolidated_calling_intervals.list"
    elif args.reference == 'CHM13':
        alldict['Mutect2.intervals'] = main_dir+"/CHM13.interval.txt"
    else:
        raise RuntimeError("the reference genonme should be hg38 or hg19 or CHM13")

    return alldict


def mkdir(args): 
    output = args.output
    if output == './':
        output = os.getcwd()
    try:
        os.mkdir(output+'/Config')
    except OSError as error:
        print("Warning: The directory of Config has already exists\n")

def write_json(name,alldict,output):
    with open(output+'/Config/'+name+'_inputs.json','w') as f:
        f.write(alldict)
    
def main(kwargs):

    args = kwargs
    sample_list = args.list
    output = args.output
    if output == './':
        output = os.getcwd()
    if not os.path.exists(output+"/"+sample_list):
        raise FileNotFoundError(output+"/"+sample_list+" not exit")
    mkdir(args)
    main_dir = (os.path.split(os.path.realpath(__file__))[0])

    alldict= init_json(args,main_dir)
    f = open('run_snp_calling.sh','w')
    command = "java -jar {main_dir}/cromwell-78.jar run {main_dir}/mutect2.wdl -i {sample}"
    for line in open(sample_list,'r'):
        line = line.strip().split()
        name,tumor,normal = line[0:3]
        if os.path.exists(tumor):
            alldict['Mutect2.tumor_reads'] = tumor
        else:
            raise FileNotFoundError(tumor+" not exit")
        if os.path.exists(normal):
            alldict['Mutect2.normal_reads'] = normal
        else:
            raise FileNotFoundError(tumor+" not exit")
        if os.path.exists(normal+'.bai'):
            alldict['Mutect2.normal_reads_index'] = normal+'.bai'
        else:
            raise FileNotFoundError(normal+" index not exit")
        if os.path.exists(tumor+'.bai'):
            alldict['Mutect2.tumor_reads_index'] = tumor+'.bai'
        else:
            raise FileNotFoundError(tumor+" index not exit")
        alldict2 = json.dumps(alldict,indent=4)
        write_json(name,alldict2,output)
        text = command.format(sample=output+'/Config/'+name+'_inputs.json',main_dir=main_dir)
        f.write("%s\n" % text)

    f.close()

if __name__ == "__main__":
    kwargs = fargv()
    main(kwargs)