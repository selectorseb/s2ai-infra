

Question: What is the s2ap infra health status?
Answer: {
    "name": "get_s2ap_infra_health_status",
    "arguments": {
        "role": "all",
        "s2_inst": "all",
        "time": "last 30 min"
    }
}


Question: Who are you?
Answer: I am co-pilot, an AI assistant developed by Selector Software. How can I assist you today?


Question: packet loss seen by device d8 in arizone?
Answer: get_pingmesh -agent d8 -device d8 -site arizona -time last 30 min
