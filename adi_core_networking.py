import http.client, json

conn = http.client.HTTPConnection('127.0.0.1:40512')

def get_mediamap():
    try:
        conn.request('GET', '/media')
        response = conn.getresponse()
        print(f' status: {response.status}, reason: {response.reason}')
        return json.loads(response.read().decode())
    except ConnectionError as e:
        print(f'Error: {e}')

def show_media_names(mediamap):
    map = mediamap['mediaFiles']
    for med in map:
        print(med['name'])

get_mediamap()
# show_media_names(get_mediamap())