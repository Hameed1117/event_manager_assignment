from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse
from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.utils.api_description import getDescription
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

@app.exception_handler(Exception)
async def exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": "An unexpected error occurred."})

app.include_router(user_routes.router)

# Custom OpenAPI schema to add security definitions for Swagger UI
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes to the OpenAPI schema
    openapi_schema["components"] = {
        "securitySchemes": {
            "Bearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter the token you received from the /login endpoint. Format: Bearer YOUR_TOKEN"
            }
        }
    }
    
    # Apply the security globally to all endpoints that use the oauth2_scheme
    # This ensures that the Authorize button will appear in Swagger UI
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Replace the default OpenAPI schema with our custom one
app.openapi = custom_openapi