from starlette.applications import Starlette
from starlette.responses import PlainTextResponse, JSONResponse
from starlette.routing import Route


def homepage(request):
    return PlainTextResponse('Hello, world!')


def homepage_json(request):
    return JSONResponse({'Hello': 'World!'})


routes = [
    Route('/', homepage),
    Route('/json', homepage_json),
]

app = Starlette(debug=True, routes=routes)
