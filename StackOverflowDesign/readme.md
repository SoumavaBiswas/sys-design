# 🏆 Stack Overflow - Low-Level Design (LLD)

## 📜 Overview
This repository contains the **Low-Level Design (LLD)** for a **Stack Overflow-like system**, implementing **user management, question & answer functionality, voting system, and reputation tracking**.

## 🎯 Features
- ✅ **Singleton `StackOverflow` class** – Ensures a centralized system for managing users, questions, and answers.
- ✅ **User Management** – Users can ask questions, post answers, and gain reputation.
- ✅ **Voting System** – Supports upvoting/downvoting questions & answers.
- ✅ **Reputation System** – Users earn/lose points based on community interactions.
- ✅ **Search Functionality** – Users can search for questions by tags or user contributions.
- ✅ **Commenting System** – Users can add comments to answers.

---

## 🏗️ UML Diagram
![Stack Overflow UML](assets/stack-overflow.drawio.svg)

---

## 📦 Class Design

### **1️⃣ `StackOverflow` (Singleton)**
- Maintains dictionaries for:
  - `users` (`{user_id: User}`)
  - `questions` (`{qsn_id: Questionary}`)
  - `answers` (`{ans_id: Answer}`)
- Manages user registration, question creation, answer posting, voting, and search.

### **2️⃣ `User`**
- Attributes: `user_id`, `name`, `questions[]`, `reputation`.
- Methods: `add_question()`, `update_reputation()`.

### **3️⃣ `Questionary`**
- Attributes: `qsn_id`, `user_id`, `title`, `body`, `answers[]`, `tags`, `votes`.
- Methods: `add_answer()`, `upvote()`.

### **4️⃣ `Answer`**
- Attributes: `ans_id`, `qsn_id`, `user_id`, `body`, `votes`, `comments[]`.
- Methods: `upvote()`, `add_comment()`.

---

## 🛠️ How to Run
```bash
python stackoverflow_demo.py
