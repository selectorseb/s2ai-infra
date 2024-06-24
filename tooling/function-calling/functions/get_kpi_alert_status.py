import json
import requests
from time import strftime, localtime


def get_kpi_alert_status(kpi_name: str = 'all', alert_state: str = 'firing', priority: str = 'P1', time: str = "last 7 day") -> str:
    """
    Function to retrieve kpi alert state status

    Parameters:
    - kpi_name (str): The kpi name, e.g., 'bist' or 'pv'. Default is 'all'.
    - alert_state (str): The alert state, e.g., 'firing' or 'resolved'. Default is 'firing'.
    - priority (str): The priority, e.g., 'P1' or 'P2'. Default is 'P1'.
    - time (str): The time range, e.g., 'last 1 day' or 'last 2 days'. Default is 'last 1 day'.

    Returns:
    - str: Returns the state of the kpi alert status or an error message.
    """

    selector_url = "https://s2m.selector.ai/api/collab2-slack/rules/command"
    api_key = "70fN07ny3x3sENNwEO2o8cJr"
    query_to_run = '#select starttime, alertname, labels.s2_inst:s2_inst, labels.kpi_name:kpi, status in alerts_state as table where '
    if alert_state == 'firing':
        query_to_run = query_to_run + 'alertstate=firing, '
    else:
        query_to_run = query_to_run + 'alertstate=resolved, '
    
    if priority.startswith('P'):
        query_to_run = query_to_run + 'priority=' + priority + ', '
    else:
        query_to_run = query_to_run + 'priority=.*, '
    
    if kpi_name == 'all':
        query_to_run = query_to_run + 'labels.kpi_name=.*, '
    else:
        query_to_run = query_to_run + 'labels.kpi_name=' + kpi_name + ', '
    
    query_to_run = query_to_run + ' for ' + time 

    print(query_to_run)
    headers = dict()
    headers["Authorization"] = "Bearer " + api_key
    headers["Content-Type"] = "application/json"
    json_data = {
        'command': query_to_run,
        'utc_offset_sec': -25200,
    }
    response = requests.post(selector_url, headers=headers, json=json_data)
    # Decode json response
    result = json.loads(response.text)
    
    if len(result['data']) == 0:
        return "No kpi alerts found."
    output = "Following kpi alerts status reported: \n"
    for item in (result['data']):
        if isinstance(item['labels']['kpi_name'], list):
            kpi_result = "  - kpi name:" + ','.join(item['labels']['kpi_name']) 
        else:
            kpi_result = "  - kpi name:" + item['labels']['kpi_name']

        if isinstance(item['labels']['s2_inst'],list):
            kpi_result = kpi_result + " instance:" + ','.join(item['labels']['s2_inst'])
        else:
            kpi_result = kpi_result + " instance:" + item['labels']['s2_inst']

        kpi_result = kpi_result + " status:" + item['status'] + " starttime:"+ strftime('%Y-%m-%d %H:%M:%S', localtime(item['starttime'])) + " alertname:" + item['alertname'] +" \n"
        output = output + kpi_result
    output = output + "\nSummarize the following output in 100 words:\n\n"
    return output

# Test function
# print(get_kpi_alert_status())