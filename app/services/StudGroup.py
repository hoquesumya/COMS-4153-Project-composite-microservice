from app.services.service_factory import ServiceFactory
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import asyncio
class StudyGroup:
    def __init__(self) -> None:
        service = ServiceFactory()
        self.compo_resource = service.get_service("CompositeResource")
    
    def get_group(self, group_id:str):
        return self.compo_resource.get_group(group_id)
    
    def get_all_group(self):
        return self.compo_resource.get_all_group()
    #synchronoulsy runnnalble data
    
    async def create_group(self,  user_id:str, group_data:dict):
        print("staring the create group ops")
        response_get, response_post = await asyncio.gather(
            self.compo_resource.get_user_sync_internal(user_id), 
            self.compo_resource.create_group(group_data)
            )
        print(response_post)
        if isinstance(response_get, JSONResponse):
            response_get_status = response_get.status_code
        else:
            response_get_status = response_get.status  # If using aiohttp, check status

        if isinstance(response_post, JSONResponse):
            response_post_status = response_post.status_code
        else:
            response_post_status = response_post.status  # If using aiohttp, check status
    
        print(f"GET Response Status: {response_get_status}")
        print(f"POST Response Status: {response_post_status}")
    
    # Now handle the conditions based on the status codes
        if response_get_status == 200 and response_post_status != 200:
            return  response_post
        elif response_get_status == 200 and response_post_status == 200:
            return {"message": "POST is successful!"}
        elif response_get_status != 200 and response_post_status == 200:
            response_post_json = await response_post.json() if hasattr(response_post, 'json') else response_post.json()
            group_id = response_post_json.get("group_id")
            response_delete = await self.compo_resource.delete_group_async(group_id)
            if isinstance(response_get, JSONResponse):
                response_delte_status = response_delete.status_code
            if response_delte_status != 200:
                raise HTTPException(status_code=400, detail="rollback failed, perform the delete one more time")
            
            raise HTTPException(status_code=400, detail="GET request failed, rollback succedded")
        elif response_get_status != 200 and response_post_status != 200:
            print("Both GET and POST requests failed.")
        raise HTTPException(status_code=400, detail="POST request failed, try again")


       # self.compo_resource.get_user(user_id)
       #self.compo_resource.create_group(group_data)

    def delete_group(self, user_id:str, group_id: int):
        #synchronous --> Structural coding pattern
        response = self.compo_resource.get_user(user_id)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="can't delete, user does not exist")
        response = self.compo_resource.delete_group(group_id)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="can't delete")
        else:
            return response
    
    def update_group(self,user_id:str, group_id:int, update_data:dict):
        response = self.compo_resource.get_user(user_id)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="can't update, user does not exis")
        print("update data1", update_data)
        response_up = self.compo_resource.update_group(group_id, update_data)
        print(response_up)
        if response_up.status_code != 200:
            error_details = response_up.body.decode("utf-8")
           # error_details = {"error": response_up.json()}
            raise HTTPException(status_code=response_up.status_code, detail=error_details)
        else:
            return response_up
        
        
