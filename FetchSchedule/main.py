import requests
import datetime
import secret

URL_ROOT = secret.url
URL_START = "&start=" + datetime.date.today().strftime("%m/%d/%Y") #ensure the start time is always today
URL_END = "&end=" + (datetime.date.today() + datetime.timedelta(days=14)).strftime("%m/%d/%Y") #set start time to 14 days from today

def get_response():
    response = requests.get(URL_ROOT + URL_START + URL_END)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError:
        print "Response type was " + response.headers['content-type']
        
    return data
    

    
def parse_data(data):
    inner_list = data.values()[3]
    for i in range(len(inner_list)):
        shift_info = inner_list[i]['shifts']
        if (len(shift_info) > 0):
            print shift_info[0]['startTime'] + " -" + shift_info[0]['endTime'][10:] +  " " + shift_info[0]['positionDescription']
        

parse_data(get_response())