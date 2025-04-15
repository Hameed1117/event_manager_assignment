from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_openapi_schema_includes_security_scheme():
    """Test that the OpenAPI schema includes the Bearer security scheme."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    
    # Parse the response JSON
    schema = response.json()
    
    # Verify that the components section exists with securitySchemes
    assert "components" in schema
    assert "securitySchemes" in schema["components"]
    assert "Bearer" in schema["components"]["securitySchemes"]
    
    # Verify the properties of the Bearer security scheme
    bearer_scheme = schema["components"]["securitySchemes"]["Bearer"]
    assert bearer_scheme["type"] == "http"
    assert bearer_scheme["scheme"] == "bearer"
    assert bearer_scheme["bearerFormat"] == "JWT"