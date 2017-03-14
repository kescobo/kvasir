#!/usr/bin/env python

import pymongo
import argparse
import os
import logging
from kvasir.mongo_import import mongo_import_genbank

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Import genbank files')

parser.add_argument("mongodb", help="The name of MongoDB database")
parser.add_argument("-i", "--input", help="File or directory to import", required=True)

parser.add_argument("-v", "--verbose", help="Display debug status messages", action="store_true")
parser.add_argument("-q", "--quiet", help="Suppress most output", action="store_true")

args = parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.DEBUG)
elif args.quiet:
    logging.basicConfig(level=logging.WARNING)
else:
    logging.basicConfig(level=logging.INFO)

INPUT = args.input
DB = pymongo.MongoClient()[args.mongodb]

success = 0

if os.path.isdir(INPUT):
    for f in os.listdir(INPUT):
        # TODO: figure out way to throw an error if it looks like the same gene/genome is being imported
        if f.endswith(".gb") or f.endswith(".gbk"):
            logging.info("** Importing {} **".format(f))
            mongo_import_genbank(os.path.join(INPUT, f), DB, "genes")
            success = 1
elif os.path.isfile:
    if f.endswith(".gb") or f.endswith(".gbk"):
        logging.inf("** Importing {} **".format(f))
        mongo_import_genbank(os.path.join(INPUT, f), DB, "genes")
        success = 1

if not success:
    raise ValueError("Input must be genbank file or folder containing genbank files")