# -*- coding: utf-8 -*-

# Given:
# - list of FAKBA IDs [FBid]
# - wikiId <-> FB mapping [FBid, mapping]
# - wikiTitle <-> FB mapping [FBid, wikiTitle]
# - wikiId/wikiTitle <-> timestamp [wikiId, wikiTitle, timestamp]

# add "first" timestamp

from collections import defaultdict
import urllib2
import codecs


def urlencoding_to_utf8(urlEncodedWikiTitle):
  wiki_title = (urlEncodedWikiTitle).replace("_", " ")
  if "%13" in wiki_title:
    wiki_title = wiki_title.replace("%13", u'\u2013')
  if "%0D" in wiki_title:
    wiki_title = wiki_title.replace("%0D", u'č')
  if "%0A" in wiki_title:
    wiki_title = wiki_title.replace("%0A", u'Ċ')
  if "%" in wiki_title:
    wiki_title = urllib2.unquote(wiki_title)
  return wiki_title

fbid2wid = defaultdict(list)
with open("data/mappings/FBid2WikiId.tsv", "r") as infile:
  for line in infile:
      FBid, mapping = line.strip().split("\t")
      fbid2wid[FBid].append(mapping)

fbid2wtitle = defaultdict(list)
with codecs.open("data/mappings/FBid2WikiTitle.tsv", "r", "utf-8") as infile:
    for line in infile:
        FBid, mapping = line.strip().split("\t")
        fbid2wtitle[FBid].append(urlencoding_to_utf8(mapping))

wid2timestamp, wtitle2timestamp = {}, {}
with codecs.open("data/mappings/wikiIdTitleTimestamp.tsv", "r", "utf-8") as infile:
  for line in infile:
      wikiId, wikiTitle, timestamp = line.strip().split("\t")
      wid2timestamp[wikiId] = timestamp
      wtitle2timestamp[wikiTitle] = timestamp


f = codecs.open("data/FAKBA_timestamps.tsv", "w", "utf-8")
with open("data/FAKBA_counts.tsv", "r") as fakbacounts:
  for line in fakbacounts:
    timestamp, wt, wi = set(), "", ""
    fbid, count = line.strip().split("\t")

    if fbid in fbid2wtitle:
      wtitle = fbid2wtitle[fbid]
      for wt in wtitle:
        if wt in wtitle2timestamp:
          timestamp.add(wtitle2timestamp[wt])
          print "\tHave title:", wt, timestamp

    if fbid in fbid2wid:
      wid = fbid2wid[fbid]
      for wi in wid:
        if wi in wid2timestamp:
          timestamp.add(wid2timestamp[wi])
          print "\tHave ID:", wi, timestamp

    if not timestamp:
      timestamp.add("-")
    out = "%s\t%s\t%s\t%s\n" % (line.strip(), sorted(timestamp)[0], wt, wi)
    print out.strip()
    f.write(out)

f.close()
