from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
  full_name: str
  email: EmailStr
  password: str


class GetUserData(BaseModel):
  user_id: str
