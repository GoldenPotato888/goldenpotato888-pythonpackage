import requests

def format_time(n: int) -> str:
    centiseconds = n % 100
    seconds = (n % 6000) // 100
    minutes = (n % 360000) // 6000
    if minutes == 0:
        if centiseconds < 10:
            return f"{seconds}.0{centiseconds}"
        else:
            return f"{seconds}.{centiseconds}"
    else:
        if seconds < 10:
            if centiseconds < 10:
                return f"{minutes}:0{seconds}.0{centiseconds}"
            else:
                return f"{minutes}:0{seconds}.{centiseconds}"
        else:
            if centiseconds < 10:
                return f"{minutes}:{seconds}.0{centiseconds}"
            else:
                return f"{minutes}:{seconds}.{centiseconds}"

def get_pr_single(WCA_ID: str, EVENT_NAME: str) -> str:
    allowed_events = ['222', '333', '444', '555', '666', '777', '333bf', '333fm', '333oh', '444bf', '555bf', 'clock', 'minx', 'pyram', 'skewb', 'sq1']
    if EVENT_NAME not in allowed_events:
        return 'ERROR: Event Name must be one of the following: ' + str(allowed_events)
    try: 
        response = requests.get(f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{WCA_ID}.json")
        singles = response.json()['rank']['singles']
    except:
        return 'ERROR: Could not fetch WCA data.'
    for i in range(len(singles)):
        if singles[i]['eventId'] == EVENT_NAME:
            if EVENT_NAME != '333fm':
                return format_time(singles[i]['best'])
            else:
                return singles[i]['best']
    return f'ERROR: {WCA_ID} does not have this result.'

def get_pr_average(WCA_ID: str, EVENT_NAME: str) -> str:
    allowed_events = ['222', '333', '444', '555', '666', '777', '333bf', '333fm', '333oh', '444bf', '555bf', 'clock', 'minx', 'pyram', 'skewb', 'sq1']
    if EVENT_NAME not in allowed_events:
        return 'ERROR: Event Name must be one of the following: ' + str(allowed_events)
    try: 
        response = requests.get(f"https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{WCA_ID}.json")
        averages = response.json()['rank']['averages']
    except:
        return 'ERROR: Could not fetch WCA data.'
    for i in range(len(averages)):
        if averages[i]['eventId'] == EVENT_NAME:
            if EVENT_NAME != '333fm':
                return format_time(averages[i]['best'])
            else:
                return averages[i]['best'] / 100
    return f'ERROR: {WCA_ID} does not have this result.'

def get_wca_id_data(WCA_ID: str) -> str:
    try:
        response = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/persons/{WCA_ID}.json')
        return response.json()
    except:
        return 'ERROR: Could not fetch WCA data.'

def get_competition_data(COMPETITION_ID: str) -> str:
    try:
        response = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/competitions/{COMPETITION_ID}.json')
        return response.json()
    except:
        return 'ERROR: Could not fetch WCA data.'

def get_wr(EVENT_NAME: str, SINGLE_OR_AVERAGE: str) -> str:
    allowed_events = ['222', '333', '444', '555', '666', '777', '333bf', '333fm', '333oh', '444bf', '555bf', 'clock', 'minx', 'pyram', 'skewb', 'sq1']
    if EVENT_NAME not in allowed_events:
        return "ERROR: Event Name must be one of the following: " + str(allowed_events)
    if SINGLE_OR_AVERAGE not in ['single', 'average']:
        return "ERROR: WR type must be either single or average."
    response = requests.get(f'https://raw.githubusercontent.com/robiningelbrecht/wca-rest-api/master/api/rank/world/{SINGLE_OR_AVERAGE}/{EVENT_NAME}.json')
    if EVENT_NAME != '333fm' or SINGLE_OR_AVERAGE == 'average':
        return format_time(response.json()['items'][0]['best'])
    else:
        return response.json()['items'][0]['best']


print(get_wca_id_data('2023METH01'))