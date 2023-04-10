from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    token: str
    expiration: datetime