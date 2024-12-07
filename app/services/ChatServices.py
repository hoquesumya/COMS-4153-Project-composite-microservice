from app.services.service_factory import ServiceFactory
class Chat:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_chat(self, user_id:str, chat_id:int):
        #self.compo_resource.get_user(user_id)
        return self.compo_resource.get_chat(chat_id)
    
    def post_chat(self, user_id: str, conversation: dict):
        print("started post service chat")
        #self.compo_resource.get_user(user_id)
        return self.compo_resource.post_chat(conversation)
       
    def delete_chat(self, user_id: str, chat_id:int):
        #self.compo_resource.get_user(user_id)
        return self.compo_resource.delete_chat(chat_id)
    
    def update_chat(self, user_id:str, chat_id:int, conversation:dict):
        #self.compo_resource.get_user(user_id)
       return  self.compo_resource.update_chat(chat_id, conversation)
    def get_all_chat(self, user_id:str):
        #self.compo_resource.get_user(user_id)
       return self.compo_resource.get_all_chat()