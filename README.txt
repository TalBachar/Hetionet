README file

Tal Bachar
Farhan Chodhury
CSCI 49371
4/4/2020

# Environment setup:


### install mongoDB:
https://docs.mongodb.com/manual/administration/install-community/


### Use pip to install pymongo:
$ python -m pip install pymongo


### Commands used in terminal to import files into mongoDB are:
mongoimport --db projectDB --collection nodes --type tsv <PATH/TO/FILE.tsv> --headerline
mongoimport --db projectDB --collection edges --type tsv <PATH/TO/FILE.tsv> --headerline


### run code
$ python part1.py


### enter name of disease



### Cassandra Setup

# Prerequisites: Install Java 8

# Download: http://cassandra.apache.org/download/

# Configuration: In conf/cassandra.yaml

### Commands used in terminal to import files into Cassandra are:

COPY node_tsv_import3 (id, name, kind) FROM '/DIRECTORY/nodes.tsv' WITH DELIMITER='\t' AND HEADER=TRUE;
COPY edge_tsv_import (id, name, kind) FROM '/DIRECTORY/edges.tsv' WITH DELIMITER='\t' AND HEADER=TRUE;

### run code
$ python cassandratest3.py

### run code
$ python cassandratest5.py
