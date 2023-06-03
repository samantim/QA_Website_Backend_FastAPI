from typing import Any
from sqlalchemy import Column
from sqlalchemy.ext.declarative import as_declarative

#super class of all models
@as_declarative()
class Base:
    id : Any