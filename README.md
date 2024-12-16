# COMS-4153-Project-composite-microservice
## User Service
- Get /StudyLink/v1/users/{user_id}/login  → call the user microservice logging endpoint
- Get  /StudyLink/v1/users/{user_id}/profile → get request, has jwt and google token as a header, pass along to the user service to verify
- Post /StudyLink/v1/users/{user_id}/profile → post request, has query parameters canvas token
- Delete /StudyLink/v1/users/{user_id}/profile → delete request, has  jwt and google token as a header, pass along to the user service to verify
- Get /StudyLink/v1/users/ → retriever all users along with jwt and google token as the header

## Study Service
- Get /StudyLink/v1/study-group/{group_id}  → get request to the study-group microservice
- Get /StudyLink/v1/study-group/" → get a request to the study-group microservice (retrieve all group)
- Post /StudyLink/v1/{user_id}/study-group/ → asynchronous post request to user service + study-group + - perform rollback operation if the post is successful but the get is not successful
- Delete /StudyLink/v1/{user_id}/study-group/{group_id} → synchronous call to user service + study-group to delete a group
- Put /StudyLink/v1/{user_id}/study-group/{group_id}" → synchronous call to user service + study-group to update a group

## Course Enrollment
Two get requests to retrieve a student's courses and find students of the course

## Chat Service
- Post /StudyLink/v1/{user_id}/conversations → post a chat; has choreography pattern to call the user service and the chat service 
- Delete "/StudyLink/v1/{user_id}/conversations/{conversation_id}", → Has google workflow to call the user and chat services
- Put /StudyLink/v1/conversations/{conversation_id} → Synchronous call between the user and chat service
- Get StudyLink/v1/{user_id}/conversations/{conversation_id} → Retrieves conversation
- Get /StudyLink/v1/conversations → Get all the conversations





