import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


def flatten_array_fields(document):
    flattened_document = {}
    for key, value in document.items():
        if isinstance(value, list):
            for i in range(len(value)):
                flattened_document[f"{key}[{i}]"] = value[i] if i < len(value) else ""
        else:
            flattened_document[key] = value
    return flattened_document

def mongo_to_excel(db_name, collection_name, output_file):
    client = MongoClient("mongodb://root:Edubild_123@mongodb:27017")
    db = client[db_name]
    collection = db[collection_name]

    documents = list(collection.find())
    flattened_documents = [flatten_array_fields(doc) for doc in documents]
    df = pd.DataFrame(flattened_documents)

    df.to_excel(output_file, index=False)

    print(f"Data has been written to {output_file}")



# db_name = 'scraped'
# collection_name = 'scrap_info'
# output_file = f'./Excel_Data/{collection_name}.xlsx'  #change name accordingly
# mongo_to_excel(db_name, collection_name, output_file)