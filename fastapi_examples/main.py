import asyncio
import uuid

import databases
from fastapi import FastAPI
from fastapi.routing import APIRoute
from pydantic.dataclasses import dataclass

from pydantic.main import BaseModel
from sqlalchemy import MetaData, Table, Column, String
from sqlalchemy.dialects.postgresql import UUID
from starlette.background import BackgroundTasks
from starlette.responses import JSONResponse


database = databases.Database(
    'postgresql://localhost/mobile',
    user='postgres',
    password='postgres'
)

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', UUID, default=uuid.uuid4, primary_key=True),
    Column('first_name', String(50), nullable=True),
)


class Item(BaseModel):
    id: int
    text: str


@dataclass
class ItemAnswer:
    code: int
    result: Item
    message: str = None


async def write_notification(message: str):
    await asyncio.sleep(5)
    print(message)


def read_root():
    """Корневой урл"""
    return {'Hello': 'World'}


def read_item(item_id: int, q: str = None):
    """Получение сущности по идентификатору"""
    return {'item_id': item_id, 'q': q}


def add_item(item: Item):
    """Добавление сущности"""
    return {
        'code': 201,
        'result': item
    }


async def user_list():
    query = users.select()
    results = await database.fetch_all(query)
    content = [
        {
            'id': str(result['id']),
            'first_name': result['first_name']
        }
        for result in results
    ]
    return {'res': content}


async def send_notification(message: str, background_tasks: BackgroundTasks):
    """"""
    background_tasks.add_task(write_notification, message)
    return {'message': 'Notification sent in the background'}


async def startup():
    print('Ready to go')
    await database.connect()


async def shutdown():
    print('Close')


routes = [
    APIRoute('/', read_root, response_class=JSONResponse),
    APIRoute('/items/{item_id}', read_item, response_class=JSONResponse),
    APIRoute(
        '/items/add',
        add_item,
        response_class=JSONResponse,
        response_model=ItemAnswer,
        methods=['POST']
    ),
    APIRoute(
        '/send-notification/{message}',
        send_notification,
        response_class=JSONResponse,
        methods=['POST']
    ),
    APIRoute(
        '/users',
        user_list,
        response_class=JSONResponse
    )
]

app = FastAPI(routes=routes, on_startup=[startup], on_shutdown=[shutdown])
