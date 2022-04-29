- ### THIS PIPELINE IS BUILT ON GATK-WORKFLOW. 
- ### This pipeline is used to detect the somatic snvs and indels based on bam file

 #
- ### Usage:
	1. The bam file should contain @RG\tID:foo\tSM:CEM-0040\tLB:library1 field that could be specified in the bwa command.

		`bwa mem  -R '@RG\tID:foo\tSM:CEM-0040\tLB:library1'`
	2. export PATH="/disk1/pengweixing/software/gatk-4.1.7.0/gatk:$PATH"
	3. provide the sample.list
		```
		Name1 tumor_bam_file1 normal_bam_file1
		Name2 tumor_bam_file2 normal_bam_file2
		...
		```
	4. download the annotation files: 

		`wget  https://storage.googleapis.com/broad-public-datasets/funcotator/funcotator_dataSources.v1.6.20190124s.tar.gz`

	5. `tar -zxf funcotator_dataSources.v1.6.20190124s.tar.gz`
	6. go to your working directory
	7. provide appropriate ref genome and run the following script

		```python
		python somatic_snp_pipeline.py -l sample.list -g hg19 -t 30 -o ./ \
			-fun_path /disk1/pengweixing/database/Funcotator/funcotator_dataSources.v1.6.20190124s \
			-ref /disk1/pengweixing/database/hg19/hg19.fa \
			-dict /disk1/pengweixing/database/hg19/hg19.dict \
			-fai /disk1/pengweixing/database/hg19/hg19.fa.fai
		```
	8. It will generate the script(run.sh) for snv calling

		```bash
		nohup bash run.sh 1>log.e 2>log.e &
		``` 