from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first: int
    second: int


class ChatList(BaseModel):
    chats: list[Chat]
