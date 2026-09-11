# Deactivated serial numbers

`/products/<product-id>/blacklist-serial-numbers.json` contains deactivated
devices for one exact hardware product ID.

```json
{
  "schemaVersion": 1,
  "productId": "3.2",
  "entries": [
    {
      "year": 2026,
      "month": 7,
      "unit": 1,
      "message": "This SmartBroom has been deactivated. Please contact us at curling@smartbroom.ca for assistance."
    }
  ]
}
```

Clients compare `year`, `month`, and `unit` numerically. A failed request,
schema validation failure, or product-ID mismatch must never deactivate a
device.
