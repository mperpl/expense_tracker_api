import pytest


def get_valid_payload():
    return {
        "amount": 50.00,
        "category": "housing",
        "description": "flower_decoration",
        "expense_date": "2025-12-28"
    }

# --- Root & Empty State Tests ---

@pytest.mark.asyncio
async def test_root(client):
    response = await client.get('/')
    assert response.status_code == 200
    assert response.json() == "Expense Tracker API"

@pytest.mark.asyncio
async def test_get_all_empty(client):
    response = await client.get('/expense')
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_by_category_empty(client):
    response = await client.get('/expense/filter/housing')
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_by_id_404(client):
    response = await client.get('/expense/999')
    assert response.status_code == 404
    assert response.json() == {"detail": "not found"}

# --- Create (POST) Tests ---

@pytest.mark.asyncio
async def test_create_expense_valid(client):
    payload = get_valid_payload()
    response = await client.post('/expense', json=payload)

    assert response.status_code == 201
    data = response.json()
    
    assert float(data["amount"]) == payload["amount"] 
    assert data["category"] == payload["category"]
    assert "id" in data

@pytest.mark.asyncio
async def test_create_expense_invalid_amount(client):
    payload = get_valid_payload()
    payload["amount"] = -10.00

    response = await client.post('/expense', json=payload)
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_expense_invalid_category(client):
    payload = get_valid_payload()
    payload["category"] = "invalid_category_name"

    response = await client.post('/expense', json=payload)
    assert response.status_code == 422

# --- Read (GET) Tests ---

@pytest.mark.asyncio
async def test_get_all_expenses(client):
    await client.post('/expense', json=get_valid_payload())
    await client.post('/expense', json=get_valid_payload())

    response = await client.get('/expense')

    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_filter_expenses_by_category(client):
    payload_housing = get_valid_payload()
    payload_housing["category"] = "housing"
    
    payload_other = get_valid_payload()
    payload_other["category"] = "other"

    await client.post('/expense', json=payload_housing)
    await client.post('/expense', json=payload_other)

    response = await client.get('/expense/filter/housing')

    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["category"] == "housing"

# --- Update (PUT) Tests ---

@pytest.mark.asyncio
async def test_update_expense_valid(client):
    create_res = await client.post('/expense', json=get_valid_payload())
    expense_id = create_res.json()['id']

    update_payload = get_valid_payload()
    update_payload["amount"] = 100.00
    update_payload["description"] = "Updated Description"
    
    response = await client.put(f'/expense/{expense_id}', json=update_payload)

    assert response.status_code == 200
    data = response.json()
    
    assert float(data["amount"]) == 100.00 
    assert data["description"] == "Updated Description"

@pytest.mark.asyncio
async def test_update_expense_not_found(client):
    update_payload = get_valid_payload()
    response = await client.put('/expense/9999', json=update_payload)
    assert response.status_code == 404

# --- Delete (DELETE) Tests ---

@pytest.mark.asyncio
async def test_delete_expense_valid(client):
    create_res = await client.post('/expense', json=get_valid_payload())
    expense_id = create_res.json()['id']

    response = await client.delete(f'/expense/{expense_id}')

    assert response.status_code == 204

    get_response = await client.get(f'/expense/{expense_id}')
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_expense_not_found(client):
    response = await client.delete('/expense/9999')
    assert response.status_code == 404