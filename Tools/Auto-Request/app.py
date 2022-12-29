import requests

id_start = 31000
id_end = 32000

url_go_api = "localhost:5000/api/v1/query"
url_global_api = "localhost:8000/api/v1/query"


while id_start <= id_end:

    params = {"identifier": str(id_start), "query": "What is Islam?"}

    response = requests.post(url_go_api, json=params)

    print("GET Request: ", id_start)
    print(response)
    print(response.json())
    print("")

    id_start += 1
