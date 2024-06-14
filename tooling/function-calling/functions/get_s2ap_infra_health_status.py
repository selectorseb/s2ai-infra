import json
import requests
from time import strftime, localtime


def get_s2ap_infra_health_status(role: str = 'all', s2_inst: str = 'all', s2ap_infra_health: str = 'violating', time: str = "last 1 day") -> str:
    """
    Function to s2ap infra health status

    Parameters:
    - role (str): The role, e.g., 'prod', 'staging' or 'poc'. Default is 'prod'.
    - s2_inst (str): The instance name.
    - s2ap_infra_health (str): The s2ap infra health state, e.g., 'violating' or 'unhealthy' when value is '2' else 'healthy' when value is '1'. Default is 'violating'.
    - time (str): The time range, e.g., 'last 1 day', 'last 30 minutes' or 'last 2 days'. Default is 'last 1 day'.

    Returns:
    - str: Returns the state of the s2ap infra health status or an error message.
    """

    selector_url = "https://s2m.selector.ai/api/collab2-slack/rules/command"
    api_key = "70fN07ny3x3sENNwEO2o8cJr"
    query_to_run = '#select s2ap_infra_health as honeycomb show-by s2_inst, role where '
    if s2_inst == 'all':
        query_to_run = query_to_run + ' s2_inst=.*, '
    else:
        query_to_run = query_to_run + ' s2_inst=' + s2_inst + ', '
    
    if role == 'all':
        query_to_run = query_to_run + 'role=.*, '
    else:
        query_to_run = query_to_run + 'role=' + role + ', '

    if s2ap_infra_health == 'violating':
        query_to_run = query_to_run + 's2ap_infra_health>=2, '
    else:
        query_to_run = query_to_run + 's2ap_infra_health<=1, '

    query_to_run = query_to_run + ' for ' + time 

    # print(query_to_run)
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
        return "No result returned."
    output = "Following s2ap infra health status reported: \n"
    for item in (result['data']):
        entry = "  - role:" + item['role']
        entry = entry + " instance:" + item['s2_inst']
        # if item['s2ap_infra_health'] is 1 then return healthy else return unhealthy
        if item['s2ap_infra_health'] == 1:
            entry = entry + " health:good"
        else:
            entry = entry + " health:violating"
        entry = entry + " \n"
        output = output + entry
    return output

# Test function
# print(get_s2ap_infra_health_status())