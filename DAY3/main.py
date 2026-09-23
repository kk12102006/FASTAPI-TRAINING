# CODE FOR ONLY CRUD OPERATIONS
from fastapi import FastAPI , HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from  bson import ObjectId

#app
app=FastAPI()

#db config
URL="mongodb://127.0.0.1:27017"
client=MongoClient(URL)
db=client["service_ticket_db"]
ticket_collection=db["tickets"]

#schema from pydantic
class TicketCreate(BaseModel):
    title:str
    description:str
    category:str
    status:str
class TicketResponse(TicketCreate):
    id:str
    
#helper
def ticket_helper(ticket_doc):
    return {
        "id":str(ticket_doc["_id"]),
        "title":ticket_doc["title"],
        "description":ticket_doc["description"],
        "category":ticket_doc["category"],
        "status":ticket_doc["status"]
    }   
    
#API's
@app.get("/")
def home():
    return {"message":"Welocome to Service Desk"}

@app.post("/tickets",status_code=201,response_model=TicketResponse)
def create_ticket(payload:TicketCreate):#payload is an object of TicketCreate class
    ticket_dict=payload.model_dump()    #model_dump() converts pydantic model to dict
    result=ticket_collection.insert_one(ticket_dict)   #insert_one will return an object of InsertOneResult class which has inserted_id attribute
    new_ticket=ticket_collection.find_one({"_id":result.inserted_id}) #.inserted_id will return the id of the newly inserted document
    return ticket_helper(new_ticket)

@app.get("/tickets",response_model=list[TicketResponse]) #list[TicketResponse] means the response will be a list of TicketResponse's
def ticket_read_all():
    docs=ticket_collection.find()
    tickets=[ticket_helper(doc) for doc in docs]
    return tickets

@app.get("/tickets/{id}",response_model=TicketResponse)
def ticket_read_by_id(id:str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    doc=ticket_collection.find_one({"_id":ObjectId(id)})
    if not doc:
        raise HTTPException(detail="Ticket not found",status_code=404)
    return ticket_helper(doc)   

@app.put("/tickets/{id}",response_model=TicketResponse)
def ticket_update(id:str,payload:TicketCreate):
    if not ObjectId.is_valid(id):
            raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    ticket_dict=payload.model_dump()
    result=ticket_collection.update_one({"_id":ObjectId(id)},
                                        {"$set":ticket_dict})    
    if result.matched_count==0: #It returns the number of documents matched by the filter. 
        raise HTTPException(detail="Ticket not found",status_code=404)
    new_ticket=ticket_collection.find_one({"_id":ObjectId(id)})
    return ticket_helper(new_ticket)

@app.delete("/tickets/{id}")
def ticket_delete(id:str):
    if not ObjectId.is_valid(id):
        raise HTTPException(detail="Invalid Ticket ID",status_code=403)
    result=ticket_collection.delete_one({"_id":ObjectId(id)})
    if result.deleted_count==0:
        raise HTTPException(detail="Ticket not found",status_code=404)
    return {"message":"Ticket deleted successfully"}