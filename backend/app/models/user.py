import uuid
from pydantic import field_validator, EmailStr
from sqlmodel import Field, SQLModel


class UserIdentityBase(SQLModel):
    name: str = Field(min_length=1, max_length=50)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be blank")
        return cleaned


class UserRegister(UserIdentityBase):
    password: str = Field(min_length=1)


class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=1)


class UserDBBase(UserIdentityBase):
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    refresh_access_token: str | None = Field(default=None, min_length=1)
    is_admin : bool = Field(default=False)


class UserUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=1)

    @field_validator("name")
    @classmethod
    def strip_and_validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("value cannot be blank")
        return cleaned


class UserRead(SQLModel):
    id: uuid.UUID
    name: str
    email: EmailStr
