# Module 09: Testing in Python & FastAPI 🧪

In this module, you will learn how to write automated tests for your code. Tests verify that your software works as expected and guarantees that making future code modifications won't break existing features (preventing regressions).

---

## 📚 Topics Covered

1. **Pytest Framework**: The standard, most popular testing library in Python.
2. **Test Naming Conventions**: Pytest automatically scans files starting with `test_*.py` and runs functions starting with `def test_*()`.
3. **Assertions**: Writing logical statements like `assert result == expected_output`. If the statement evaluates to `True`, the test passes; if `False`, the test fails.
4. **FastAPI `TestClient`**: Importing `TestClient` from `fastapi.testclient` to simulate hitting your API endpoints without running the server on a port. This makes integration testing lightning fast!
5. **Fixtures (Optional Concept)**: Reusable setup code blocks that prepare databases or mock payloads before tests run.

---

## ⚙️ Running Your Tests

To run pytest:
1. Ensure your virtual environment is active.
2. Install pytest (already in `requirements.txt`):
   ```bash
   pip install pytest
   ```
3. Run the following command from the root of `09_testing/` (or run it globally pointing to this folder):
   ```bash
   pytest
   ```
   *Pytest will automatically scan and run all assertions in `test_basics.py` and `test_api.py`!*

---

## 🗂️ Files in this Module

- `test_basics.py`: Unit tests for helper functions (math and string modifications).
- `test_api.py`: API integration tests using FastAPI's `TestClient` on a simple mock server.
- `challenge.py`: A challenge script asking you to write unit and API tests for an order discounts system. Run it using:
  ```bash
  pytest challenge.py
  ```
