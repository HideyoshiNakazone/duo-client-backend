from fastapi import HTTPException


class InvalidUserAuthenticationException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=401, detail=message)
