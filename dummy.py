from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, HTTPException, Depends

app = FastAPI()


def my_schema():
    openapi_schema = get_openapi(
        title="The Amazing Programming Language Info API",
        version="1.0",
        routes=app.routes,
    )
    openapi_schema["info"] = {
        "title": "The Amazing Programming Language Info API",
        "version": "1.0",
        "description": "Learn about programming language history!",
        "termsOfService": "http://programming-languages.com/terms/",
        "contact": {
            "name": "Get Help with this API",
            "url": "http://www.programming-languages.com/help",
            "email": "support@programming-languages.com"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
        },
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

    print(routes)


app.openapi = my_schema
