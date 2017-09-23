# -*- coding: utf-8 -*-

################################################
# Step 1:  Input: Wiki stub history xml        #
#             Do: Extract timestamps           #
#         Output: wiki_title \t wiki_timestamp #
################################################

import re, gzip
import xml.etree.cElementTree as ET
import cPickle as pkl
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
p = re.compile(r"^Wikipedia|User|File|Template|Category|Help|Talk|MediaWiki|Portal( talk)?:")


def extract_timestamps(wiki_stub_file, mappings):

    with gzip.open(wiki_stub_file) as infile:
        for _ in range(45):
            next(infile) # skip header

        txt = ''
        for line in infile:
            txt += line

            if line.strip().startswith("</page>"):
                try:
                    e = ET.fromstring(txt)
                except:
                    txt = ''
                    continue

                txt = ''
                if e.find("redirect") is None: # no redirect, test for bogus title
                    wiki_id = e.find('id').text

                    if wiki_id not in mappings:
                        continue

                    title = e.find('title').text
                    if not re.match(p, title) and not "(disambiguation)" in title:  # escape if bad title
                        timestamp = []

                        for child in e.findall("revision"):
                            timestamp.append(child.find("timestamp").text)

                        yield("%s\t%s\n" % (mappings[wiki_id], sorted(timestamp)[0]))

                    del mappings[wiki_id]


if __name__ == "__main__":


    with open('data/pkl/wiki2fb.pkl', 'r') as pkl_file:
        wiki2fb = pkl.load(pkl_file)

    with open('data/FB2Timestamp.tsv', 'w') as f:
        for ts in extract_timestamps('data/enwiki-latest-stub-articles.xml.gz', wiki2fb):
            f.write(ts)

