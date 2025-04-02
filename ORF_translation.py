from Bio import Seq, SeqIO
import pandas as pd
HMG2_fasta = "/data18tb/datnguyen/ORF_HuyenDo/HMG2.cds.raw.fa"

HMG2_content = SeqIO.parse(HMG2_fasta, "fasta")

id = []
seqs = []
prots = []
States = []
for seq in HMG2_content:
    id.append(seq.id)
    seqs.append(seq.seq)
    prot = seq.translate(table="Standard", stop_symbol="*")
    prots.append(prot.seq)
    if prot[0] == "M" and prot[-1] == "*":
        # print(seq.id)
        # print(prot.seq)
        # prots.append(str(prot.seq))
        States.append("Complete")
    elif prot[0] != "M" and prot[-1] == "*":
        States.append("5'-prime-partial")
    elif prot[0] == "M" and prot[-1] != "*":
        States.append("3'-prime-partial")
    
    elif prot[0] != "M" and prot[-1] != "*":
        States.append("3'& 5'-prime-partial")

df = pd.DataFrame(data={"Gene name":id, "Gene sequence":seqs, "Protein sequence":prots, "States":States})
df.to_excel("/data18tb/datnguyen/ORF_HuyenDo/HMG2_results.xlsx")
print(df)
# print(len(id))
# print(len(seqs))
# print(len(prots))
# print(len(States))