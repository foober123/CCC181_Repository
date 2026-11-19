# Schema Review
1. Order Address Validation: Initially, database did not enforce relationship between order_type and address. I added ck_order_address_by_order_type to make sure walk-in orders have no address and delivery orders have a non-empty address
2. Check constraint for an order item needing a quantity greater than 0. No such thing as an order for negative items in a shop. 

## Scope Decisions
Did not add a separate service entity because it would increase complexity without satisfying a requirement. 
