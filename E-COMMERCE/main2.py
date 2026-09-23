from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId


app=FastAPI()

#Mongo
URL="mongodb://127.0.0.1:27017"
client=MongoClient(URL)
db=client["e-com_db"]
complaint_collection=db["complaints"]   

#schema
class TicketCreate(BaseModel):
    title:str
    description:str
    category:str
    status:str
class TicketResponse(TicketCreate):
    id:str

#helper
def complaint_helper(complaint_doc):
    return {
        "id":str(complaint_doc["_id"]),
        "title":complaint_doc["title"],
        "description":complaint_doc["description"],
        "category":complaint_doc["category"],
        "status":complaint_doc["status"]
    }
    
@app.get("/complaints",response_model=list[TicketResponse])
def complaint_read_all():
    docs=complaint_collection.find()
    complaints=[complaint_helper(doc) for doc in docs]
    return complaints

@app.get("/complaints/{id}",response_model=TicketResponse)
def complaint_read_by_id(id:str,payload:TicketCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Complaint ID",status_code=403)
    doc=complaint_collection.find_one({"_id":ObjectId(id)})
    if not doc:
        raise HTTPException(detail="Complaint not found",status_code=404)
    return complaint_helper(doc)

@app.post("/complaints",status_code=201,response_model=TicketResponse)
def create_complaint(payload:TicketCreate):
    complaint_dict=payload.model_dump()
    result=complaint_collection.insert_one(complaint_dict)
    new_complaint=complaint_collection.find_one({"_id":result.inserted_id})
    return complaint_helper(new_complaint)

@app.put("/complaints/{id}",response_model=TicketResponse)
def update_complaint(id:str,payload:TicketCreate):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Complaint ID",status_code=403)
    complaint_dict=payload.model_dump()
    result=complaint_collection.update_one({"_id":ObjectId(id)},
                                      {"$set":complaint_dict})
    if result.matched_count==0:
        raise HTTPException(detail="Complaint Not Found",status_code=404)
    new_complaint=complaint_collection.find_one({"_id":ObjectId(id)})
    return complaint_helper(new_complaint)

@app.delete("/complaints/{id}")
def delete(id:str):
    if not ObjectId.is_valid(id):
            raise HTTPException(detail="Invalid Complaint ID",status_code=403)
    result=complaint_collection.delete_one({"_id":ObjectId(id)})
    if result.deleted_count==0:
        raise HTTPException(detail="Complaint Not Found",status_code=404)
    return {"message":"Complaint Deleted Successfully"}     