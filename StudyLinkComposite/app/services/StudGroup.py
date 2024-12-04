from app.services.service_factory import ServiceFactory
class StudyGroup:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_group(self, user_id:str,  group_id:str):
        self.compo_resource.get_user(user_id)
        self.compo_resource.get_group(group_id)
    
    def get_all_group(self, user_id:str):
        self.compo_resource.get_user(user_id)
        self.compo_resource.get_all_group()
   
    def create_group(self,  user_id:str, group_data:dict):
        print("staring the create group ops")
        self.compo_resource.get_user(user_id)
        self.compo_resource.create_group(group_data)

    def delete_group(self, user_id:str, group_id: str):
        self.compo_resource.get_user(user_id)
        self.compo_resource.delete_group(group_id)
    
    def update_group(self,user_id:str, group_id:str):
        self.compo_resource.get_user(user_id)
        self.compo_resource.update_group(group_id)
