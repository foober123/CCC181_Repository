| Rule                               | Layer    | How I tested | Result                                                                                            |
|------------------------------------|----------|--------------|---------------------------------------------------------------------------------------------------|
| Walk-in Orders have no addresses   | database | `INSERT INTO orders (customer_name, order_type, address)
VALUES ('Test Invalid Walk-in', 'WALK_IN', '123 Sample Street');` in PSQL   | ERROR:  new row for relation "orders" violates check constraint "ck_orders_address_by_order_type" |
| Delivery Orders require an address | database | `INSERT INTO orders (customer_name, order_type, address)
VALUES ('Test Invalid Delivery', 'DELIVERY', NULL);`           | ERROR:  new row for relation "orders" violates check constraint "ck_orders_address_by_order_type" |

