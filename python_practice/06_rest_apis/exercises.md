# ✍️ Practice Exercises: REST API Design

These exercises will test your understanding of RESTful API naming conventions, HTTP verbs, and status codes. Read the scenarios and try to formulate the correct designs.

---

## Exercise 1: Spot the Violations 🔍
Look at the following endpoint design drafts. Explain why they violate REST conventions, and provide the correct RESTful alternative.

1. **`GET /api/delete_user?id=12`**
   - *Why it's bad:* Uses a verb in the URL (`delete_user`) and uses a `GET` method to mutate/delete data. `GET` requests must be safe and read-only.
   - *Correct RESTful alternative:*
     - Verb: `DELETE`
     - URL: `/api/users/12`

2. **`POST /api/books/update/5`**
   - *Why it's bad:* Uses a verb in the path (`update`).
   - *Correct RESTful alternative:*
     - Verb: `PUT` (for complete updates) or `PATCH` (for partial updates)
     - URL: `/api/books/5`

3. **`POST /api/get_all_active_products`**
   - *Why it's bad:* Uses `POST` (typically for creation) to read data, and includes verbs (`get_all`) and attributes (`active`) in the path.
   - *Correct RESTful alternative:*
     - Verb: `GET`
     - URL: `/api/products?status=active`

---

## Exercise 2: Selecting Query vs. Path Parameters 🛣️
Which parameter type (Path or Query) should you use for the following scenarios?

1. Filtering blogs by a tag named `"tech"`.
   - *Answer:* **Query Parameter**. Filters are optional modifiers to a list of resources.
   - *Example:* `GET /blogs?tag=tech`
2. Fetching a specific blog article with slug name `"learning-fastapi"`.
   - *Answer:* **Path Parameter**. Uniquely identifies a single resource.
   - *Example:* `GET /blogs/learning-fastapi`
3. Paginating user profiles, fetching page 3.
   - *Answer:* **Query Parameter**. Pagination modifications are optional parameters.
   - *Example:* `GET /users?page=3`

---

## Exercise 3: Matching HTTP Status Codes 🔢
Select the most appropriate HTTP status code from (200, 201, 400, 401, 404, 500) for these server scenarios:

1. A user successfully logs in and is returned their profile.
   - *Status Code:* **`200 OK`**
2. A client submits a product registration form but leaves the required `price` field blank.
   - *Status Code:* **`400 Bad Request`** (or `422 Unprocessable Entity` in FastAPI)
3. A client attempts to delete a user profile with an ID that does not exist in the database.
   - *Status Code:* **`404 Not Found`**
4. A user successfully creates a new blog post.
   - *Status Code:* **`201 Created`**
5. A client tries to access a dashboard endpoint without sending a Bearer authentication token.
   - *Status Code:* **`401 Unauthorized`**
