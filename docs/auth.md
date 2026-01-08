# Authentication API

**Register Endpoint**: `POST /api/register`

**Description**: Registers a new farmer user with email, username, and password.

### Request
```json
{
  "username": "farmer_jay",
  "email": "jay@example.com",
  "password": "strongpassword123"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "status": "User registered",
    "user_id": "60d5ecb5f1d2b2a1a8e1e1e1"
  }
}
```

---

**Login Endpoint**: `POST /api/login`

**Description**: Authenticates a user and returns a JWT token for further requests.

### Request
```json
{
  "email": "jay@example.com",
  "password": "strongpassword123"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```
