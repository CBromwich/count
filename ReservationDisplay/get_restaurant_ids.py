import requests
from main import HEADERS
""" Parse restaurant list JSON to match restaurant ids to names """

URL = "https://disneyworld.disney.go.com/api/wdpro/bulk-service/snapshot/WDW-finder-restaurant"



def get_ids():
    response = requests.get(URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
        
    innerlist = data.values()[0]
    with open("id_list.txt", "w") as f:
        for i in range(len(innerlist)):
            f.write(innerlist[i]["id"].encode('utf8') + ", " + innerlist[i]["name"].encode('utf8') + "\n")
            
get_ids()

