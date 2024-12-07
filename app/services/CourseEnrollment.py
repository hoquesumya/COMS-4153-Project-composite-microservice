from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
class CourseEnrolment:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResourceService")
 
    def get_all_students(self, course_id:str, token:str):
        try:
            return self.compo_resource.get_all_students_per_course(course_id, token)
        except  Exception as e:
            raise HTTPException(status_code=404, detail=f"Error fetching coureses: {str(e)}")


        
    def get_all_course(self, user_id: str, token:str):
        try:
            return self.compo_resource.get_course(user_id, token)
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Error fetching coureses: {str(e)}")
    