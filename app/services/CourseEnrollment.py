from app.services.service_factory import ServiceFactory
class CourseEnrolment:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResourceService")
    
    def verify_user(self, user_id:str):
        self.compo_resource.get_course(user_id)
        
    def get_all_course(self, user_id: str):
        self.compo_resource.get_course(user_id)
    