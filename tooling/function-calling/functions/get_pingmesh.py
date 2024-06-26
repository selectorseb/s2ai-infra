import json
import requests
from time import strftime, localtime


def get_pingmesh(agent: str = '', device: str = '', site: str = '', time: str = "last 30 min") -> str:
    """
    Function to get pingmesh synthetic metrics like latency and packet loss

    Parameters:
    - agent (str): pingmesh agents which originate the ping packets. These are sources
    - device (str): The starting device. This is the source endpoint of the graph. Graph connections start from this device
    - site: A datacenter site with all devices. e.g - dnvr1, ari1, bpwifi
    - time (str): The time range, e.g., 'last 1 day', 'last 30 minutes' or 'last 2 days'. Default is 'last 30 min'.

    Returns:
    - str: Returns the state of network topology. How devices are connected to each other
    """

    selector_url = "https://s2m.selector.ai/api/collab2-slack/rules/command"
    api_key = "70fN07ny3x3sENNwEO2o8cJr"
    query_to_run = '#select layer2_topology as topology '
    query_to_run = query_to_run + ' s2_inst=.*, '
    query_to_run = query_to_run + 'role=.*, '
    query_to_run = query_to_run + 's2ap_infra_health>=1, '

    query_to_run = query_to_run + ' for ' + time

    print(query_to_run)
    headers = dict()
    headers["Authorization"] = "Bearer " + api_key
    headers["Content-Type"] = "application/json"
    json_data = {
        'command': query_to_run,
        'utc_offset_sec': -25200,
    }
    return "No result returned."
    response = requests.post(selector_url, headers=headers, json=json_data)
    # Decode json response
    result = json.loads(response.text)

    if len(result['data']) == 0:
        return "No result returned."
    output = "Following s2ap infra health status reported: \n"
    for item in (result['data']):
        if s2_inst != 'all' and item['s2_inst'] != s2_inst:
            continue

        if role != 'all' and item['role'] != role:
            continue

        entry = " - instance:" + item['s2_inst']
        entry = entry + " role:" + item['role']
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
