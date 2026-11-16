# Delivery Queue requirements
**Setting:** Warehouse, Office inside warehouse
**People who wait:** Customers who tell their orders to the business owner via phone call or in-person
**People who Serve:** Business owners (e.g Manang In-In and Cartso)

**Problem Statement:** Business Owners need to Track order status so that deliveries are not delayed and customers dont leave over frustration with the service order

## Functional Requirements

| ID    | Requirement                                                                         | Priority | Stores Data | Status        |
| ---   | ---                                                                                 | ---      | ---         | ---           |
| FR-01 | Push an order to the Queue                                                          | Must     | Yes         | Done (Week 3) |
| FR-02 | Check Pending Orders                                                                | Must     | Yes         | Done (Week 3) |
| FR-03 | View Order Details                                                                  | Must     | Yes         | Done (Week 3) |
| FR-04 | Mark order as Complete                                                              | Must     | Yes         | Done (Week 3)              |
| FR-05 | Mark order as Cancelled                                                             | Must     | Yes         | Done (Week 3)              |
| FR-06 | Mark order as IN_TRANSIT                                                            | Must     | Yes         | Done (Week 3)              |
| FR-07 | Name and address are separate ★                                                     | Must     | Yes         | Later                      |
| FR-08 | System rejects any attempt to register a Walk-In service as IN_TRANSIT ★            | Must     | Yes         | Later                      |
| FR-09 | Filter Orders that are in progress (i.e orders with a WAITING or IN_TRANSIT status) | Must     | No          | Done (Week 3)              |
| FR-10 | Walk-in orders have no address  ★                                                   | Must     | Yes         | Later                      |

## Non-Functional Requirements
| ID     | Requirement                                                                               | Category       | Priority |
| ---    | ---                                                                                       | ---            | ---      |
| NFR-01 | App will restrict access to authorized business owners                                    | Security       | Could    |
| NFR-02 | The system retains order details and status changes. No duplicated records during testing | Data Integrity | Must     |
| NFR-03 | System history that records date and time when an order's status is changed               | Auditability   | Could    |
| NFR-04 | App loads within 3 seconds                                                                | Performance    | Must     |


## MVP
| ID    | Requirement                                                                         | Priority | Stores Data | Status        |
| ---   | ---                                                                                 | ---      | ---         | ---           |
| FR-01 | Push an order to the Queue                                                          | Must     | Yes         | Done (Week 3) |
| FR-02 | Check Pending Orders                                                                | Must     | Yes         | Done (Week 3) |
| FR-03 | View Order Details                                                                  | Must     | Yes         | Done (Week 3) |
| FR-04 | Mark order as Complete                                                              | Must     | Yes         | Done (Week 3)              |
| FR-05 | Mark order as Cancelled                                                             | Must     | Yes         | Done (Week 3)              |
| FR-06 | Mark order as IN_TRANSIT                                                            | Must     | Yes         | Done (Week 3)              |
| FR-07 | Name and address are separate ★                                                     | Must     | Yes         | Later                      |
| FR-08 | System rejects any attempt to register a Walk-In service as IN_TRANSIT ★            | Must     | Yes         | Later                      |
| FR-09 | Filter Orders that are in progress (i.e orders with a WAITING or IN_TRANSIT status) | Must     | No          | Done (Week 3)              |
| FR-10 | Walk-In Orders have no address  ★                                                   | Must     | Yes         | Later                      |

**Out of Scope:**
1. Inventory Management, system only needs to know items only belong to a particular ticket
2. Customer Registration, system only needs basic customer identification like name and address. Maintaining customer profiles is not necessary for order processing 


## Check Requirements With a Real Person

| Who (Role Only) | What They Said                  | What I changed              |
| ---             | ---                             | ---                         |
| Business Owner  | some customer names are similar | FR-07 (from Should to Must) [must |](|)
