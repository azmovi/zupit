from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    first: str
    second: str


class ChatList(BaseModel):
    chats: list[Chat]


class Message(BaseModel):
    sender: str
    message: str


class MessageList(BaseModel):
    messages: list[Message]
