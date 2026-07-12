# Price Module

This folder contains the price calculation helpers for the Smart Stay project.

## Files

- `price_calculator.py` - price calculation functions and Excel loader.
- `group_discount_rules_example.xlsx` - example Excel file for group discount rules.

## How to use

### 1. Excel discount rules format

The Excel file must contain columns for:
- `min_size` / `min_count` / `minimum`
- `max_size` / `max_count` / `maximum`
- `discount` / `discount_amount` / `discount_percent`

Example rows:

| min_size | max_size | discount |
|----------|----------|----------|
| 1        | 4        | 0        |
| 5        | 9        | 50       |
| 10       | 14       | 10%      |
| 15       | 20       | 100      |

This means:
- group size 1-4: no discount
- group size 5-9: fixed 50 shekel discount
- group size 10-14: 10% discount
- group size 15-20: fixed 100 shekel discount

### 2. Using the API in Swagger

Run the FastAPI app and open Swagger at:

- `http://localhost:8000/docs`

Then:
1. Choose `POST /price/group-pricing/excel`
2. Provide `group_id` as a form value.
3. Upload the Excel file under `file`.
4. Click `Execute`.

The response returns:
- `GroupID`
- `VacationID`
- `GroupSize`
- `BasePrice`
- `TotalPrice`
- `MemberPrices`

### 3. Using JSON directly

If you want to skip Excel, use `POST /price/group-pricing/json`.

Example JSON body:

```json
{
  "group_id": 1,
  "discount_rules": [
    {"min_size": 5, "max_size": 9, "discount": 50},
    {"min_size": 10, "max_size": 14, "discount": "10%"}
  ]
}
```

### 4. Using Python code directly

Import from the module:

```python
from price.price_calculator import (
    load_group_discount_rules,
    calculate_group_pricing,
    calculate_group_pricing_from_excel,
)

rules = load_group_discount_rules("price/group_discount_rules_example.xlsx")
result = calculate_group_pricing(db, group_id=1, discount_rules=rules)

# or
result = calculate_group_pricing_from_excel(db, group_id=1, excel_path="price/group_discount_rules_example.xlsx")
```

### 5. Notes

- The Excel loader supports both fixed amount discounts and percentage discounts.
- `calculate_group_pricing` uses the group size and the discount table to compute the total group price.
- Preference extra price is added per group member only if the member has a preference with additional cost.
