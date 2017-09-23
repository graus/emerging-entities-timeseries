# -*- coding: utf-8 -*-

"""  INPUT: FAKBA1_counts
    OUTPUT: Wikipedia-Freebase ID-mappings """

import cPickle as pkl
import os
import sys


def extract_FAKBA_FBids(fakba_count_file):
    fakba_ids = {}

    with open(fakba_count_file) as infile:
        for line in infile:
            fbid, count = line.strip().split("\t")
            fakba_ids[fbid] = 1

    print "Have %d FBids" % len(fakba_ids)
    return fakba_ids


def db2fb(fblinks_file, fb_ids):

    d = {}
    with open(fblinks_file) as f:
        for line in f:
            triple = line.strip().split(" ")

            if len(triple) == 4:
                db, p, fb, _ = triple
                fb = "/" + fb.rsplit("/", 1)[-1].replace(".", "/")[:-1]  # <http://rdf.freebase.com/ns/m.0100j9wd>

                if fb in fb_ids:
                    db = db.rsplit('/', 1)[-1][:-1] # <http://dbpedia.org/resource/Stephen_Kwelio_Chemlany>
                    d[db] = fb
                    del fb_ids[fb]

    print("Can map %d of these to DBpedia" % len(d))
    return d


def wiki2fb(page_id_file, mappings):
    d = {}
    with open(page_id_file) as f:
        for line in f:
            triple = line.strip().split(" ")
            if len(triple) == 4:
                db, p, wiki, _ = triple
                db = db.rsplit('/', 1)[-1][:-1]
                if db in mappings:
                    wiki = wiki.split('"', 2)[1] # "10"^^<http://www.w3.org/2001/XMLSchema#integer>
                    d[wiki] = mappings[db]

    print "Can map %d of these to Wikipedia (%.1f%% coverage)" % (len(d),
                                                                  (len(d)/float(len(mappings)))*100
                                                                  )
    return d


if __name__ == "__main__":
    FAKBACOUNT_FILE = 'out/FAKBA1_FBid_counts.tsv'
    FB_LINKS_FILE = 'data/freebase_links_en.ttl'
    PAGE_IDS_FILE = 'data/page_ids_en.ttl'

    if not os.path.exists(FAKBACOUNT_FILE):
        sys.exit("Run 0_parse_FAKBA.py first")
    if not os.path.exists(FB_LINKS_FILE):
        sys.exit("Download Freebase links: http://downloads.dbpedia.org/2016-10/core-i18n/en/freebase_links_en.ttl.bz2")
    if not os.path.exists(PAGE_IDS_FILE):
        sys.exit("Download Page ID triples: http://downloads.dbpedia.org/2016-10/core-i18n/en/page_ids_en.ttl.bz2")

    fakba_ids = extract_FAKBA_FBids(FAKBACOUNT_FILE)
    db2fb_mappings = db2fb(FB_LINKS_FILE, fakba_ids)
    wiki2fb_mappings = wiki2fb(PAGE_IDS_FILE, db2fb_mappings)

    with open ('data/pkl/wiki2fb.pkl', 'w') as out:
        pkl.dump(wiki2fb_mappings, out)
