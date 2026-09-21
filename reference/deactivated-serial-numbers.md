# Deactivated serial numbers

`/v1/products/<product-id>/blacklist-serial-numbers.json` contains deactivated
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

## Reserved product IDs

Product ID `2.0` is reserved for TNG-era SmartBroom hardware and has no units
yet. TNG hardware does not report a product ID, so clients identify its TNG
calibration service and use `2.0` for deactivation checks. Its empty manifest
is published now so clients can validate that contract before a unit is
allocated. Add an entry only when a TNG unit must be deactivated.
