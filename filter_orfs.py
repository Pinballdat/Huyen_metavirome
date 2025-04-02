import pandas as pd
from Bio import SeqIO
input_file = "/data18tb/datnguyen/ORF_HuyenDo/test.txt"
fasta_file = "/data18tb/datnguyen/ORF_HuyenDo/HMG2.cds.raw.fa"
names = []
sequences = []
states = []

fasta_seqs = SeqIO.parse(fasta_file, "fasta")
for seq in fasta_seqs:
    names.append(seq.id)
    sequences.append(seq.seq)
content = pd.read_csv(input_file, sep="\t", 
                      names=["Tên gene","Vị trí bắt đầu ORF","Vị trí kết thúc ORF","Thông tin", "Ghi chú", "Chiều"],
                      usecols=["Tên gene","Thông tin"])

content[["ID","Trạng thái","Độ dài ORF","Khung ORF","Codon bắt đầu","Codon kết thúc"]] = content["Thông tin"].str.split(";", expand=True)
content["Độ dài ORF"] = content["Độ dài ORF"].str.extract("(\d+)").astype(int)
# print(content.dtypes)
test = content.groupby(["Tên gene"], as_index=True).agg({"Độ dài ORF":"max","Trạng thái":"first"})
for name in names:
    if name in test.index:
        states.append(test.at[name,"Trạng thái"])
    else:
        states.append("3-prime-partial + 5-prime-partial")
# test["Số thứ tự"] = test["Tên gene"].str.extract(r'(\d+)').astype(int)
# sorted_df = test.sort_values(by="Số thứ tự").reset_index().drop(columns="index")
df = pd.DataFrame({"Name":names, "Sequence":sequences, "States":states})
# id_not_test = []
# for index in sorted_df.index:
#     if (index + 1) not in list(sorted_df["Số thứ tự"]):
#         id_not_test.append(index+1)
# print(id_not_test)
# sorted_df = test.sort_values(by='Tên gene', key=lambda col: col.str.split("_")[2])
df.to_csv("/data18tb/datnguyen/ORF_HuyenDo/ORFs_results.final.tsv", sep="\t")
# print(sorted_df)