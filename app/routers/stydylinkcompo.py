from fastapi import APIRouter, HTTPException, Form, Body
from app.services.ChatServices import Chat
from app.services.StudGroup import StudyGroup
from app.services.UserServices import UserService
from app.services.CourseEnrollment import CourseEnrolment

router = APIRouter()
group = StudyGroup()
chat =  Chat()
user = UserService()

# User Profile Service
@router.get("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def get_user_profile(user_id: str):
    """
    Retrieve the profile of a user by user ID.
    """
    try:
        res = user.get_user(user_id)
        if not res:
            raise HTTPException(status_code=404, detail="have not find the users")
    except HTTPException as err:
        raise err


#need to fix 
@router.post("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def post_user_profile(user_id: str, token: str):
    """
    Create  the profile of a user by user ID.
    """
    user.post_user(user_id, token)

@router.delete("/StudyLink/v1/users/{user_id}/profile", tags=["users"])
def delete_user_profile(user_id: str):
    """
    Delete the profile of a user by user ID.
    """
    user.delete_user(user_id)

@router.get("/StudyLink/v1/users/", tags=["users"])
def get_all_users(params:dict):

    user.get_all_users(params=params)
# .................Chat Service..................
@router.post("/StudyLink/v1/{user_id}/conversations", tags=["conversations"])
def create_conversation(user_id: str, conversation: dict):
    """
    Create a new conversation for a user by user ID
    """
    chat.post_chat(user_id, conversation)

@router.put("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def update_conversation(user_id: str, conversation_id: int, conversation: dict):
    """
    Update a conversation by conversation ID for a user by user ID.
    """
    chat.update_chat(user_id, conversation_id, conversation)

@router.get("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def get_conversation(user_id: str, conversation_id: int):
    """
    Retrieve a conversation by conversation ID for a user by user ID.
    """
    chat.get_chat(user_id, conversation_id)

@router.delete("/StudyLink/v1/{user_id}/conversations/{conversation_id}", tags=["conversations"])
def delete_convo(user_id: str, conversation_id: int):
    chat.delete_chat(user_id, conversation_id)

@router.get("/StudyLink/v1/{user_id}/conversations")
def get_all_chat(user_id: str):
    chat.get_all_chat(user_id)
#......................StudyGroup.....................
@router.get("/StudyLink/v1/{user_id}/studyGroup/{group_id}", tags = ["studyGroup"])
def get_studyGroup(user_id: str, group_id:str):
    group.get_group(user_id, group_id=group_id)

@router.get("/StudyLink/v1/{user_id}/studyGroup/", tags = ["studyGroup"])
def get_all_group(user_id: str):
    group.get_all_group(user_id)

@router.post("/StudyLink/v1/{user_id}/studyGroup/", tags = ["studyGroup"])
def post_studyGroup(user_id: str, group_data:dict):
    group.create_group(user_id,group_data)

@router.delete("/StudyLink/v1/{user_id}/studyGroup/{group_id}", tags = ["studyGroup"])
def get_studyGroup(user_id: str, group_id: int):
    group.delete_group(user_id)

@router.put("/StudyLink/v1/{user_id}/studyGroup/{group_id}", tags = ["studyGroup"])
def update_study_group( user_id: str, group_id: int):
    group.update_group(user_id, group_id)


