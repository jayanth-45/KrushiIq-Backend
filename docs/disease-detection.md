# Disease Detection API

**Endpoint**: `POST /api/disease-detection`

**Description**: Detects crop disease from a leaf image URL and returns disease name with severity.

### Request
```json
{
  "image_url": "https://example.com/leaf.jpg",
  "crop": "Wheat"
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "disease": "Leaf Blight",
    "severity": "medium"
  }
}
```
