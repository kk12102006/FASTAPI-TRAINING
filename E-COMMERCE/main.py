from fastapi import FastAPI , HTTPException
from pydantic import BaseModel

app=FastAPI()

db={
    1:{
        "id":1,
        "title":"Placing order",
        "description":"Unable to place the order",
        "category":"order",
        "status":"new"
    },
    2:{
            "id":2,
            "title":"Order status not updated ",
            "description":"Order status not updated even after the order is placed",
            "category":"order",
            "status":"new"
        },
    3:{
            "id":3,
            "title":"Wrong item received",
            "description":"Received order is different from the ordered order",
            "category":"order",
            "status":"new"
        },
    4:{
            "id":4,
            "title":"Cancel order",
            "description":"Unable to cancel the order",
            "category":"order",
            "status":"new"
        },
    5:{
            "id":5,
            "title":"Order not delivered",
            "description":"Order not delivered even after the specified delivery date",
            "category":"delivery",
            "status":"new"
        },
    6:{
            "id":6,
            "title":"Dameged Item",
            "description":"Order delivered is damaged",
            "category":"delivery",
            "status":"new"
        },
    7:{
            "id":7,
            "title":"Delivery address",
            "description":"Change the delivery adddress",
            "category":"delivery",
            "status":"new"
        },
    8:{
            "id":8,
            "title":"Order deliverd but not received",
            "description":"Order not received but the order status is delivered",
            "category":"delivery",
            "status":"new"
        }
    
}

#schemas
class TicketCreate(BaseModel):
    title:str
    description:str
    category:str
    status:str
class TicketResponse(TicketCreate):
    id:int


#API's
@app.get("/")
def home():
    return {"message":"Welcome to E-Commerce Customer Service Help Desk"}

@app.get("/complaints")
def read_all_complaint():
    return list(db.values())

@app.get("/complaints/{id}")
def read_complaint_id(id:int):
    if id not in db:
        raise HTTPException(detail="Complaint not found",status_code=404)
    return db[id]

@app.post("/complaints",status_code=201,response_model=TicketResponse)
def create_complaint(payload:TicketCreate):
    new_id=max(db.keys(),default=0)+1
    db[new_id]={"id":new_id,**payload.model_dump()}
    return db[new_id]

@app.put("/complaints/{id}",response_model=TicketResponse)
def update_complaint(id:int,payload:TicketCreate):
    if id not in db:
        raise HTTPException(detail="No such complaint exist",status_code=404)
    db[id]={"id":id,**payload.model_dump()}
    return db[id]

@app.delete("/complaints/{id}")
def delete_complaint(id:int):
    if id not in db:
        raise HTTPException(detail="No such complaint exist",status_code=404)       
    del db[id]
    return {"message":"Complaint deleted successfully"}