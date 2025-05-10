from builtins import str
import pytest
from httpx import AsyncClient
from app.main import app
from app.models.user_model import User, UserRole
from app.utils.nickname_gen import generate_nickname
from app.utils.security import hash_password
from app.services.jwt_service import decode_token  # Import your FastAPI app
from app.dependencies import get_settings, get_current_user, require_role
from app.routers.user_routes import admin_or_manager_only
from app.dependencies import  get_email_service


# Example of a test function using the async_client fixture
@pytest.mark.asyncio
async def test_create_user_access_denied(async_client_factory):
    async with async_client_factory(override_user=True, role="AUTHENTICATED") as client:
        headers = {"Authorization": "Bearer faketoken"}
        user_data = {
            "nickname": generate_nickname(),
            "email": "test@example.com",
            "password": "sS#fdasrongPassword123!",
        }

        response = await client.post("/users/", headers=headers, json=user_data)
        assert response.status_code == 403

# You can similarly refactor other test functions to use the async_client fixture
@pytest.mark.asyncio
async def test_retrieve_user_access_denied(async_client, verified_user, user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    response = await async_client.get(f"/users/{verified_user.id}", headers=headers)
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_retrieve_user_access_allowed(async_client, admin_user, admin_token):
    app.dependency_overrides[get_current_user] = lambda: {
    "user_id": "admin-id",
    "role": "ADMIN"
}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.get(f"/users/{admin_user.id}", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["id"] == str(admin_user.id)

@pytest.mark.asyncio
async def test_update_user_email_access_denied(async_client_factory, verified_user, user_token):
    updated_data = {"email": f"updated_{verified_user.id}@example.com"}
    async with async_client_factory(override_user=True, role="AUTHENTICATED") as client:
        headers = {"Authorization": f"Bearer {user_token}"}
        response = await client.put(f"/users/{verified_user.id}", json=updated_data, headers=headers)
        assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client_factory, admin_user, admin_token):
    updated_data = {"email": f"updated_{admin_user.id}@example.com"}
    async with async_client_factory(override_user=False) as client:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == updated_data["email"]

@pytest.mark.asyncio
async def test_update_user_email_access_allowed(async_client_factory, admin_token, admin_user):
    async with async_client_factory(override_user=False) as client:
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(f"/users/{admin_user.id}", json={"email": "new@example.com"}, headers=headers)
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_user(async_client_factory, admin_user, admin_token):
    async with async_client_factory(override_user=False) as client:
        headers = {"Authorization": f"Bearer {admin_token}"}
        delete_response = await client.delete(f"/users/{admin_user.id}", headers=headers)
        assert delete_response.status_code == 204

         # Verify the user is deleted
        fetch_response = await client.get(f"/users/{admin_user.id}", headers=headers)
        assert fetch_response.status_code == 404

@pytest.mark.asyncio
async def test_create_user_duplicate_email(async_client_factory, verified_user):
    async with async_client_factory() as client:
        user_data = {
            "email": verified_user.email,
            "password": "AnotherPassword123!",
            "role": UserRole.ADMIN.name
        }
        response = await client.post("/register/", json=user_data)
        assert response.status_code == 400
        assert "Email already exists" in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_create_user_invalid_email(async_client_factory):
    async with async_client_factory() as client:
        user_data = {
            "email": "notanemail",
            "password": "ValidPassword123!",
        }
        response = await client.post("/register/", json=user_data)
        assert response.status_code == 422

import pytest
from app.services.jwt_service import decode_token
from urllib.parse import urlencode

@pytest.mark.asyncio
async def test_login_success(async_client_factory, verified_user):
    async with async_client_factory() as client:
        form_data = {
            "username": verified_user.email,
            "password": "MySuperPassword$1234"
        }
        response = await client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        decoded_token = decode_token(data["access_token"])
        assert decoded_token["role"] == "AUTHENTICATED"

@pytest.mark.asyncio
async def test_login_user_not_found(async_client_factory):
    async with async_client_factory() as client:
        form_data = {
            "username": "nonexistentuser@here.edu",
            "password": "DoesNotMatter123!"
        }
        response = await client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 401
        assert "Incorrect email or password." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_login_incorrect_password(async_client_factory, verified_user):
    async with async_client_factory() as client:
        form_data = {
            "username": verified_user.email,
            "password": "IncorrectPassword123!"
        }
        response = await client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 401
        assert "Incorrect email or password." in response.json().get("detail", "")


@pytest.mark.asyncio
async def test_login_unverified_user(async_client_factory, unverified_user):
    async with async_client_factory() as client:
        form_data = {
            "username": unverified_user.email,
            "password": "MySuperPassword$1234"
        }
        response = await client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_locked_user(async_client_factory, locked_user):
    async with async_client_factory() as client:
        form_data = {
            "username": locked_user.email,
            "password": "MySuperPassword$1234"
        }
        response = await client.post("/login/", data=urlencode(form_data), headers={"Content-Type": "application/x-www-form-urlencoded"})
        assert response.status_code == 400
        assert "Account locked due to too many failed login attempts." in response.json().get("detail", "")

@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client_factory, admin_token):
    non_existent_user_id = "00000000-0000-0000-0000-000000000000"
    async with async_client_factory(override_user=False) as client:
        headers = {"Authorization": f"Bearer {admin_token}"}
        delete_response = await client.delete(f"/users/{non_existent_user_id}", headers=headers)
        assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_update_user_github(async_client, admin_user, admin_token):
    updated_data = {"github_profile_url": "http://www.github.com/kaw393939"}
    headers = {"Authorization": f"Bearer {admin_token}"}
    response = await async_client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["github_profile_url"] == updated_data["github_profile_url"]

