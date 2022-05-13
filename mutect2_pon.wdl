version 1.0

#  Create a Mutect2 panel of normals
#
#  Description of inputs
#  intervals: genomic intervals
#  ref_fasta, ref_fai, ref_dict: reference genome, index, and dictionary
#  normal_bams: arrays of normal bams
#  scatter_count: number of parallel jobs when scattering over intervals
#  pon_name: the resulting panel of normals is {pon_name}.vcf
#  m2_extra_args: additional command line parameters for Mutect2.  This should not involve --max-mnp-distance,
#  which the wdl hard-codes to 0 because GenpmicsDBImport can't handle MNPs

#import "mutect2.wdl" as m2

import "mutect2.wdl" as m2

workflow Mutect2_Panel {
  input {
    File? intervals
    File ref_fasta
    File ref_fai
    File ref_dict
    Int scatter_count
    Array[String] normal_bams
    Array[String] normal_bais
    String? m2_extra_args
    String? create_pon_extra_args
    Boolean? compress
    String pon_name
    String outdir
    Int? min_contig_size
    Int? num_contigs

    # Use as a last resort to increase the disk given to every task in case of ill behaving data
    Int? emergency_extra_disk
  }

  Int contig_size = select_first([min_contig_size, 1000000])

    scatter (normal_bam in zip(normal_bams, normal_bais)) {
        call m2.Mutect2 {
            input:
                intervals = intervals,
                ref_fasta = ref_fasta,
                ref_fai = ref_fai,
                ref_dict = ref_dict,
                tumor_reads = normal_bam.left,
                tumor_reads_index = normal_bam.right,
                scatter_count = scatter_count,
                outdir = outdir,
                m2_extra_args = select_first([m2_extra_args, ""]) + "--max-mnp-distance 0"

        }
    }

    call m2.SplitIntervals {
        input:
            ref_fasta = ref_fasta,
            ref_fai = ref_fai,
            ref_dict = ref_dict,
            scatter_count = select_first([num_contigs, 24]),
            split_intervals_extra_args = "--subdivision-mode BALANCING_WITHOUT_INTERVAL_SUBDIVISION --min-contig-size " + contig_size,
    }

    scatter (subintervals in SplitIntervals.interval_files ) {
            call CreatePanel {
                input:
                    input_vcfs = Mutect2.filtered_vcf,
                    intervals = subintervals,
                    ref_fasta = ref_fasta,
                    ref_fai = ref_fai,
                    ref_dict = ref_dict,
                    output_vcf_name = pon_name,
                    create_pon_extra_args = create_pon_extra_args,
         
            }
    }

    call m2.MergeVCFs {
        input:
            input_vcfs = CreatePanel.output_vcf,
            input_vcf_indices = CreatePanel.output_vcf_index,
            output_name = pon_name,
            compress = select_first([compress, false]),
            outdir = outdir,
    }

    output {
        File pon = MergeVCFs.merged_vcf
        File pon_idx = MergeVCFs.merged_vcf_idx
        Array[File] normal_calls = Mutect2.filtered_vcf
        Array[File] normal_calls_idx = Mutect2.filtered_vcf_idx
    }
}

task CreatePanel {
    input {
      File intervals
      Array[String] input_vcfs
      File ref_fasta
      File ref_fai
      File ref_dict
      String output_vcf_name
      String? create_pon_extra_args
    }


    command {
        set -e

        gatk GenomicsDBImport --genomicsdb-workspace-path pon_db -R ~{ref_fasta} -V ~{sep=' -V ' input_vcfs} -L ~{intervals}

        gatk  CreateSomaticPanelOfNormals -R ~{ref_fasta} \
            -V gendb://pon_db -O ~{output_vcf_name}.vcf ~{create_pon_extra_args}
    }

    runtime {
         backend:"Local"
    }

    output {
        File output_vcf = "~{output_vcf_name}.vcf"
        File output_vcf_index = "~{output_vcf_name}.vcf.idx"
    }
}