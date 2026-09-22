from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017/")
db=client["college"]
stu=db["students"]
for i in stu.find():
    print(i["name"],i["age"])
tea=db["teachers"]
tea.insert_one(
    {"name":"Bhavya", "age":29,"Dept":"Math"}
)  
tea.insert_one({"name":"Bhavya", "age":29,"Dept":"Math"})
tea.delete_many({"name":"Bhavya"})
 