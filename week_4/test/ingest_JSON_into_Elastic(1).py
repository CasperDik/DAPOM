import datetime
from elasticsearch import Elasticsearch


def ingest_from_file(file_name: str, index_name: str, template: dict, properties: dict):
    elasticsearch_cluster_object = Elasticsearch(hosts="http://elastic:vivo&Bok@localhost:9200")

    elasticsearch_cluster_object.indices.delete(index=index_name, ignore=[400, 404])
    elasticsearch_cluster_object.indices.create(index=index_name, settings=template, mappings=properties)
    print("empty index", index_name, "created")

    with open(file_name) as file:
        docs = [line.strip() for line in file]
    print(file_name, "file reading ended")

    start_time = datetime.datetime.now()
    print("start indexing at", start_time)

    for doc in docs:
        print(doc)
        elasticsearch_cluster_object.index(index=index_name, document=doc)

    total_time = datetime.datetime.now() - start_time
    print('finished after', total_time)
# ----------------end of the function------------------
#
# to use the ingestion more effectively, please use the function above
# but be careful what kind arguments you prepare for it. Commented, an example of
# thef unction call is presented just below and is doing the same as the code after (from line 43).

# EXAMPLE OF FUNCTION CALL (commented)
# an argument is initially prepared in a variable for the argument list
prop = {
    "properties": {
        "date_of_birth": {
            "type": "date",
            "format": "dd/MM/yyyy"
        }
    }
}
ingest_from_file(file_name="employee_list.json",
                 index_name="employees",
                 template={"number_of_shards": 3},
                 properties=prop)

#---------------CODE FOR INITIAL STUDY---------------------------------
#--------USE THE FUNCTION FOR YOUR CODE--------------------------------

# __if you run the script below and comment out the function call above, only the code below will be executed.
# if you installed the Elasticsearch minimal security, you have to indicate the
# user = elastic, and password = [in my own case] vivo&Bok, yours is probably different, see the syntax below

# es = Elasticsearch(hosts="http://elastic:vivo&Bok@localhost:9200")
#
# # to make sure that you don't have an error, delete an eventual index with the same name
# es.indices.delete(index='employees', ignore=[400, 404])
#
# # (re)create empty employee index
# template = {
#     "number_of_shards": 3
# }
# props = {
#     "properties": {
#         "date_of_birth": {
#             "type": "date",
#             "format": "dd/MM/yyyy"
#         }
#     }
# }
#
# es.indices.create(index='employees', settings=template, mappings=props)
# print("empty index 'employee' created")
#
# with open("employee_list.json") as file:
#     docs = [line.strip() for line in file]  # this the quickest way to read a text file line by line
# print("file reading ended")
#
# # measure how long it takes to index the elements of the docs list into the employee index
# start_time = datetime.datetime.now()
# print("start indexing at", start_time)
#
# for doc in docs:
#     print(doc)
#     es.index(index="employees", document=doc)  # index one by one (the most time consuming part)
#
# total_time = datetime.datetime.now() - start_time
# print('finished after', total_time)

# you can check now the _count parameter of the employees index via the browser, using the string
# 'http://elastic:<your password here>@localhost:9200/employees/_count', or via the Kibana console
# with the 'GET employees/_count' request (used without the apostrophes, of course)
