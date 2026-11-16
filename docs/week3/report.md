# Week 3 report
App: Delivery Queue, Order Tracking system for walk-ins and deliveries
Setting: Beverage Warehouse
Name: Charlson Y. Fabrigar
ID: 2024-0796
Date: November 16, 2026

## Personas
Manang In-In, Business owner who offers walk-ins and deliveries. Woman in her 40s with moderate tech skills and eyesight problems. Top Tasks: Mark deliveries as In Transit (FR-05), View Order Details (FR-06)

Mr. Cartso, Business owner of a warehouse that only takes walkins. 50 Y.O man with experience with MS Excel and other spreadsheet software. Top Tasks: View Order Details (FR-06) 

## Screens
| Screenshot                                             | Persona      | Requirements               |
|--------------------------------------------------------|--------------|----------------------------|
| [Join, Phone/Tablet](screenshots/join_phone.png)       | Manang In-In | FR-01                      |
| [Staff, Phone/Tablet](screenshots/staff_phone.png)     | Manang In-In | FR-02, FR-03, FR-04, FR-05 |
| [Ticket, Phone/Tablet](screenshots/ticket_phone.png)   | Manang In-In | FR-06                      |
| [Join, Phone/Tablet](screenshots/join_desktop.png)     | Cartso       | FR-01                      |
| [Staff, Phone/Tablet](screenshots/staff_desktop.png)   | Cartso       | FR-02, FR-03, FR-04        |
| [Ticket, Phone/Tablet](screenshots/ticket_desktop.png) | Cartso       | FR-06                      |

## Design Decisions
1. Light mode because persona with tablet or mobile device might use queuing app outdoors. [Sources](https://www.mockplus.com/blog/post/dark-mode-vs-light-mode-which-one-is-better) say that light mode is easier to read in natural or artificial light
2. Order Details are omitted from the dashboard because it needs to stay brief. Order of tickets is the concern and adding orders to dashboard tickets causes information overload. Details can be checked in the my place page for verifying purposes

## Usability
I let my mother test the application and she took 5 mins to complete an order. She hesitated when adding an order and found a stale button

## Reflection
* Hardest part: getting used to Python and Web development. There is no `while(1)` loop for me to add features in and I spent more time adjusting to python syntax and the flask framework than reasoning API boundaries
* What To Change:
    - Add date to orders
    - Introduce more horizontal stacking to mobile version
    - Make Orders with a delivery service count as Ahead when checking a Walk-In Order

## Declaration
I used GPT-6.0 for syntax help with python and HTML
