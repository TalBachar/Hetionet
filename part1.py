#####     Tal Bachar     #####
#####  Farhan Chowdhury  #####
##### CSCI 49371 Project #####

# Commands used in terminal to import files into mongoDB are:
### mongoimport --db projectDB --collection nodes --type tsv <PATH/TO/FILE.tsv> --headerline
### mongoimport --db projectDB --collection edges --type tsv <PATH/TO/FILE.tsv> --headerline


import pymongo
import pprint
import sys

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)    # sets client to local database
db = client["projectDB"]      #db = name of database
edge_collection = db["edges"] #edges = name of collection
node_collection = db["nodes"] #nodes = name of collection

# What is the disease's name, what are drug names that can treat or palliate this disease, --> showDrugs()
# what are the gene names that cause this disease,  --> showGenes()
# and where this disease occurs?        --> showBodyParts()


###################################################################################

def main_menu():
    global disease_name
    global disease_id
    disease_name = input("Enter Disease Name, or type 'exit' to quit program: ")
    if disease_name == "exit":
        print("Goodbye!")
        sys.exit(0)
    result = node_collection.count_documents({ "name": disease_name}) != 0  #check if disease exists in DB
    if not result:  # if disease doesn't exist, return to start of main menu
        print("Could not find a disease called", disease_name, "\n")
        main_menu()
    print ("Found disease called:", disease_name, "\n")
    showDrugs(disease_name)
    showGenes(disease_name)
    showBodyParts(disease_name)
    main_menu()

###################################################################################

def showDrugs(disease_name):

    drugList = [] # will hold all drugs that match
    global disease_id

    for user_input_result in node_collection.find({ "kind": "Disease", "name": disease_name },
                                                        {"_id": 0}):    # find specific disease
        disease_id = user_input_result['id']   # save id of disease as disease_id
        for drugs_that_match in edge_collection.find({ "target": disease_id,
                        "source": {"$regex": "^Comp", "$options": 'i' }}, {"target": 0}):
            drugList.append(drugs_that_match) #insert all drugs that match disease into array

    print("Drugs that treat of palliate", disease_name, "are:")
    print("-------------------------------------------------------")

    if not drugList:
        print("No data available \n")
    else:
        pprint(drugList)    # print all drugs that match disease
        print("\n\n")

###################################################################################

def showGenes(disease_name):

    geneList = []   # will hold all genes that cause the disease
    global disease_id

    for user_input_result in node_collection.find({ "kind": "Disease", "name": disease_name },
                                                        {"_id": 0}):    # find  disease code
        disease_id = user_input_result['id']   # save id of disease as disease_id

    for genes_that_cause in edge_collection.find({"source": disease_id,
                            "target": {"$regex": "^Gen", "$options": 'i' }}, {"source": 0}):
        geneList.append(genes_that_cause)   #insert all genes that cause disease into array

    print("Genes that cause", disease_name, "are:")
    print("-------------------------------------------------------")

    if not geneList:
        print("No data available \n")
    else:
        pprint(geneList)    # print all genes that cause disease
        print("\n\n")

###################################################################################

def showBodyParts(disease_name):

    bodypartList = []
    global disease_id

    for user_input_result in node_collection.find({ "kind": "Disease", "name": disease_name },
                                                    {"_id": 0}):    # find  disease code
        disease_id = user_input_result['id']   # save id of disease as disease_id

    for bodypartAffected in edge_collection.find({"source": disease_id,
                                            "target": {"$regex": "^A", "$options": 'i' }} ):
        tempStr = bodypartAffected['target']
        for named_body_parts in node_collection.find({"id": tempStr},
                                                    {"id": 0, "kind": 0}):
            bodypartList.append(named_body_parts)
    print ("\n\nWhere in the body does this disease occur:")
    print("-------------------------------------------------------")

    if not bodypartList:
        print("No data available \n")
    else:
        pprint(bodypartList)    #prints all bodyparts that are affected
        print("\n\n")

###################################################################################


main_menu() #run program
