from typing import Optional, List

from pydantic import BaseModel, Field, field_validator


class CreateUserRequest(BaseModel):
    """Request model for creating a user"""
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

    @field_validator('username')
    def validate_username(cls, v):
        if not v or v.isspace():
            raise ValueError('Username cannot be empty or whitespace only')
        return v


class UpdateUserRequest(BaseModel):
    """Request model for updating user email"""
    email: str


class UserData(BaseModel):
    """User data model in response"""
    id: int
    username: str
    email: str = None


class CreateUserResponse(BaseModel):
    """Response model for create user"""
    code: int
    data: Optional[UserData] = None
    msg: str


class GetUserResponse(BaseModel):
    """Response model for get user details"""
    code: int
    data: Optional[UserData] = None
    msg: str


class UpdateUserResponse(BaseModel):
    """Response model for update user"""
    code: int
    data: Optional[dict] = None
    msg: str


class DeleteUserResponse(BaseModel):
    """Response model for delete user"""
    code: int
    data: Optional[dict] = None
    msg: str


class UserListItem(BaseModel):
    """User item in batch query response"""
    id: int
    username: str


class BatchQueryData(BaseModel):
    """Data model for batch query response"""
    total: int
    list: List[UserListItem]


class BatchQueryResponse(BaseModel):
    """Response model for batch query users"""
    code: int
    data: Optional[BatchQueryData] = None
    msg: str