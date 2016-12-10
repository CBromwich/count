import requests
import ast

TOKEN_URL = "https://disneyworld.disney.go.com/authentication/get-client-token/"
HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Authorization": ""
}

URL_ROOT = "https://disneyworld.disney.go.com/api/wdpro/finder-service/public/finder/dining-availability/80007798;entityType=destination"
URL_DATE = "?searchDate="
URL_SIZE = "&partySize=" 
URL_TIME = "&searchTime="

#%3A = colon

TEST_DATE = "2016-12-25"
TEST_SIZE = "2"
TEST_TIME = "17%3A30"

available_reservations = {}

def generate_url(date, size, time):
    return URL_ROOT + URL_DATE + date + URL_SIZE + size + URL_TIME + time
    

def get_response():
    response = requests.get(generate_url(TEST_DATE, TEST_SIZE, TEST_TIME), headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data
    
    
def get_auth_token(token_url):
    token = requests.get(token_url)
    return ast.literal_eval(token.content)["access_token"]
    
def set_auth_token(_dict):
    _dict["Authorization"] = "BEARER " + get_auth_token(TOKEN_URL)


def find_in_obj(obj, condition, path=None):

    if path is None:
        path = []    

    # In case this is a list
    if isinstance(obj, list):
        for index, value in enumerate(obj):
            new_path = list(path)
            new_path.append(index)
            for result in find_in_obj(value, condition, path=new_path):
                yield result 

    # In case this is a dictionary
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = list(path)
            new_path.append(key)
            for result in find_in_obj(value, condition, path=new_path):
                yield result 

            if condition == key:
                new_path = list(path)
                new_path.append(value)
                yield new_path 


                
def match_id():
    for k, v in available_reservations.iteritems():
        with open('id_list.txt', 'r') as f:
            for line in f:
                if k in line:
                    current_line = line.split(",")
                    print(current_line[1].rstrip() + " -"),
                    for i in v:
                        print i + " | ",
                    print "\n"
                    
def populate_dict(_dict):
    data = _dict
    
    for item in find_in_obj(data, 'time'):
        if item[1] not in available_reservations:
            available_reservations[item[1].encode('utf8')] = [item[-1].encode('utf8')]
        else:
            available_reservations[item[1].encode('utf8')].append(item[-1].encode('utf8'))

set_auth_token(HEADERS)
populate_dict(get_response())
match_id()
