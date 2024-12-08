from fastapi import APIRouter, HTTPException, Form, Body, Header
from app.services.ChatServices import Chat
from app.services.StudGroup import StudyGroup
from app.services.UserServices import UserService
from app.services.CourseEnrollment import CourseEnrolment
import asyncio

router = APIRouter()
group = StudyGroup()
chat =  Chat()
user = UserService()
course = CourseEnrolment()

# User Profile Service
@router.get("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def get_user_profile(user_id: str, google_user:dict):
    """
    Retrieve the profile of a user by user ID.
    """
    print("calling the fuction")
    return user.get_user(user_id, google_user)
   

#need to fix 
@router.post("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def post_user_profile(user_id: str, token: str):
    """
    Create  the profile of a user by user ID.
    """
    return user.post_user(user_id, token)

@router.delete("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def delete_user_profile(user_id: str, google_user:dict):

   return  user.delete_user(user_id, google_user)

@router.get("/StudyLink/v1/users/", tags=["users"])
def get_all_users(params:dict):

    return user.get_all_users(params=params)

#.................. Course Enrollment Service............
@router.get("/StudyLink/v1/course/{course_id}/students")
def get_all_students(course_id:str, token: str = Header(...)):
    print("staried finding all courses")
    return course.get_all_students(course_id, token)

@router.get("/StudyLink/v1/users/{student_id}/courses")
def get_allcourse(student_id: str, token: str = Header(...)):
    print("started the request for students course")
    return course.get_all_course(student_id, token)
# .................Chat Service..................

@router.post("/StudyLink/v1/{user_id}/conversations", tags=["conversations"])
def create_conversation(user_id: str, conversation: dict, google_user:dict):
    print("started chat")
    return chat.post_chat(user_id, conversation, google_user)

@router.put("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def update_conversation(user_id: str, conversation_id: int, conversation: dict, google_user:dict):
    """
    Update a conversation by conversation ID for a user by user ID.
    """
    return chat.update_chat(user_id, conversation_id, conversation, google_user)

@router.get("/StudyLink/v1/conversations/{conversation_id}", tags=["conversations"])
def get_conversation(conversation_id: int):

   return chat.get_chat(conversation_id)

@router.delete("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def delete_convo(user_id: str, conversation_id: int, google_user:dict):
    return chat.delete_chat(user_id, conversation_id, google_user)

@router.get("/StudyLink/v1/conversations")
def get_all_chat():
    return chat.get_all_chat()
#......................StudyGroup.....................
@router.get("/StudyLink/v1/studyGroup/{group_id}", tags = ["studyGroup"])
def get_studyGroup( group_id:str):
    return group.get_group( group_id=group_id)

@router.get("/StudyLink/v1/studyGroup/", tags = ["studyGroup"])
def get_all_group():
    return group.get_all_group()

@router.post("/StudyLink/v1/{user_id}/studyGroup/", tags = ["studyGroup"])
async def post_studyGroup(user_id: str, group_data:dict, google_user:dict):
    print("statting the creating the group")
    res = await group.create_group(user_id,group_data, google_user)
    return res

@router.delete("/StudyLink/v1/{user_id}/studyGroup/{group_id}", tags = ["studyGroup"])
def get_studyGroup(user_id: str, group_id: int,google_user:dict ):
    return group.delete_group(user_id, group_id,google_user)

@router.put("/StudyLink/v1/{user_id}/studyGroup/{group_id}", tags = ["studyGroup"])
def update_study_group( user_id: str, group_id: int, update_data:dict, google_user:dict):
    print("update data", update_data)
    return group.update_group(user_id, group_id, update_data, google_user)

