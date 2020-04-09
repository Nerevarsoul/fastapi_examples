import dataclasses
from datetime import datetime
from pprint import pprint
from typing import List

from pydantic import ValidationError
from pydantic.dataclasses import dataclass


@dataclass
class User:
    id: int
    name: str = 'John Doe'
    signup_ts: datetime = None
    friends: List[int] = dataclasses.field(default_factory=lambda: [0])


if __name__ == '__main__':
    external_data = {
        'id': '123',
        'signup_ts': '2019-06-01 12:22',
        'friends': [1, 2, '3']
    }

    user = User(**external_data)
    print(user.id)
    print(repr(user.signup_ts))
    print(user.friends)
    print()
    pprint(dataclasses.asdict(user))
    print()
    pprint(user.__pydantic_model__.schema())

    try:
        User(signup_ts='broken', friends=[1, 2, 'not number'])
    except ValidationError as e:
        print(e.json())
    except Exception as e:
        print(type(e))
