from dataclasses import dataclass
from typing import Optional

from dataclasses_json import LetterCase, dataclass_json


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class URLRequest:
    url: str
    title: Optional[str]
