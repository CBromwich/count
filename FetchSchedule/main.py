import requests
import datetime
import secret

URL_ROOT = secret.url #don't sniff my secrets plz
URL_START = "&start=" + datetime.date.today().strftime("%m/%d/%Y") #ensure the start time is always today
URL_END = "&end=" + (datetime.date.today() + datetime.timedelta(days=14)).strftime("%m/%d/%Y") #set end time to 14 days from today

def get_response():
    """ Makes a request to the API URL and convert parse the JSON return """
    response = requests.get(URL_ROOT + URL_START + URL_END)
    response.raise_for_status()
    try:
        data = response.json()
    except ValueError:
        print "Response type was " + response.headers['content-type'] #in case something goes wrong and the content type is not JSON
    return data
    
def parse_data(data):
    """ Comb through returned JSON and find pertinent information """
    inner_list = data.values()[3]
    for i in range(len(inner_list)):
        shift_info = inner_list[i]['shifts']
        if (len(shift_info) > 0):
            print shift_info[0]['startTime'] + " -" + shift_info[0]['endTime'][10:] +  " " + shift_info[0]['positionDescription']
        

parse_data(get_response())