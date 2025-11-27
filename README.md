# 💰 Expense Tracker API

A simple RESTful API designed for tracking and managing personal expenses.

---

## 🚀 Technologies

* **Language:** Python 3.x
* **API Framework:** FastAPI
* **Data Validation:** Pydantic
* **Database:** SQLite
* **ORM:** SQLAlchemy
---

## ✨ Key Features

The API provides standard CRUD (Create, Read, Update, Delete) operations for expense management:

| Function | Description | Endpoint | HTTP Method |
| :--- | :--- | :--- | :--- |
| **Add Expense** | Registers a new expense (amount, category, description, date). | `/expenses/` | `POST` |
| **Get Expense** | Retrieves details of a single expense by ID. | `/expenses/{expense_id}` | `GET` |
| **List Expenses** | Retrieves a list of all recorded expenses. | `/expenses/` | `GET` |
| **Update Expense**| Modifies an existing expense entry. | `/expenses/{expense_id}` | `PUT` / `PATCH` |
| **Delete Expense** | Permanently removes an expense entry. | `/expenses/{expense_id}` | `DELETE` |
