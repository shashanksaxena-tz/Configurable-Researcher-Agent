import pytest

@pytest.mark.asyncio
async def test_read_main(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    # HealthResponse includes status, app_name, version, timestamp
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data
    assert "version" in data

@pytest.mark.asyncio
async def test_list_modules(client):
    response = await client.get("/api/v1/modules")
    assert response.status_code == 200
    data = response.json()
    # Returns a list of ModuleInfo objects directly, not a dict with "modules" key
    assert isinstance(data, list)
    assert len(data) > 0
    first_module = data[0]
    assert "id" in first_module
    assert "name" in first_module
