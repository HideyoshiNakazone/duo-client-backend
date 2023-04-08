from fastapi import HTTPException


class UserNotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=404, detail=message)
