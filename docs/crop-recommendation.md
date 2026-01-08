# Crop Recommendation API

**Endpoint**: `POST /api/crop-recommendation`

**Description**: Returns recommended crops based on soil nutrients, pH, location and season.

### Request
```json
{
  "soil_n": 50,
  "soil_p": 30,
  "soil_k": 40,
  "ph": 6.5,
  "location": "Bangalore",
  "season": "Kharif"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "recommended_crops": ["Wheat", "Rice"],
    "confidence": 0.87
  }
}
```
