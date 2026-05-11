# Expense Tracker API

A RESTful API for tracking personal expenses built with FastAPI and Supabase. Features JWT authentication, expense management, category organization, and spending summary reports.

## Tech Stack

- **FastAPI** — Python web framework for building APIs
- **Supabase** — PostgreSQL database hosting
- **JWT** — Token-based authentication
- **Railway** — Cloud deployment platform

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |

### Categories
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/categories` | Create a category |
| GET | `/categories` | Get all categories |

### Expenses
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/expenses` | Create an expense |
| GET | `/expenses` | Get all expenses |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |

### Reports
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/reports/summary` | Get total spending summary by category |

## Authentication

All endpoints except `/register` and `/login` require a JWT token. Include it in the request header: Authorization: Bearer your_token_here

## Database Schema

- **users** — stores user accounts with hashed passwords
- **categories** — expense categories linked to a user
- **expenses** — individual expenses linked to a user and category
