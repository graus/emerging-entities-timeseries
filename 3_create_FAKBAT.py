""" Given FBid-timestamp mapping, annotate FAKBA (and write only docs w/ emerging entities) """

from time import time
import gzip
import os
import dateutil.parser
import datetime
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool


def run(filename):
    OUT_FILE = filename.replace(".gz", ".timestamped.gz").replace("FAKBA1", "FAKBAT")

    with gzip.open(filename) as infile:

        t0 = time()
        print "Parsing: %s" % filename

        first, buf = True, ""

        for line in infile:
            buf += line.strip()

            if first:
                assert line.startswith("trec/kba/kba")
                timestamp_doc = int(line.split("#")[-1].split("-")[0]) #datetime.datetime.fromtimestamp()
                first = False

            elif line == "\n": # new doc; flush
                first = True

            else:
                fbid = line.strip().split("\t")[-1]

                if fbid in timestamps:
                    timestamp_e = timestamps[fbid]
                    age = timestamp_doc-timestamp_e
                    buf += "\t" + str(age)

            buf += "\n"

    print "Done w/ %s.\nTook %.2f seconds. Compressing..." % (filename, (time()-t0))

    with gzip.open(OUT_FILE, 'wb') as f:
        f.write(buf)
    print "Finished compression"


if __name__ == "__main__":

    FBTIMESTAMP_FILE = 'data/FB2Timestamp.tsv'
    FAKBA1_DIR = 'data/FAKBA1/'

    timestamps = {}
    with open(FBTIMESTAMP_FILE) as f:
        for line in f:
            fbid, timestamp = line.strip().split("\t")
            timestamp = dateutil.parser.parse(timestamp).replace(tzinfo=None)
            timestamps[fbid] = (timestamp-datetime.datetime(1970,1,1)).total_seconds()
    print("Parsed %d FBid:timestamp-mappings" % len(timestamps))

    for (dirpath, dirnames, filenames) in os.walk(FAKBA1_DIR):
        filenames = sorted([dirpath + f for f in filenames])

    pool = Pool(4)
    pool.map(run, filenames)
    pool.close()
    pool.join()
