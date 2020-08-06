from typing import List
import requests, os, sys, time, datetime
from math import ceil
from datetime import datetime

# setting path for cron job
folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ' ..'))
sys.path.append(folder)
from ping_dashboard.services import location_service

# Setting log date format for all print statements
# Uses timezone set on the server
log_date_time = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def determine_uptime_status(status):
    print(f'{log_date_time} Determining uptime status...')

    if status == 0:
        status = 'PAUSED'
    elif status == 1:
        status = 'NOT CHECKED YET'
    elif status == 2:
        status = 'UP'
    elif status == 8:
        status = 'SEEMS DOWN'
    elif status == 9:
        status = 'DOWN'
    else:
        status = 'UNKNOWN'

    print(f'{log_date_time} Uptime status set to: {status}')
    return status

def check_ms(ping):
    print(f'{log_date_time} Determining status color...')

    status = ""
    if ping is None:
        status = "Timeout Error"
    elif 0 <= ping <= 100:
        status = "green"
    elif 101 <= ping <= 150:
        status = "yellow"
    elif 151 <= ping <= 250:
        status = "orange"
    elif 251 <= ping <= 400:
        status = "red"
    elif ping > 400:
        status = "purple"
    else:
        status = "Your shit ain't working"

    print(f'{log_date_time} Status color set to: {status}')
    return status

def get_monitor_type(type_code):
    print(f'{log_date_time} Determining uptime monitor type...')

    if type_code == '1':
        monitor_type = "HTTP(s)"
    elif type_code == '2':
        monitor_type = "Keyword"
    elif type_code == '3':
        monitor_type = "Ping"
    elif type_code == '4':
        monitor_type = "Port"
    else:
        monitor_type = "Unknown"

    print(f'{log_date_time} Uptime monitor type code {type_code} detected as: {monitor_type}')
    return monitor_type

def create_responses_time_dict(friendly_name, response_times, response_times_values):
    response_times_dict = {}

    i = 0
    for _ in response_times:
        response_times_dict[f'{friendly_name}'] = [f'{response_times[i]}', f'{response_times_values[i]}']
        i += 1

    return response_times_dict

def unix_time_converter(unix_time_stamp):
    return datetime.fromtimestamp(unix_time_stamp)

def uptime_get_account_details() -> int:
    print(f'{log_date_time} Making account detail api call...')

    url = "https://api.uptimerobot.com/v2/getAccountDetails"

    payload = "api_key=[YOUR_API_KEY_HERE]&format=json"
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    # print(response.text)
    monitor_limit_list = extract_values(response.json(), 'monitor_limit')
    total_monitor_up = extract_values(response.json(), 'up_monitors')
    total_monitor_down = extract_values(response.json(), 'down_monitors')
    total_monitor_paused = extract_values(response.json(), 'paused_monitors')
    total_monitor_amount = total_monitor_up[0] + total_monitor_down[0] + total_monitor_paused[0]
    print(f'{log_date_time} Total up monitors set to: {total_monitor_up}')
    print(f'{log_date_time} Total down monitors set to: {total_monitor_down}')
    print(f'{log_date_time} Total paused monitors set to: {total_monitor_paused}')
    print(f'{log_date_time} Total monitor count set to: {total_monitor_amount}')

    print(f'{log_date_time} Account detail api call complete.')
    return total_monitor_amount

