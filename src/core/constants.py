from typing import Annotated

from annotated_types import MaxLen
from pydantic import EmailStr


str_len = 50
long_str_len = 255
country_len = 2

default_str = Annotated[str, MaxLen(str_len)]
long_str = Annotated[str, MaxLen(long_str_len)]
email_str = Annotated[EmailStr, MaxLen(long_str_len)]
country_code_str = Annotated[str, MaxLen(country_len)]
