import json
import requests
from time import strftime, localtime


def get_s2ap_infra_instance_kpi_status(role: str = 'all', s2_inst: str = 'all', kpi_name: str = 'all', time: str = "last 30 min") -> str:
    """
    Function to get status of s2ap infra instance kpi state

    Parameters:
    - role (str): The role, e.g., 'prod', 'staging' or 'poc'.
    - s2_inst (str): The instance name.
    - kpi_name (str): The kpi name, e.g., 'bist' or 'pv'. Default is 'all'.
    - time (str): The time range, e.g., 'last 1 day', 'last 30 minutes' or 'last 2 days'. Default is 'last 30 min'.

    Returns:
    - str: Returns status of s2ap infra instance kpi state.
    """

    selector_url = "https://s2m.selector.ai/api/collab2-slack/rules/command"
    api_key = "70fN07ny3x3sENNwEO2o8cJr"
    query_to_run = '#select s2ap_infra_health_by_kpi as honeycomb show-by role, s2_inst, kpi_name'

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
        return "No result returned."
    output = "Following s2ap kpi health status reported: \n"
    for item in (result['data']):
        if s2_inst != 'all' and item['s2_inst'] != s2_inst:
            continue

        if role != 'all' and item['role'] != role:
            continue

        if kpi_name != 'all' and item['kpi_name'] != kpi_name:
            continue

        entry = " - instance:" + item['s2_inst']
        entry = entry + " role:" + item['role']
        entry = entry + " kpi:" + item['kpi_name']
        # if item['s2ap_infra_health'] is 1 then return healthy else return unhealthy
        if item['s2ap_infra_health_by_kpi'] >= 1:
            entry = entry + " kpi health:violating"
        else:
            entry = entry + " kpi health:good"
        entry = entry + " \n"
        output = output + entry
    return output

# Test function
# print(get_s2ap_infra_instance_kpi_status())