def uptime_get_monitors(total_monitor_amount):
    print(f'{log_date_time} Making get monitors api call...')

    total_monitors_possible = total_monitor_amount
    offset = 50
    round_amount = total_monitors_possible / offset
    offset_run_total = ceil(round_amount)
    print(f'{log_date_time} Round amount set to: {round_amount}')
    print(f'{log_date_time} Offset run total set to: {offset_run_total}')


    offset_run_amount = 0
    offset_start_amount = 0

    current_time = int(time.time())
    current_time_minus_1_min = int(current_time - (1 * 60))  # 1 min * 60 seconds

    print(f'{log_date_time} Current run amount: {offset_run_total}')
    while offset_run_amount != offset_run_total:
        url = "https://api.uptimerobot.com/v2/getMonitors"
        # payload = f"api_key=ur330388-aa2b828733412ae717f11b98&format=json&response_times=1&offset={offset_start_amount}"
        payload = f"api_key=[YOUR_API_KEY_HERE]&format=json&response_times=1&response_times_limit=1&offset={offset_start_amount}"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        average_pings = extract_values(response.json(), 'average_response_time')
        friendly_names = extract_values(response.json(), 'friendly_name')
        anonymize_names = extract_values(response.json(), 'id')
        statuses = extract_values(response.json(), 'status')
        url = extract_values(response.json(), 'url')
        monitor_type = extract_values(response.json(), 'type')
        response_times = extract_values(response.json(), 'datetime')
        response_times_values = extract_values(response.json(), 'value')

        # print(f'{log_date_time} friendly_names: {len(friendly_names)}')
        # print(f'{log_date_time} response_times_values: {len(response_times_values)}')

        i = 0
        for friendly_name in friendly_names:
            print(f'{log_date_time} Gathering info on {friendly_name}...')

            location_service.update_server(friendly_name,
                                           f'Customer #{anonymize_names[i]}',
                                           unix_time_converter(response_times[i]),
                                           response_times_values[i],
                                           determine_uptime_status(statuses[i]),
                                           url[i],
                                           check_ms(response_times_values[i]),
                                           monitor_type[i])
            i += 1

            print(f'{log_date_time} Gathering info on {friendly_name} complete.')



        # i = 0
        # for friendly_name in friendly_names:
        #     print(f'friendly name: {friendly_name}')
        #     print(f'type: {get_monitor_type(monitor_type[i])}')
        #     print(f'anonymized name: Cust_{i}')
        #     print(f'average ping: {average_pings[i]}')
        #     print(f'status: {determine_uptime_status(statuses[i])}')
        #     print(f'url: {url[i]}')
        #     print(f'status color: {check_ms(float(average_pings[i]))}')
        #     print(f'repsonse times: {response_times[1]}')
        #     i += 1
        #     print(i)

        offset_run_amount += 1
        offset_start_amount += 50

    print(f'{log_date_time} Get monitors api call complete.')

def uptime_get_friendly_names(total_monitor_amount) -> List:
    total_monitors_possible = total_monitor_amount
    offset = 50
    round_amount = total_monitors_possible / offset
    offset_run_total = ceil(round_amount)

    offset_run_amount = 0
    offset_start_amount = 0

    customers = []
    while offset_run_amount != offset_run_total:
        url = "https://api.uptimerobot.com/v2/getMonitors"
        # payload = f"api_key=ur330388-aa2b828733412ae717f11b98&format=json&response_times=1&offset={offset_start_amount}"
        payload = f"api_key=[YOUR_API_KEY_HERE]&format=json&offset={offset_start_amount}"
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)

        friendly_names = extract_values(response.json(), 'friendly_name')
        for name in friendly_names:
            customers.append(name)

        offset_run_amount += 1
        offset_start_amount += 50

    return customers

def check_for_removed_customers():
    print(f'{log_date_time} Checking for any customers removed from uptime...')

    print(f'{log_date_time} Gathering uptime customers and local db customers.')
    uptime_customers = uptime_get_friendly_names(uptime_get_account_details())
    db_customers = location_service.get_server_urls()
    print(f'{log_date_time} Uptime and local db customers gathered.')

    for db_customer in db_customers:
        if db_customer.id not in uptime_customers:
            print(f'{log_date_time} DB Customer {db_customer} is not in uptime.')
            print(f'{log_date_time} DB Customer {db_customer} is being removed from db.')
            location_service.remove_customer(db_customer.id)
            print(f'{log_date_time} DB Customer {db_customer} has been removed from db.')

    print(f'{log_date_time} Check complete.')

if __name__ == '__main__':
    print(f'{log_date_time} Starting uptime_service.py run...')
    uptime_get_monitors(uptime_get_account_details())
    check_for_removed_customers()
    print(f'{log_date_time} uptime_service.py run complete.')
    # uptime_get_account_details()