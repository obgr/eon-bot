import random
import json


def getActivity():
    filepath = "app/data/activities.json"
    with open(filepath) as json_file:
        data = json.load(json_file)
        # print(data)
        random_element = random.choice(list(data.keys()))
        print(random_element)
        random_key = random.choice(list(data[random_element].items()))
        random_key = random.choice(list(data[random_element]['activities']))
        print(random_key)
        # for station in data["liveweer"]:
    return random_element, random_key


getActivity()
