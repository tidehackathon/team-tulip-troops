from elasticsearch import Elasticsearch

# Found in the 'Manage this deployment' page
CLOUD_ID = "3b7c7ef1ec744d898bf05ea60d28d2de:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDVmNWNkY2UyOTFlMjQ3YWE5YjhmMWZlNjgyM2Y2NTE4JDRjOTY5N2YzYmY2ZjQwY2I5MmU4NWNkY2UzNjRlZjU1"

# Found in the 'Management' page under the section 'Security'
API_KEY = "ZjNHMFRJWUJETGVSREluRXdLVnY6VGl1d3NPQjdSRWF5aU1aQVRFSkRnQQ=="


def get_elastic_data():

    # Create the client instance
    es = Elasticsearch(
        cloud_id=CLOUD_ID,
        api_key=API_KEY,
    )

    resp = es.search(index="news_articles", query={"match_all": {}})
    print("Got %d Hits:" % resp['hits']['total']['value'])
    for hit in resp['hits']['hits']:
        print("%(published)s %(headlines)s: %(articles)s %(news_paper)s" % hit["_source"])


get_elastic_data()