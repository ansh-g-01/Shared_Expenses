from enum import Enum
from pydantic import BaseModel
    

class SplitType(str, Enum):
    equal = "equal"
    unequal = "unequal"
    percentage = "percentage"
