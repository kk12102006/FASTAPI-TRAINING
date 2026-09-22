from fastapi import FastAPI, HTTPException #If the color is dim it means it is not used in program
from pydantic import BaseModel

app = FastAPI()

@app.get("/") #"get" is verb and "/"" is noun
def home():
    return {"message":"Enterprise IT SErvide Desk"}


db={
    1:{"id":1,
       "title":"computer is not on",
       "description":"power button not working",
       "category":"hardware",
       "status":"NEW"},
    2:{"id":2,
       "title":"internet is not working",
       "description":"wifi problem",
       "category":"hardware",
       "status":"NEW"}
}

#schemas
class TicketCreate(BaseModel):
    title:str
    description:str
    category:str
    status:str

class TicketResponse(TicketCreate):
    id :int    

#APIs
@app.get("/tickets")
def ticket_read_all():
    return list(db.values())

@app.get("/tickets/{id}")
def ticket_read_by_id(id:int):
    if id not in db:
        raise HTTPException(detail="Ticket Not Found",status_code=404)
    return db[id]

@app.post("/tickets",status_code=201,response_model=TicketResponse)
def ticket_create(ticket_payload:TicketCreate):
    new_id=max(db.keys(),default=0)+1
    db[new_id]={"id":new_id,**ticket_payload.model_dump()}
    return db[new_id]

@app.put("/tickets/{id}",response_model=TicketResponse)
def ticket_update(id:int,payload:TicketCreate):
    if id not in db:
        raise HTTPException(detail="Ticket Not Found",status_code=404)
    db[id]={"id":id,**payload.model_dump()}
    return db[id]

@app.delete("/tickets/{id}")
def ticket_delete(id:int):
    if id not in db:
        raise HTTPException(detail="Ticket not found",status_code=404)
    del db[id]
    return{"Message":"Ticket Deleted Successfully"}

#LEVEL 1 COMPLETED