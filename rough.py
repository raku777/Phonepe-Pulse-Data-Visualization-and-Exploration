import json
import requests

def change_state_name():
     url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
     response = requests.get(url)
     data = json.loads(response.content)
     state_name = [i['properties']['ST_NM'] for i in data['features']]
     state_name.sort()
     return state_name

print(change_state_name())