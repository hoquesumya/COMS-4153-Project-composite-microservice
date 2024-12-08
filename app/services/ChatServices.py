from app.services.service_factory import ServiceFactory

from fastapi import HTTPException
from fastapi.responses import JSONResponse
class Chat:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_chat(self, chat_id:int):
        data, status_code =  self.compo_resource.get_chat(chat_id)
        if status_code == 200:
            return data
        else:
            raise HTTPException(status_code=status_code, detail=data)
    
    def post_chat(self, user_id: str, conversation: dict, google_user:dict):

        print("started post service chat")
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
       
        #this one works perfectly
        response_post, status_code = self.compo_resource.post_chat(conversation)
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_post)
        else:
            print("chat created successfully")
            return JSONResponse(content={"detail": response_post}, status_code=200)

       
    def delete_chat(self, user_id: str, chat_id:int, google_user:dict):
        
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        
        print("deleteing the chat")
        response_delete_data, status_code = self.compo_resource.delete_chat(chat_id)
        print(response_delete_data)
        if status_code != 201 or status_code!=200:
            raise HTTPException(status_code=status_code, detail=response_delete_data)
        else:
            return JSONResponse(content={"detail": response_delete_data}, status_code=200)
    
    def update_chat(self, user_id:str, chat_id:int, conversation:dict, google_user:dict):
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user)
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        response_put_data, status_code = self.compo_resource.update_chat(chat_id, conversation)
        print(status_code)
        if status_code != 200 :
            raise HTTPException(status_code=status_code, detail=response_put_data)
        else:
            return JSONResponse(content={"detail": response_put_data}, status_code=200)
    
    def get_all_chat(self):
       data, status_code = self.compo_resource.get_all_chat()
       if status_code == 200:
           return data
       raise HTTPException(status_code=status_code, detail=data)