# Pesticide Recommendation API

**Endpoint**: `POST /api/pesticide-recommendation`

**Description**: Provides pesticide recommendation and dosage based on disease, crop, and area.

### Request
```json
{
  "disease": "Leaf Blight",
  "crop": "Wheat",
  "area_acres": 2.0
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "pesticide": "Cypermethrin",
    "dosage_per_acre": 0.5,
    "eco_friendly_alternative": "Neem Oil"
  }
}
```
