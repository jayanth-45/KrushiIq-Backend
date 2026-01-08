# Weather API

**Endpoint**: `GET /api/weather?location={location}`

**Description**: Returns current weather data for the specified location.

### Request Parameters
- `location` (string, required): City name or coordinates.

### Response
```json
{
  "status": "success",
  "data": {
    "temperature": 28,
    "humidity": 70,
    "rainfall": 0,
    "description": "Clear sky"
  }
}
```

---

**Endpoint**: `GET /api/weather-forecast?location={location}`

**Description**: Returns a 7‑day weather forecast.

### Response
```json
{
  "status": "success",
  "data": {
    "forecast": [
      {"day": "Day 1", "temperature": 28, "humidity": 70, "rainfall": 0},
      {"day": "Day 2", "temperature": 30, "humidity": 65, "rainfall": 0},
      {"day": "Day 3", "temperature": 27, "humidity": 75, "rainfall": 2},
      {"day": "Day 4", "temperature": 26, "humidity": 80, "rainfall": 5},
      {"day": "Day 5", "temperature": 29, "humidity": 68, "rainfall": 0},
      {"day": "Day 6", "temperature": 31, "humidity": 60, "rainfall": 0},
      {"day": "Day 7", "temperature": 28, "humidity": 70, "rainfall": 1}
    ]
  }
}
```
