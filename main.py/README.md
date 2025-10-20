## 🐱 Dynamic Profile API (Stage Zero Backend Task)

A simple RESTful API built with **FastAPI** that returns your profile information along with a **dynamic cat fact** fetched from the [Cat Facts API](https://catfact.ninja/fact).

This project demonstrates consuming a third-party API, formatting JSON responses, handling errors gracefully, and returning dynamic data.

---

### 📌 **Endpoint**

**`GET /me`**

#### Example Response
```json
{
  "status": "success",
  "user": {
    "email": "your_email@example.com",
    "name": "Your Full Name",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-19T12:34:56.789Z",
  "fact": "Cats sleep 70% of their lives."
}
