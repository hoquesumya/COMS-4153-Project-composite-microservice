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
    def get_user(self, user_id:str, google:dict):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            print("calling get user",google)
            response = requests.get(url, json = google, timeout=10)
            response.raise_for_status()
            
            print(self.user_config, user_id)
            return (response.json(), response.status_code)
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
            # Try to parse the response as JSON
                response_data = response.json()  # This is from the external service
                print(f"External service response (JSON): {response_data}")
            except ValueError:
            # If it's not JSON, log the raw text response
             response_data = response.text
            print(f"HTTP errors occurred: {http_err}", response.status_code, response_data)

            return (response_data, response.status_code)
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

    
    def post_user(self, user_id: str, token:str):
        url = f"{self.user_config}/users/{user_id}/profile?token={token}"
        try:
            response = requests.post(url,timeout=5)
            response.raise_for_status()
            status_code = response.status_code
            #print(status_code, response.json())
            return (response.json(), response.status_code)
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            try:
            # Try to parse the response as JSON
                response_data = response.json()  # This is from the external service
                print(f"External service response (JSON): {response_data}")
            except ValueError:
            # If it's not JSON, log the raw text response
             response_data = response.text
            print(f"HTTP errors occurred: {http_err}", response.status_code, response_data)
            return (response_data,response.status_code)
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
      
        print(self, user_id, self.user_config)

    def get_all_users(self, params:dict):
        url = f"{self.user_config}/users/"
        try:
            response = requests.get(url, json=params, timeout=5)
            response.raise_for_status()
            return (response.json(), response.status_code)
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            return (response.json(), response.status_code)
            return JSONResponse(
                content={"error": response.json()},
                status_code=response.status_code
            )
            print(f"HTTP error occurred: {http_err}")
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

   
    def delete_user(self, user_id: str, google_user:dict):
        url = f"{self.user_config}/users/{user_id}/profile"
        try:
            print("start deleting")
            response = requests.delete(url, json=google_user, timeout=5)
            response.raise_for_status()
            return (response.json(), response.status_code)
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return (response.json(), response.status_code)
    
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
        
        print(self, user_id, self.user_config)
    
    
    async def get_user_sync_internal(self, user_id:str, google_user:dict):
        url = f"{self.user_config}/users/{user_id}/profile"

        async with aiohttp.ClientSession() as session:
            try:
                response = await session.get(url, json=google_user)
                response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
                response_data = await response.json()
                return response_data, response.status
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                print(f"Client error occurred: {client_err}")
                return (response.json(), response.status)
              
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
            return response.json(), response.status_code
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return (response.json(), response.status_code)
            return JSONResponse(
                    content={"error": response.json()},
                    status_code=response.status_code
                )
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return JSONResponse(
                    content={"error": response.json()},
                    status_code=response.status_code
                )
        except Exception as err:
             print(f"An unexpected error occurred: {err}")

       
    async def create_group(self, group_data: dict):
        url = f"{self.study_config}/study-group/"
        async with aiohttp.ClientSession() as client:
            try:
                response = await client.post(url, json=group_data, timeout=5)
                response.raise_for_status()
                  # This will raise an error for 4xx/5xx status codes
                response_data = await response.json()
                return (response_data, response.status)
            
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                try:
                    error_data = await client_err.response.json()
                except Exception:
                    error_data = {"error": f"Client error occurred: {client_err.status}"}
                return (error_data, client_err.status)
                
            except Exception as err:
                print(f"An unexpected error occurred: {err}")
                return (response_data, response.status)
    
    
    async def delete_group_async(self, group_id:int):
        url = f"{self.study_config}/study-group/{group_id}"
        async with aiohttp.ClientSession() as client:
            try:
                response = await client.delete(url, timeout=15)
                response.raise_for_status()  # This will raise an error for 4xx/5xx status codes
                response_data = await response.json()
                return (response_data, response.status)
            
            except TimeoutError:
                return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
            except aiohttp.ClientError as client_err:
                print(f"Client error occurred: {client_err}")
                try:
                    error_data = await client_err.response.json()
                except Exception:
                    error_data = {"error": f"Client error occurred: {client_err.status}"}
                return (error_data,  client_err.status)
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
            return (response.json(), response.status_code)
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            return (response.json(), response.status_code)
            return JSONResponse(
                content={"error": response.json()},
                status_code=response.status_code
            )
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
            return (response.json(), response.status_code)
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        
        except HTTPError as http_err:
            
            print(f"HTTP error occurred: {http_err}")
            return (response.json(), response.status_code)
            return JSONResponse(
                content={"error": response.json()},
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
            return (response.json(), response.status_code)
        
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            return (response.json(), response.status_code)
            return JSONResponse(
                content={"error": response.json()},
                status_code=response.status_code
            )
        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
    
    #.....staring thr course enrollment service....
    def get_course(self, student_id:str, token :str):
        url = f"{self.course_config}/users/{student_id}/courses"
        try:
            print("staring getting courses", token)
            headers = {
                "token": token
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=response.status_code
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return JSONResponse(
                content={"error": response.json()},
                status_code=response.status_code
            )

        except RequestException as req_err:
             print(f"Request error occurred: {req_err}")
        except Exception as err:
             print(f"An unexpected error occurred: {err}")
       
        print(self.course_config, student_id)
    
    def get_all_students_per_course(self, course_code: str, token: str):
        url = f"{self.course_config}/course/{course_code}/students"
        try:
            headers = {
                "token":token
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
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
            return response.json()
       
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

    
    def get_all_chat(self):
        print(self.chat_config)
        url = f"{self.chat_config}/conversations/"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
       
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
            return (response.json(), response.status_code)
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            return JSONResponse(
                content={"error": "The request timed out"},
                status_code=408
            )
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            return (response.json(), response.status_code)


    def delete_chat(self,chat_id:int):
        url = f"{self.chat_config}/conversations/{chat_id}"
        try:
            response = requests.delete(url, timeout=5)
            response.raise_for_status()
            return (response.json(), response.status_code)
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
            error_details = {"error": "Unknown error"}
            
            return error_details, 408
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
                # Try to extract error details from the response if available
                error_content = response.json()
                return (error_content, response.status_code)
            except Exception:
                # Fallback if response content is not JSON
                error_content = {"message": "Unknown error"}
            return {
                "error": error_content,
                "status_code": response.status_code,
            }

        print(self.chat_config, chat_id)

    
    def update_chat(self, chat_id, conversation: dict):
        url = f"{self.chat_config}/conversations/{chat_id}"
        try:
           # print("conversation is:", conversation)
            response = requests.put(url, json=conversation, timeout=5)
            response.raise_for_status()
            print(response.json(),response)
            return (response.json(), response.status_code)
       
        except requests.exceptions.Timeout:
            print("The request timed out!")
          
            error_details = {"error": "Unknown error"}
            
            return error_details, 408

          
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
                error_details = response.json()
            except ValueError:
                error_details = {"error": "Unknown error"}
            
            return error_details, response.status_code

        
    

    




    
    
