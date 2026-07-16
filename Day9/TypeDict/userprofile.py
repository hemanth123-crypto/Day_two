from typing import List, Optional, TypedDict

class userprofile(TypedDict):
    name: str
    email: str
    age: int
    bio:Optional[str]

def format_user_profile(users:List[userprofile]) -> List[str]:
    return[f"{u["name"]} ({u["age"]}) - {u["email"]}" for u in users]

print(format_user_profile([{"name": "xyz", "email": "xyz@gmail.com", "age": 25}]))

users=[{
    "id": 1,
    "name": "John Doe",
    "email": "alice@example.com"
    "bio":None
},
   {
       
    "id": 2,
    "name": "Jane Smith",
    "email": "bob@example.com",
    "bio": "A software engineer."
    
   }
}]