import requests
import json
import datetime
import time


url = 'https://api.inboxevo.com/campaigns/overview'
headers = {
    'authority': 'api.inboxevo.com',
    'accept': 'application/json, text/plain, text/plain;charset=UTF-8',
    'accept-language': 'en-RO,en-US;q=0.9,en;q=0.8,zh-TW;q=0.7,zh;q=0.6,de;q=0.5,ro;q=0.4',
    'authorization': 'Basic Gzsa1UFOUVnd8C1LXd5PZdy76mENJjj3rRxGLnI20StDlF430wzbKjni76TfXcSb0hUFo1BNr4sXnSBDWjkkAkxvj0sm88Wx4Ig2zDYDNgtmlqE3Mal6lfmobl3lR4cR',
    'content-type': 'application/json',
    'origin': 'https://members.inboxevo.com',
    'referer': 'https://members.inboxevo.com/',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
params = {
    'dateFrom': 1715146654000,
    'dateTo': 1715233054000,
    'tags': ['663b74b75956e13053436243'],
    'computeCombinationsStats': True,
    'max': 2,
    'ignoreRecipientThreshold': 200,
    'computePmtaLogsErrCount': True
}
minute = 60000
hour = 60 * minute
day = 24 * hour
week = 7 * day

#search_param = 'draft_name'
search_param = 'suffix'
search_value = 'crinemin.com'

def make_mint_request() -> json:
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_campaign_list():
    test_dict = make_mint_request()
    with open('test.json', "w") as f:
        json.dump(test_dict,f,indent=4)

    campaign_list = test_dict['campaigns']
    return campaign_list

def get_metadata_elements(data):
    root_dict = data['metadata']
    temp_dict = root_dict['lists'][0]
    # print(temp_dict[0])
    list_name = temp_dict['listName']
    set_name = root_dict['tags']['setName']
    draft_name = root_dict['tags']['draftName']
    return list_name, set_name, draft_name

def get_campaign_direct_values(data):
    obj_key_list = ['id', 'suffix', 'recipients', 'delivered', 'opened','clicked', 'unsubscribed']
    temp_dict = {}
    for _ in obj_key_list:
        temp_dict[_] = data[_]
    return temp_dict

def form_result_dict(data):
    temp_dict = {}
    temp_dict['list_name'], temp_dict['set_name'], temp_dict['draft_name'] = get_metadata_elements(data)
    direct_dict = get_campaign_direct_values(data)
    temp_dict.update(direct_dict)
    temp_dict['creationTime'] = data['creationTime']
    return temp_dict

def process_campaign_list(campaign_list):
    result_list = []
    for _ in campaign_list:
        result_list.append(form_result_dict(_))
    return result_list

def return_filtered_list(campaign_list, search_value, search_param):
    campaign_list = process_campaign_list(campaign_list)
    sorted_campaign_list = sorted(campaign_list, key=lambda k: k['creationTime'], reverse=True)
    filtered_list = [x for x in sorted_campaign_list if x.get(search_param, "") == search_value]
    return filtered_list

def convert_time(input_time):
    timestamp_milliseconds = input_time
    timestamp_seconds = timestamp_milliseconds / 1000
    date_time = datetime.datetime.utcfromtimestamp(timestamp_seconds)
    return date_time

def get_current_time():
    current_time_unix_seconds = time.time()
    current_time_unix_milliseconds = int(current_time_unix_seconds * 1000)
    return current_time_unix_milliseconds

def get_results_since(filtered_list, time_delta):
    current_time = get_current_time()
    threshold_time = current_time - time_delta
    results_since = [x for x in filtered_list if x['creationTime'] > threshold_time]
    return results_since




def main():
    campaign_list = get_campaign_list()
    print (campaign_list)
    # filtered_list = return_filtered_list(campaign_list, search_value, search_param)
    # start_time = get_current_time()
    # filtered_list = get_results_since(filtered_list, 3 * day)
    # print(len(filtered_list))
    # for _ in filtered_list:
    #     print(_)
    # end_time = get_current_time()

    # print("Start time: {} \nEnd time: {} \nTime elapsed: {}".format(start_time, end_time, end_time - start_time))

    
    

if __name__ == '__main__':
    main()