#################################################
#  File Name:run.sh
#  Author: Pengwei.Xing
#  Mail: xingwei421@qq.com,pengwei.xing@igp.uu.se,xpw1992@gmail.com
#  Created Time: Fri Apr 29 11:50:14 2022
#################################################

python somatic_snp_pipeline.py -l sample.list -g hg19 -t 30 -o ./ \
	-fun_path /disk1/pengweixing/database/Funcotator/funcotator_dataSources.v1.6.20190124s \
	-ref /disk1/pengweixing/database/hg19/hg19.fa \
	-dict /disk1/pengweixing/database/hg19/hg19.dict \
	-fai /disk1/pengweixing/database/hg19/hg19.fa.fai 
