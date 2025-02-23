# 🏪 Vending Machine - Low Level Design (LLD)

## 📜 Overview
This repository contains the **Low-Level Design (LLD)** of a **Vending Machine**, demonstrating **Object-Oriented Design principles**, **state management**, and **payment processing**.

## 🎯 Features
- ✅ **Singleton Pattern** for `VendingMachine` to ensure a single instance.  
- ✅ **State Management** using `StateManager` to control product selection, payment, and dispensing.  
- ✅ **Inventory Management** for tracking available products.  
- ✅ **Payment Processing** supporting both **coins** and **notes**.  
- ✅ **Concurrency Handling** with thread-safe singleton instantiation.  

---

## 🏗️ UML Diagram
![Vending Machine UML](assets/vending-machine.drawio.svg)

---

## 📦 Class Design

### **1️⃣ `VendingMachine` (Singleton)**
- Manages **inventory, payment processing, and state transitions**.
- Ensures **only one instance exists** in a multi-threaded environment.

### **2️⃣ `StateManager`**
- Implements the **State Pattern** to prevent invalid operations.
- Tracks states like `IDLE`, `READY`, `WAITING`, `DISPENSE`, and `BALANCE`.

### **3️⃣ `Inventory`**
- Stores available products and handles stock management.

### **4️⃣ `Money` (Abstract Class)**
- Common base class for `Coin` and `Note`.

### **5️⃣ `Coin` & `Note`**
- Implements `Money`, supporting different denominations via `CoinType` and `NoteType` Enums.

### **6️⃣ `PaymentProcessor`**
- Manages balance, validates payments, and returns change.

---

## 🛠️ How to Run
```bash
python vending_machine_demo.py
