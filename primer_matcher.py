
from Bio.Seq import Seq
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import Gapped, generic_dna

import re
import Bio.Seq
import sys
import os

DEBUG = 0

data_dir = "data"
infile_its = os.path.join(data_dir, "F_ITS.fasta")
infile_28s = os.path.join(data_dir, "F_28S.fasta")
outfile_name = os.path.join(data_dir, "Result_matched.fasta")

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
                dict_match[key].append(record)
#                 print dict_match[key]
#                 dict_match[key] = record
            else:
                dict_match[key] = [record]
    #     print sys.getsizeof(record), len(record.seq)
    return dict_match

def join_two_records(record_part1, record_part2):

    if DEBUG > 2:
        print key, record_part1.seq.find(key), record_part1.seq
        print key, record_part2.seq.find(key), record_part2.seq
#         prefix = dict_its[key].seq.split(key)
#         sufix = dict_28s[key].seq.split(key)
#         prefix_str = str(prefix[0])
#         sufix_str = str(sufix[1])
#         new_seq = SeqRecord(Seq(prefix_str + key + sufix_str), id=(id1 + "_" + id2))

    prefix_index = record_part1.seq.find(key)
    prefix_str = str(record_part1.seq)[0:prefix_index]
#         sufix_index = dict_28s[key].seq.find(key)
    sufix_str = str(record_part2.seq)


    new_seq = SeqRecord(Seq(prefix_str + sufix_str),
                        id=(record_part1.id + "_" + record_part2.id), description="")
    if DEBUG > 1:
        print (prefix_str)
        print (sufix_str)
    print "Merged %s: %s" % (new_seq.id, new_seq.seq)
    return new_seq


dict_its = parseInputFile(infile_its)
dict_28s = parseInputFile(infile_28s)

print "================"
print "ITS:", dict_its.keys()
print "28S:", dict_28s.keys()
print "================"
all_new_seq = []

for key in dict_its.keys():
    if key in dict_28s:
        for r1 in dict_its[key]:
            for r2 in dict_28s[key]:
                new_seq = join_two_records(r1, r2)
                all_new_seq.append(new_seq)

SeqIO.write(all_new_seq, outfile_name, "fasta")
