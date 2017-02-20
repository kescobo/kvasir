#Kvasir

[![DOI](https://zenodo.org/badge/22309/kescobo/kvasir.svg)](https://zenodo.org/badge/latestdoi/22309/kescobo/kvasir) [![Join the chat at https://gitter.im/kescobo/kvasir](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/kescobo/kvasir?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Dependencies:
* Python 3+
* MongoDB
  * pymongo
* BioPython
* BLAST+ CLI

**Identification of horizontal gene transfer between sequenced microbial genomes**

Kvasir takes as the input a folder containing genomes in genbank format. The protein coding genes from these genomes are loaded into a database, and blasted against each other.

[Kvasir](https://en.wikipedia.org/wiki/Kvasir) is a Norse god associated with fermented beverages. According to Wikipedia,

>Extremely wise, Kvasir traveled far and wide, teaching and spreading knowledge. This continued until the dwarfs Fjalar and Galar killed Kvasir and drained him of his blood. The two mixed his blood with honey, resulting in the Mead of Poetry, a mead which imbues the drinker with skaldship and wisdom, and the spread of which eventually resulted in the introduction of poetry to mankind.

## Usage

### Mongod

Kvasir uses a [MongoDB](https://www.mongodb.com/) database to store genome and HGT information, so you'll need to install [mongodb](https://www.mongodb.com/download-center?jmp=nav#community) and [PyMongo](https://api.mongodb.com/python/current/installation.html) before doing anything.

MongoDB will build a database and index on your local system, so you should make a folder to put them in. You'll never have to interact with the folder manually, so I just put it in a hidden folder in my home directory.

```
mkdir ~/.mongo_databases
```

Before you run any commands with kvasir, you need to launch a local MongoDB server using the `mongod` command:

```
$ mongod --dbpath ~/.mongo_databases
```

### Adding Genomes

Kvasir can import genomes in [Genbank](https://www.ncbi.nlm.nih.gov/Sitemap/samplerecord.html) format. You can pass either a single file, or a folder with many genbank files. Only files with extensions `.gb` or `.gbk` will be imported.

Each genome set should have a unique name - this will be the first argument for every script. For the following examples, I'll be looking at cheese genomes and the set will have the name `cheese1`

```
$ python bin/import_genomes.py cheese1 -i path/to/genbank/files
```

I haven't yet built a way to check if you're trying to import the same genome multiple times, so use with caution! If you're not sure if you've already imported a file, you can query your MongoDB with the species name (see below for info on what is used as the species name). If you're not sure if you've imported *Awesomeus speciesus strain A*, launch python, and try the following:

```python
> import pymongo
> db = pymongo.MongoClient()["cheese1"] # substitute "cheese1" for the name of your genome set
> db["genes"].find_one({"species":"Awesomeus speciesus strain A"})
```

If nothing is returned, then you haven't imported it yet. The text has to be exact though. If you're not sure, you can also get a list of all the species with any genes in the database:

```python
> db["genes"].distinct("species")
```

**A note on Genbank formats**

If your files aren't formatted correctly, you ~~may~~ will have issues. At one point, I tried to write in a way to accomodate all kinds of messed up formats, but it's just not worth it. So check your genomes with care.

In particular, be sure that each contig in the genome has a uniqe id (that's the first field in the `LOCUS` line). Kvasir uses this to determine which genes are located near each other, if there are duplicates, it may think that genes on separate contigs are next to each other. Each gene should also have a unique `locus_tag` field.

Most genbank files have a `SOURCE` identifier, which contains the genus, species and strain that a particular contig comes from. This is what kvasir will use to identify genes from the same species. If your genbank file doesn't have this, kvasir will use the name of the genbank file as the name of the species - but be careful! A single genbank file can contain contigs from multiple species - if your files are organized this way, make sure that they have a `SOURCE` field.

At some point, I'll write a convenience script to check through your genomes to make sure that they'll work. But until then - use with caution.

### BLAST Searching

This is the meat of the analysis, and to make it work you need one more tool - [BLAST+](https://www.ncbi.nlm.nih.gov/books/NBK279671/) command line tools. This needs to be installed and accessible from your `$PATH`. In other words, you should be able to run `which blastn` and get a path spit back at you. If not - do some googling.

Assuming this is working (you've still got `mongod` running right?), it's time to start blasting. There are a couple of commands in the `blast.py` script. First, you've gotta make a blast database with all of the the genes in your database using `makedb`. This command will make 3 files, in the current directory by default, or in the directory you specify with `-b`

```
# python3 bin/blast.py cheese1 -c makedb -b ~/blastdbs
INFO:root:making BLAST database with protein coding sequences from cheese1 at /Users/ksb/blastdbs
INFO:root:BLAST db created at /Users/ksb/blastdbs
```

Next, blastall will go through each species in your database and blast it against that database. Each hit will then be stored in your MongoDB with some metadata.

```
# python3 bin/blast.py cheese1 -c blastall -b ~/blastdbs
INFO:root:blasting Glutamicibacter bergerei BW77
INFO:root:Blasting all by all
INFO:root:Getting Blast Records
INFO:root:---> 500 blast records retrieved
...
```

In this case - I've put in a check so if you run this a second time, 
