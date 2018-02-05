This is a collection of scripts that accompany our paper: [_"The Birth of Collective Memories: Analyzing Emerging Entities 
in Text Streams"_](http://graus.co/publications/the-birth-of-collective-memories-analyzing-emerging-entities-in-text-streams/). 
These scripts enable you to recreate the "`FAKBAT`" dataset from the paper (i.e., [FAKBA1](http://trec-kba.org/data/fakba1/) with "entity age timestamps").

My apologies for the current state/lack of documentations of these scripts, they are currently very 'academic.' However, I did run through them to clean them up a bit, and the process shouldn't be too complex to follow. I'll likely do a clean-up soon. 

If you use the dataset, please kindly cite:

    @article {ASI:ASI24004,
    author = {Graus, David and Odijk, Daan and de Rijke, Maarten},
    title = {The birth of collective memories: Analyzing emerging entities in text streams},
    journal = {Journal of the Association for Information Science and Technology},
    issn = {2330-1643},
    url = {http://dx.doi.org/10.1002/asi.24004},
    doi = {10.1002/asi.24004},
    year={2018}
    }

## Requirements

* Python 2.7

### Libraries/packages
* `dateutil`

### Data
* Freebase Annotations for the TREC KBA 2014 StreamCorpus: [FAKBA1](http://aws-publicdatasets.s3.amazonaws.com/trec/kba/FAKBA1/index.html) (~200GB)
* DBpedia to Wikipedia ID-mappings: [page\_ids\_en.ttl](http://downloads.dbpedia.org/2016-10/core-i18n/en/page_ids_en.ttl.bz2) (~170MB)
* DBpedia to Freebase MID-mappings: [freebase\_links\_en.ttl](http://downloads.dbpedia.org/2016-10/core-i18n/en/freebase_links_en.ttl.bz2) (~80MB) 
* Wikipedia Meta history (for extracting page creation dates): [enwiki-latest-stub-meta-history.xml](https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-stub-meta-history.xml.gz) (50+ GB)


## Pipeline

1. `./0_parse_FAKBA.py <location of FAKBA1 files>` do a single pass through FAKBA1, collect (+count) all Freebase MIDs in FAKBA1;
1. `./1_Wiki2Freebase.py`: Generate mappings from Wikipedia IDs to Freebase MIDs (filtered with the MIDs yielded by the previous step);
1. `./2_extract_WikiTimestamps.py`: Pass through Wikipedia Meta Stub file, output Freebase MID to timestamp-mappings;
1. `./3_create_fakbat.py`: Pass through FAKBA1 file-by-file, add entity 'age' column.


### TODOs 
It is not absolutely necessary to first pass through FAKBA1 just to get counts. It is also easy to parallelize. 
