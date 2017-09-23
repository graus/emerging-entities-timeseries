from collections import defaultdict
from time import time
import os
import gzip


def extract_fb_ids(fakba_chunk):
    """ Parses FAKBA1 chunkfile, extracts FBids """

    t0 = time()
    print("Parsing: %s" % fakba_chunk)

    with gzip.open(fakba_chunk, "rb") as f:
        data = f.read().split("trec/kba/kba-streamcorpus-2014-v0_3_0-serif-only/")

        for a in data:
            annotations = filter(None, a.split("\n"))

            if annotations: # [docid, entity_1, entity_2, ...]

                for line in annotations[1:]: # prune docid
                    fb_id = line.strip().split("\t")[-1]
                    d[fb_id] += 1

    print "\tFinished: %s (in %f seconds)" % (fakba_chunk, time() - t0)


if __name__ == "__main__":

    OUTFILE = "out/FAKBA1_FBid_counts.tsv"
    FAKBA_DIR = "data/FAKBA1/"

    for (dirpath, dirnames, filenames) in os.walk(FAKBA_DIR):
        file_paths = [dirpath + f for f in filenames]

    d = defaultdict(int)
    for fp in file_paths:
        extract_fb_ids(fp)

    with open(OUTFILE, "w") as out:
        for fb_id, count in d.iteritems():
            out.write("%s\t%d\n" % (fb_id, count))