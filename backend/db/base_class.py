from typing import Any
from sqlalchemy import Column
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    id : Any
    
    