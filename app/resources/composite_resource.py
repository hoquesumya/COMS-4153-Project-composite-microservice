from typing import Any

from framework.resource.base_resource import BaseResource

from app.models.studycompositionmodel import CompositeResponse
from app.services.service_factory import ServiceFactory
import logging
import requests
from requests.exceptions import HTTPError, RequestException
logging.basicConfig(level=logging.INFO)

class CompositeResource:
    def __init__(self):
        #super().__init__(config)
        service = ServiceFactory()
        self.config = service.get_service("CompositeResourceService")
        self.user_config = self.config.get_user_config()
        self.chat_config = self.config.get_chat_config()
        self.study_config = self.config.get_study_config()
        self.course_config = self.config.get_couuse_config()
    
    #this will perform the rest call
    def get_user(self, user_id:str):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            response = requests.get(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.user_config, user_id)
            return(status_code, data)
        
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

    
    def post_user(self, user_id: str, token:str):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            response = requests.post(url, token)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.user_config, user_id)
            return(status_code, data)
        
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
      
        print(self, user_id, self.user_config)

    def get_all_users(self, params:dict):
        url = f"{self.user_config}/users/"
        try:
            response = requests.get(url, params)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            return(status_code, data)
        
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

   
    def delete_user(self, user_id: str):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.user_config, user_id)
            return(status_code, data)
        
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
        
        print(self, user_id, self.user_config)
   
    #......starting the study group apis call......
    def get_group(self,group_id:str):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.study_config, group_id)
            return(status_code, data)
        

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

       
    def create_group(self, group_data:dict):
        url = f"{self.study_config}/study-group/"
    
        try:
            response = requests.post(url, group_data)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.study_config)
            return(status_code, data)
        

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
       

    def delete_group(self, group_id:str):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            response = requests.delete(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.study_config, group_id)
            return(status_code, data)
        

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

        print(self.study_config, group_id)
    def update_group(self, group_id:str):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            response = requests.put(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.study_config, group_id)
            return(status_code, data)
        

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
        print(self.study_config, group_id)
    
    def get_all_group(self):
         
        print(self.study_config)
        url = f"{self.study_config}/study-group"
        try:
            response = requests.get(url)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            return(status_code, data)
        

        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
    
    #.....staring thr course enrollment service....
    def get_course(self, user_id:str):
        print(self.course_config, user_id)
    #......staring the chat service.....
    def get_chat(self, chat_id:int):
        print(self.chat_config, chat_id)
    
    def get_all_chat(self):
         print(self.chat_config)
    
    def post_chat(self, conversation:dict):
        print(self.chat_config)

    def delete_chat(self,chat_id:int):
        print(self.chat_config, chat_id)
    
    def update_chat(self, chat_id, conversation: dict):
        print(self.chat_config, chat_id)
        
    

    




    
    
