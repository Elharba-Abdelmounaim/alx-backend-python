# 🧪 ALX Backend Python: Unittests & Integration Tests

> This project is part of the **ALX Software Engineering** program.  
> Its focus is on mastering **unit testing**, **mocking**, and **integration testing** in Python.

---

## 📁 Project Structure

alx-backend-python/
└── 0x03-Unittests_and_integration_tests/
├── client.py # Contains the Client class that fetches GitHub org info
├── utils.py # Helper functions for accessing nested structures and JSON fetching
├── test_utils.py # Unit tests for functions in utils.py
├── fixtures.py # Dummy data (used in integration tests)
└── venv/ # Optional: Virtual environment for dependencies

---

## 🧰 Features Covered

- ✅ **Unit Testing** with `unittest`
- ✅ **Mocking** external API calls with `unittest.mock`
- ✅ **Parameterized Tests** with `parameterized`
- ✅ **Integration Testing** using fixtures

---

## ⚙️ How to Run

### 1. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate

2. Install dependencies

pip install requests parameterized

3. Run the tests

python3 -m unittest test_utils.py

Or run all tests:

python3 -m unittest discover
```
🧠 Logic Flow Diagram (Mermaid)
The following diagram shows how the Client class fetches GitHub organization data:


flowchart TD
    A[Client Class] --> B[get_org]
    B --> C[utils.get_json]
    C --> D[requests.get(url)]
    D --> E[Return JSON data]
You can visualize this Mermaid diagram on GitHub or with a Markdown preview extension in VS Code.


