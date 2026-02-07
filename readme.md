
# Django API Foundation - Week 1

## Project Overview

The primary objective of Week 1 was to establish a production-ready Django environment and a secure authentication layer using industry-standard JWT protocols.

---

## Tech Stack

* **Framework:** Django 6.0.2
* **API Toolkit:** Django REST Framework (DRF)
* **Authentication:** SimpleJWT (OAuth 2.0 compliant)
* **Testing:** DRF APITestCase

---

## Key Milestones Achieved

* **Infrastructure:** Initialized a virtualized Python environment and a Django project with a clean "Apps-based" architecture.
* **Identity Management:** Developed a custom User authentication system featuring secure registration and hashed password storage.
* **JWT Integration:** Implemented `djangorestframework-simplejwt` to handle stateless authentication via Access and Refresh tokens.
* **Documentation & Testing:** Established a 100% pass-rate test suite covering both "Happy Path" and "Edge Case" scenarios.

---

## Security & Testing Strategy

Instead of just manual testing, I implemented an automated `APITestCase` suite. This ensures that:

1. **Duplicate Protection:** Users cannot register with an existing username or email.
2. **Token Integrity:** The system detects and rejects tampered or malformed JWTs.
3. **Endpoint Security:** Private views return `401 Unauthorized` without a valid Bearer token.

---

## Handling Test:

Manual Testing is done by POSTMAN and Automated testing is done by Django Test


## API Endpoints Summary

| Method | Endpoint | Description | Auth Required |
| --- | --- | --- | --- |
| `POST` | `/api/auth/register/` | Registers a new user | No |
| `POST` | `/api/auth/login/` | Returns JWT token pair | No |
| `POST` | `/api/auth/token/refresh/` | Renews expired access tokens | Refresh Token |
| `GET` | `/api/auth/test-auth/` | Validates current token status | **Yes** |

---

## Quality Assurance

To ensure system stability, I implemented an automated test suite in `tests.py`.

* **Total Tests:** Normal - 4, Edge - 6
* **Coverage:**

**Normal Case**
1. User creation and password write-only verification.
2. JWT token generation on valid credentials.
3. Permission blocking for unauthorized requests.
4. Token rotation and refresh logic.
5. Duplicate username and email authentications

**Normal Case**
1. Token Based Authentications with tampered,malformed,missing.
2. Token refreshing with invalid token

---

## Documentation of API:

Used Django REST Framework - Yet Another Swagger Generator for API Documentation. It turned my live code into Interactive instruction manual.

1. Swagger UI: A webpage where you can see all your endpoints, see what JSON they expect, and even click a "Try it out" button to run requests directly from your browser.

2. Redoc: A more professional, clean, and organized version of your documentation (great for "Read Only" docs).

* `Swagger UI` → **Endpoints visible**

---

## Takeaway of WEEK 1:

* **Setting up Django Project:** Project is created in the name of ai_prompt_manager and a virtual environment for the project
* **Implementing Authentication:** The user login, registration and session are secured based on Token Authentications system in users app.
* **Testing the Flow:** The basic test is conducted using POSTMAN based on POST and GET actions. The Test is verified and conducted Automated test cases via tests.py with Normal Case of 4 and Edge Cases of 6
* **Created API Documentation:** The documentation of API is done based on "Django REST Framework - Yet Another Swagger Generator."

**Everything went green, so this is the wrap of WEEK ONE**
---
