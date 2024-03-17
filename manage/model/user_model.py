from typing import Optional, Dict

from basic.model.basic_model import BasicModel


class UserModel(BasicModel):
    name: str
    password_hash: str
    profile: Optional[Dict] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
