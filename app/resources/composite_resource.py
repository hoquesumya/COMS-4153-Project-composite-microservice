from typing import Any

from framework.resource.base_resource import BaseResource
from fastapi.responses import JSONResponse
import asyncio
from app.models.studycompositionmodel import CompositeResponse
from app.services.service_factory import ServiceFactory
import logging
import requests
import aiohttp
from requests.exceptions import HTTPError, RequestException
logging.basicConfig(level=logging.INFO)
from asyncio.exceptions import TimeoutError

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
            print("calling get user")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            print(self.user_config, user_id)
            return response
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

    
    def post_user(self, user_id: str, token:str):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            response = requests.post(url, token, timeout=5)
            response.raise_for_status()
            status_code = response.status_code
            return response
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
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
            response = requests.get(url, params, timeout=5)
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            return JSONResponse(
                content={"error": "Something is wrong"},
                status_code=response.status_code
            )
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

   
    def delete_user(self, user_id: str):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            response = requests.delete(url, timeout=5)
            response.raise_for_status()
            status_code = response.status_code
            data = response.json()
            print(self.user_config, user_id)
            return(status_code, data)
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
        
        print(self, user_id, self.user_config)
    
    
    async def get_user_sync_internal(self, user_id:str):
        url = f"{self.user_config}/users/{user_id}/profile"

        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(url)
                response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
                return response
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                print(f"Client error occurred: {client_err}")
                return JSONResponse(
                    content={"error": f"Client error occurred: {client_err}"},
                    status_code=500
                )
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return JSONResponse(
                    content={"error": f"An unexpected error occurred: {err}"},
                    status_code=500
                )

    
   
    #......starting the study group apis call......
    def get_group(self,group_id:str):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": f"Server error occurred:"},
                    status_code=500
                )
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return JSONResponse(
                    content={"error": f"request error occurred:"},
                    status_code=400
                )
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

       
    async def create_group(self, group_data: dict):
        url = f"{self.study_config}/study-group/"
        async with aiohttp.ClientSession() as client:
            try:
                response = await client.post(url, json=group_data, timeout=5)
                response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
                return response
            
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                print(f"Client error occurred: {client_err}")
                return JSONResponse(
                    content={"error": f"Client error occurred: {client_err}"},
                    status_code=500
                )
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return JSONResponse(
                    content={"error": f"An unexpected error occurred: {err}"},
                    status_code=500
                )
    
    async def delete_group_async(self, group_id:int):
        url = f"{self.study_config}/study-group/{group_id}"
        async with aiohttp.ClientSession() as client:
            try:
                response = await client.delete(url, timeout=15)
                response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
                return response
            
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                print(f"Client error occurred: {client_err}")
                return JSONResponse(
                    content={"error": f"Client error occurred: {client_err}"},
                    status_code=500
                )
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return JSONResponse(
                    content={"error": f"An unexpected error occurred: {err}"},
                    status_code=500
                )

    def delete_group(self, group_id:int):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            response = requests.delete(url, timeout=5)
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

        print(self.study_config, group_id)
    
    def update_group(self, group_id:int, update_data:dict):
        url = f"{self.study_config}/study-group/{group_id}"
        try:
            print("staring the udate", update_data)
            response = requests.put(url, json=update_data, timeout=15)
            print(response.json())
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        
        except HTTPError as http_err:
            
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                content={"error": "an error occurred"},
                status_code=response.status_code
            )
        
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
        print(self.study_config, group_id)
    
    def get_all_group(self):
        print(self.study_config)
        url = f"{self.study_config}/study-group"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
    
    #.....staring thr course enrollment service....
    def get_course(self, user_id:str, token :str):
        url = f"{self.course_config}/users/{user_id}/courses"
        try:
            response = requests.get(url, token)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
       
        print(self.course_config, user_id)
    
    def get_all_students_per_course(self, course_code: str, token: str):
        url = f"{self.course_config}/course/{course_code}/students"
        try:
            response = requests.get(url, token)
            response.raise_for_status()
            return response
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

    #......staring the chat service.....
    def get_chat(self, chat_id:int):
        url = f"{self.chat_config}/conversations/{chat_id}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": f"Server error occurred:"},
                    status_code=response.status_code
                )

        print(self.chat_config, chat_id)

    
    def get_all_chat(self):
        print(self.chat_config)
        url = f"{self.chat_config}/conversations/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": f"Server error occurred:"},
                    status_code=response.status_code
                )

    #this will be the event driven
    def post_chat(self, conversation:dict):
        print(self.chat_config)
        url = f"{self.chat_config}/conversations/"
        try:
            response = requests.post(url, json=conversation, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": response.json()},
                    status_code=response.status_code
            )


    def delete_chat(self,chat_id:int):
        url = f"{self.chat_config}/conversations/{chat_id}"
        try:
            response = requests.delete(url, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": response.json()},
                    status_code=response.status_code
            )

        print(self.chat_config, chat_id)

    
    def update_chat(self, chat_id, conversation: dict):
        url = f"{self.chat_config}/conversations/{chat_id}"
        try:
            print("conversation is:", conversation)
            response = requests.put(url, json=conversation, timeout=5)
            response.raise_for_status()
            return response
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                    content={"error": response.json()},
                    status_code=response.status_code
            )

        
    

    




    
    
