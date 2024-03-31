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

def get_media_file_info(media_id: str) -> dict[str: int | str | bool | list] | None:
    try:
        response = requests.get(f'{base_url}/media/{media_id}')
        match response.status_code:
            case 200:
                print(f'SUCCESS: Found file')
                return response.json()
            case 400 | 404 | 500:
                print(f'ERROR - status: {response.status_code}, reason: {response.text}')
            case _:
                print(f'ERROR - Uknown')
        return None
    except ConnectionError as e:
            print(f'ERROR: {e}')

def replace_by_index(target_index: int, replacement_id: str) -> None:
        try:    
            response = requests.put(f'{base_url}/media/addmapentry/{target_index}/{replacement_id}')
            match response.status_code:
                case 200:
                    print('SUCCESS: Media file replaced')
                case 400 | 404 | 500:
                    print(f'ERROR - status: {response.status_code}, reason: {response.text}')
                case _:
                    print(f'ERROR - Uknown')
        except ConnectionError as e:
            print(f'Error: {e}')

def replace_media_file_in_map(target_id: int, replacement_id: int) -> None:
    target = search_by_id(target_id)
    replacement = search_by_id(replacement_id)
    if target != None and replacement != None:
        replace_by_index(target['index'], replacement_id)
    else:
        if target == None:
            print(f'ERROR - Target media not found with that ID')
        elif replacement == None:
            print('ERROR - replacement media not found with that ID')

def show_media_names(media_list: list) -> None:
    for med in media_list:
        print(med['name'])

def search_by_name(media_name: str, media_list: list) -> list | None:
    results = []
    if type(media_list) == list:
        for med in media_list:
            if med['name'] == media_name:
                results.append(med)

        if len(results) > 0:           
            print(f'Found {len(results)} file(s) called: {media_name}')
            return results
        else:
            print(f'File not found: {media_name}')

    return None
    
def search_by_id(media_id: str, media_list: list) -> dict[str: int | str] | None:
    if type(media_list) == list:
        for med in media_list:
            if media_id == med['mediaID']:
                print(f'Found {media_id}')
                return med       
        print(f'ERROR - File: {media_id}, Not Found')
    return None



def find_replace(target_name: str, replacement_name: str) -> None:
    replacement = search_by_name(replacement_name)
    target = search_by_name(target_name)
    if target is not None and replacement is not None:
        if len(target) == 1 and len(replacement) == 1:   
            replace_media_file_in_map(target['index'], replacement['index'])
            print(f'SUCCESS: Media file {target["name"]} replaced')
        if len(target) > 1:
            print(f'There are multiple files called {target_name}')
        if len(replacement) > 1:
            print(f'There are multiple files called {replacement_name}')

def find_replace_adv():
    pass

def load_csv():
    pass

def validate_files():
    pass
