# 🏆 Challenge Task: REST Movie Rental API Design

Your challenge is to design and map out a REST API for a **Movie Rental System**. Write down the URL path, HTTP Method, request body requirements, and success/failure status codes for each of the specifications listed below.

---

## 🎬 Challenge Specifications

### 1. Catalog Management
- **Action A:** Retrieve a list of all movies. Allow filtering by genre (e.g. `Action`, `Comedy`) and sorting by year.
- **Action B:** Add a new movie to the catalog (requires Title, Director, Genre, Release Year, and Stock count).
- **Action C:** Retrieve details of a single movie by its ID.
- **Action D:** Update the stock quantity of a movie.
- **Action E:** Delete a movie from the catalog.

### 2. Rental Transaction Operations
- **Action F:** Rent a movie. This takes a customer's name, their member ID, and the movie ID. This should reduce the movie stock quantity by 1.
- **Action G:** Return a movie. This takes the rental transaction ID and updates the transaction status to "Returned", adding 1 back to the movie stock.

---

## 📝 Design Template
Create a file named `movie_api_design.md` inside this directory and fill it out using this structure:

```markdown
# Movie Rental API Endpoints Design

### 1. List Movies
- **Method:** GET
- **Path:** `/movies`
- **Query Parameters:** `genre` (optional string), `sort_by` (optional string)
- **Success Status Code:** `200 OK`
- **Response Body Example:**
  ```json
  [
    { "id": 1, "title": "Inception", "genre": "Sci-Fi", "release_year": 2010 }
  ]
  ```

### 2. Add Movie
- **Method:** POST
- ...
```

---

## 💡 Pro Challenge (Optional Implementation):
Convert your design into a working Python file named `movie_api.py` using FastAPI! Use an in-memory list database to verify that hitting your endpoints successfully adjusts movie stock levels when rentals are processed!
