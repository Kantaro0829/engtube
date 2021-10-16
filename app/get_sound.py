import requests
import base64

class GetSoundOfEnglish():
    def __init__(self, words_list):
        self.default_url1 = "https://translate.google.com/translate_tts"
        self.words_list = words_list  #音声ファイルがほしい英単語のリスト
        self.default_params = {
            "ie": "UTF-8",
            "client": "tw-ob",
            "tl": "en",
            "total": "1",
            "idx": "0"
        }#q, textlen　は後で追加
        self.success_list = []
        self.failure_list = []
    def get_sound(self):

        for word in self.words_list:
            temp_dict = {}           
            self.default_params['q'] = word
            self.default_params['textlen'] = len(word)
            response = requests.get(self.default_url1, params=self.default_params)

            if response.status_code is not 200:
                self.failure_list.append(word)
            
            temp_dict["english"] = word 
            print("-------------------------------------------------")
            print(response.content)
            print("-------------------------------------------------")               
            temp_dict["sound"] = base64.b64encode(response.content).decode()
            print("?????????????????????????????????????????????????")
            #temp = temp_dict["sound"].encode("utf-8")
            print(temp_dict['sound'])
            print("????????????????????????????????????????????????")
            print("###############################################33")
            print(base64.b64decode(temp_dict["sound"]))
            print("###############################################33")
            if base64.b64decode(temp_dict["sound"]) == response.content:
                print("goooooooooooooooooooooooooooooooooooooood")
            else:
                print("baaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaad")
            self.success_list.append(temp_dict)
        
        return self.success_list, self.failure_list

    

            

