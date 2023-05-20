from fastapi import HTTPException


class ResourceNotFoundException(HTTPException):
    def __init__(self, message: str = None, **kwargs):
        super().__init__(status_code=404, detail=message, **kwargs)