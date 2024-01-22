import json


with open('script.json') as f:
    scenes = json.load(f)
    

class QuestEngine:
    def __init__(self):
        pass
    
    def number_split(self, number):
        number = number.split('.')
        return number[0], number[1]
    
    
    def get_scene(self, number):
        location, number = self.number_split(number)
        if location not in scenes or number not in scenes[location]['scenes']:
            print(location, number)
            return "END", None, None, None
        name = scenes[location]['scenes'][number]["name"]
        name = f"Локация: {scenes[location]['name']}" + "\n\n\n" + name
        return name, scenes[location]['scenes'][number]["description"], scenes[location]['scenes'][number]["image"], scenes[location]['scenes'][number]["options"]
    
    
    def get_options(self, number):
        location, number = self.number_split(number)
        return scenes[location]['scenes'][number]["options"]
    
    
    def get_transition(self, number, transition):
        location, number = self.number_split(number)
        return scenes[location]['scenes'][number]["transitions"][transition]
    
    
    def get_save_data(self, number):
        location, number = self.number_split(number)
        try:
            return scenes[location]['scenes'][number]["save_data"]
        except KeyError:
            return 'None'
