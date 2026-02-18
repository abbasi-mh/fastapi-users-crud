from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