@pytest.mark.asyncio
async def test_update_user_linkedin(async_client_factory, admin_user, admin_token):
    async with async_client_factory(override_user=False) as client:
        # Simulate the admin user
        app.dependency_overrides[get_current_user] = lambda: {
            "user_id": str(admin_user.id),
            "role": UserRole.ADMIN.name
        }
        updated_data = {"linkedin_profile_url": "http://www.linkedin.com/kaw393939"}
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = await client.put(f"/users/{admin_user.id}", json=updated_data, headers=headers)
        assert response.status_code == 200
        assert response.json()["linkedin_profile_url"] == updated_data["linkedin_profile_url"]

@pytest.mark.asyncio
async def test_list_users_as_admin(async_client_factory, admin_token):
    async with async_client_factory(override_user=False) as client:
        # Simulate the admin user
        app.dependency_overrides[get_current_user] = lambda: {
            "user_id": "admin-id",
            "role": UserRole.ADMIN.name
        }
        # Test the endpoint
        response = await client.get(
            "/users/",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        assert 'items' in response.json()
        # Check if the response contains a list of users
        assert isinstance(response.json()['items'], list)
        # Check if the list is not empty
        assert len(response.json()['items']) > 0
        assert response.status_code == 200
        assert 'items' in response.json()

@pytest.mark.asyncio
async def test_list_users_as_manager(async_client_factory, manager_token):
    async with async_client_factory(override_user=False) as client:
        # Simulate the manager user
        app.dependency_overrides[get_current_user] = lambda: {
            "user_id": "manager-id",
            "role": UserRole.MANAGER.name
        }
        # Test the endpoint 
        response = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {manager_token}"}
    )
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_list_users_unauthorized(async_client_factory, user_token):
    async with async_client_factory(override_user=True) as client:
        # Simulate the regular user
        app.dependency_overrides[get_current_user] = lambda: {
            "user_id": "user-id",
            "role": UserRole.AUTHENTICATED.name
        }
        # Test the endpoint
        response = await client.get(
        "/users/",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden, as expected for regular user
