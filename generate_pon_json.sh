#################################################
#  File Name:generate_pon_json.sh
#  Author: Pengwei.Xing
#  Mail: xingwei421@qq.com,pengwei.xing@igp.uu.se,xpw1992@gmail.com
#  Created Time: Fri May 13 11:23:09 2022
#################################################

python generate_pon_json.py  -ref /disk1/pengweixing/database/CHM13/chm13v2.0.fa -dict /disk1/pengweixing/database/CHM13/chm13v2.0.dict -fai /disk1/pengweixing/database/CHM13/chm13v2.0.fa.fai -g CHM13 > mutect2_pon.inputs.json
/disk1/pengweixing/software/jdk-17.0.3/bin/java -jar /disk1/pengweixing/pipeline/GATK_wdl_pipeline/cromwell-78.jar run mutect2_pon.wdl -i mutect2_pon.inputs.json
