import requests, json

base_url = 'http://127.0.0.1:40512'

def get_mediamap() -> None:
    try:
        response = requests.get(f'{base_url}/media/map')
        if response.status_code == 200:
            media_json = response.json()
            # Used to creat the test .json entries
            # with open('json_get_media_test.json', 'w') as f:
            #     f.write(response.text)
            return media_json
        else:
            print(f'ERROR - status: {response.status_code}, reason: {response.text}')

    except ConnectionError as e:
        print(f'Error: {e}')

def show_media_names(json: list) -> None:
    for med in json:
        print(med['name'])

def search_by_name(media_name: str, json: list) -> list | None:
    results = []
    if type(json) == list:
        for med in json:
            if med['name'] == media_name:
                results.append(med)

        if len(results) > 0:           
            print(f'Found {len(results)} file(s) called: {media_name}')
            return results
        else:
            print(f'File not found: {media_name}')

    return None
    
            

def replace(target_id: int, replacement_id: int) -> bool:
    valid_target = search_by_name(target)
    if  valid_target != True:
        print(f'ERROR - File: {target}, Not Found')


def find_replace():
    pass

def find_replace_adv():
    pass

def load_csv():
    pass

def validate_files():
    pass
