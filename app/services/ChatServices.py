from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
class Chat:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_chat(self, chat_id:int):
        #self.compo_resource.get_user(user_id)
        return self.compo_resource.get_chat(chat_id)
    
    def post_chat(self, user_id: str, conversation: dict, google_user:dict):
        print("started post service chat")
        response = self.compo_resource.get_user(user_id,google_user)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        response = self.compo_resource.post_chat(conversation)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        else:
            return response

       
    def delete_chat(self, user_id: str, chat_id:int, google_user:dict):
        response = self.compo_resource.get_user(user_id,google_user)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        response_delete = self.compo_resource.delete_chat(chat_id)
        if response_delete.status_code != 200:
            raise HTTPException(status_code=response_delete.status_code, detail=response_delete.json())
        else:
            return response_delete
    
    def update_chat(self, user_id:str, chat_id:int, conversation:dict, google_user:dict):
        response = self.compo_resource.get_user(user_id,google_user)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        response_post = self.compo_resource.update_chat(chat_id, conversation)
        if response_post.status_code != 200:
            raise HTTPException(status_code=response_post.status_code, detail=response_post.json())
        else:
            return response_post
    def get_all_chat(self):
       return self.compo_resource.get_all_chat()