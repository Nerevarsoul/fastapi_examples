import uuid

import databases

from sqlalchemy import Column, MetaData, Table, String
from sqlalchemy.dialects.postgresql import UUID
from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route


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


def homepage(request):
    return PlainTextResponse('Hello, world!')


def homepage_json(request):
    return JSONResponse({'Hello': 'World!'})


async def user_list(request):
    query = users.select()
    results = await database.fetch_all(query)
    content = [
        {
            'id': str(result['id']),
            'first_name': result['first_name']
        }
        for result in results
    ]
    return JSONResponse({'res': content})


async def startup():
    print('Ready to go')
    await database.connect()


routes = [
    Route('/', homepage),
    Route('/json', homepage_json),
    Route('/users', user_list)
]

app = Starlette(debug=True, routes=routes, on_startup=[startup])
