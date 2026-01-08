# Market Price API

**Endpoint**: `GET /api/market-prices?crop={crop}`

**Description**: Returns the current market price for the specified crop.

### Request Parameters
- `crop` (string, required): Name of the crop.

### Response
```json
{
  "status": "success",
  "data": {
    "crop": "Wheat",
    "price_per_quintal": 2500,
    "unit": "INR"
  }
}
```

---

**Endpoint**: `POST /api/profit-estimation`

**Description**: Estimates profit based on estimated yield, market price, and cost.

### Request
```json
{
  "crop": "Wheat",
  "estimated_yield": 3.5,
  "price_per_quintal": 2500,
  "cost_per_quintal": 1500
}
```

### Response
```json
{
  "status": "success",
  "data": {
    "estimated_profit": 3500,
    "currency": "INR"
  }
}
```
