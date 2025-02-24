# 🍽️ Swiggy - Low-Level Design (LLD)

## 📜 Overview
This project is a **Low-Level Design (LLD)** for a **Swiggy-like food delivery system**. It includes key features such as **user management, restaurant operations, order processing, delivery agent assignment, and rating system**.

---

## 🏗️ Class Structure
The system follows an **object-oriented design**, where each entity represents a real-world component of a food delivery platform.

### **🛠️ Core Classes**
| **Class**        | **Responsibilities** |
|------------------|---------------------|
| `Swiggy`        | Singleton class managing users, restaurants, orders, and delivery agents. |
| `User`          | Represents a customer with details like name, location, and order history. |
| `Restaurant`    | Stores restaurant details, menu items, and ratings. |
| `Item`          | Represents individual food items in a restaurant menu. |
| `Order`         | Stores order details, including status and assigned delivery agent. |
| `OrderService`  | Manages order placement, updates, and tracking. |
| `DeliveryAgent` | Represents delivery personnel, tracking their availability and assigned orders. |
| `AgentService`  | Assigns orders to the nearest available delivery agent. |
| `RestaurantService` | Handles restaurant-related operations like adding menu items and searching for nearby restaurants. |
| `UserService`   | Manages user accounts and order history. |
| `Util`          | Contains helper functions like distance calculation. |

---

## 🏗️ UML Diagram
![Swiggy UML](assets/swiggy.drawio.svg)

---

## 🔥 Features Implemented
- ✅ **User Management** – Register users, fetch user details.
- ✅ **Restaurant Service** – Add restaurants, manage menu, get nearby restaurants.
- ✅ **Order Processing** – Place orders, track order status.
- ✅ **Delivery Assignment** – Assign orders to the nearest available agent.
- ✅ **Distance Calculation** – Uses **Pythagorean theorem** to fetch nearby restaurants/agents.
- ✅ **Rating System** – Users can rate restaurants after order completion.

---

## 🛠️ How to Run
```bash
python swiggy_demo.py
