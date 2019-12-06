code_dir=/home/yihang/NaoJiYe/code/demultiplex_by_barcodes.py 
datapath=/home/yihang/NaoJiYe/scRNA_seq
patient=0426
samplelist=`ls ${datapath}/${patient}|grep "fastq"|cut -d "_" -f1|uniq`
##samplelist=CSF-0107-A1-1
barcode_pos=9
barcode_len=8
barcode_fil=/home/yihang/NaoJiYe/code/demultiplex_barcode.csv
mismatch=2
fix=1

for sample in ${samplelist[@]}
do
	read1=${datapath}/${patient}/${sample}_combined_R1.fastq
	read2=${datapath}/${patient}/${sample}_combined_R2.fastq
	python3 ${code_dir} ${read1} ${read2} ${barcode_pos} ${barcode_len} ${barcode_fil} ${mismatch} ${fix} ${datapath}/${patient}/${sample}
	if [ ! -d ${datapath}/${patient}/${sample}/Unmatched ];then
	mkdir ${datapath}/${patient}/${sample}/Unmatched
	fi
	cd ${datapath}/${patient}/${sample}
	mv *unmatched* Unmatched/
done
