# Farmer Profile API

**Endpoint**: `GET /api/farmer-profile`

**Description**: Retrieves the profile information of the current farmer.

### Response
```json
{
  "status": "success",
  "data": {
    "name": "John Doe",
    "location": "Bangalore, Karnataka",
    "land_acres": 2.5,
    "language": "en"
  }
}
```

---

**Endpoint**: `POST /api/farmer-profile`

**Description**: Updates the profile information of the current farmer.

### Request
```json
{
  "name": "John Doe",
  "location": "Bangalore, Karnataka",
  "land_acres": 2.5,
  "language": "en"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "status": "profile updated"
  }
}
```
