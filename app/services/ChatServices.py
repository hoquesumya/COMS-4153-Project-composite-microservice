from app.services.service_factory import ServiceFactory

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from .pub_sub import Publisher, Subscriber
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
    
    def post_chat(self, user_id: str, conversation: dict, google_user:dict, jwt_payload:dict):

        print("started post service chat")
        pub = Publisher()
        user_sub = Subscriber("user_sub")
        chat_sub = Subscriber("chat_sub")
        compo_sub =  Subscriber("chat_response")
        
        pub.subscribe(user_sub, "get_user")
        pub.subscribe(chat_sub, "get_chat")
        pub.subscribe(compo_sub, "chat_response")

        pub.publish("Get User", "get_user", [user_id, google_user, jwt_payload])
        user_stat, response_data_get, status_code = user_sub.receive()

        #response_data_get, status_code = self.compo_resource.get_user(user_id,google_user)
        if not user_stat:
            raise HTTPException(status_code=status_code, detail=response_data_get)
       
        #if  status_code != 200:
            #raise HTTPException(status_code=status_code, detail=response_data_get)
       
        #this one works perfectly
        print("successful user")
        pub.publish("Get chat", "get_chat", [conversation])
        chat_stat, response_post, status_code = chat_sub.receive()
        if status_code != 200:
             raise HTTPException(status_code=status_code, detail=response_post)
        else:
            return JSONResponse(content={"detail": response_post}, status_code=200)

        '''
       
        response_post, status_code = self.compo_resource.post_chat(conversation)
        if status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_post)
        else:
            print("chat created successfully")
            return JSONResponse(content={"detail": response_post}, status_code=200)
        '''

       
    def delete_chat(self, user_id: str, chat_id:int, google_user:dict, jwt_payload:dict):
        
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user,jwt_payload)
       
        if  status_code != 200:
            raise HTTPException(status_code=status_code, detail=response_data_get)
        
        print("deleteing the chat")
        response_delete_data, status_code = self.compo_resource.delete_chat(chat_id)
        print(response_delete_data)
        if status_code != 201 or status_code!=200:
            raise HTTPException(status_code=status_code, detail=response_delete_data)
        else:
            return JSONResponse(content={"detail": response_delete_data}, status_code=200)
    
    def update_chat(self, user_id:str, chat_id:int, conversation:dict, google_user:dict, jwt_payload:dict):
        response_data_get, status_code = self.compo_resource.get_user(user_id,google_user, jwt_payload)
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