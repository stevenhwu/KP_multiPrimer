
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import Gapped, generic_dna

import re
import Bio.Seq
import sys

DEBUG = 0


infile_its = "F_ITS.fasta"
infile_28s = "F_28S.fasta"
outfile_name = "F_matched.fasta"

primer_its1f = "AAAACCGG"
primer_lror = "CCCCGGTT"
primer_edf360 = "GGGGTTAA"
primer_lr7 = "TTTTAACC"

re_primer_key1 = re.compile(primer_lror)
re_primer_key2 = re.compile(primer_lr7)

pattern = primer_lror + "([ACGTN-]+)" + primer_edf360
re_matching_seq = re.compile(pattern)

# in_handle1 = open(infile_its, "r")
# in_handle2 = open(infile_28s, "r")
# out_handle = open(outfile_name, "w")


def parseInputFile(infile):
    dict_match = {}
    for record in SeqIO.parse(infile, "fasta"):
        seq = str(record.seq)
        match = re_matching_seq.search(seq)

        if match:
            if DEBUG:
                print('<Match: %r, groups=%r, full=%s>' %
                      (match.group(), match.groups(), match.string))
            key = match.group()
            if key in dict_match:
                print "===Warning===: key fragment:(%s) exist already" % key
#                 dict_match[key].append(record)
#                 print dict_match[key]
                dict_match[key] = record
            else:
                dict_match[key] = record
    #     print sys.getsizeof(record), len(record.seq)
    return dict_match



dict_its = parseInputFile(infile_its)
dict_28s = parseInputFile(infile_28s)

print dict_its.keys()
print "================"
print dict_28s.keys()

all_new_seq = []

for key in dict_its.keys():
    if key in dict_28s:


        id1, id2 = dict_its[key].id, dict_28s[key].id
        print key, dict_its[key].seq.find(key), dict_its[key].seq
        print key, dict_28s[key].seq.find(key), dict_28s[key].seq
#         prefix = dict_its[key].seq.split(key)
#         sufix = dict_28s[key].seq.split(key)
#         prefix_str = str(prefix[0])
#         sufix_str = str(sufix[1])
#         new_seq = SeqRecord(Seq(prefix_str + key + sufix_str), id=(id1 + "_" + id2))
#         print new_seq.seq

        prefix_index = dict_its[key].seq.find(key)
        prefix_str = str(dict_its[key].seq)[0:prefix_index]
#         sufix_index = dict_28s[key].seq.find(key)
        sufix_str = str(dict_28s[key].seq)
        print (prefix_str)
        print (sufix_str)


        new_seq = SeqRecord(Seq(prefix_str + sufix_str),
                            id=(id1 + "_" + id2), description="")
        print "FINAL: %s" % new_seq.seq
        all_new_seq.append(new_seq)

#         print dict_its[key].seq[:prefix_index]
#         print dict_28s[key].seq[sufix_index:]
#         print prefix
#         print sufix
#
#
#
#         new_seq = SeqRecord(Seq(prefix_str + key + sufix_str), id=(id1 + "_" + id2))
#         print new_seq.seq
SeqIO.write(all_new_seq, outfile_name, "fasta")
