from app.services.service_factory import ServiceFactory
class UserService:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_user(self, user_id:str):
        status, response = self.compo_resource.get_user(user_id)
        if status != 200:
            return None
        else:
            return response
    def get_all_users(self, params:dict):
        self.compo_resource.get_all_users(params)

    def post_user(self, user_id: str, token:str):
        self.compo_resource.get_course(user_id)
        self.compo_resource.post_user(user_id, str)

    def delete_user(self, user_id: str):
        self.compo_resource.delete_user(user_id)