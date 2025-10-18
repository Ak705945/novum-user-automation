# User Management API Automation Framework

## 📋 Project Overview

A comprehensive Python-based API automation testing framework for User Management RESTful APIs. This framework implements industry best practices with clear separation of concerns, reusable components, and detailed test reporting using Allure.

### Key Highlights
-  **30~ comprehensive test cases** covering positive, negative, and edge scenarios
-  **Multi-environment support** (test/staging/production)
-  **Rich Allure reports** with request/response details
-  **Pydantic validation** for data integrity
-  **Retry mechanism** for handling transient failures
-  **Detailed logging** with configurable levels

---

## 🏗️ Project Structure

```
api_automation_framework/
│
├── api/                           # API Encapsulation Layer
│   ├── __init__.py
│   ├── models.py                  # Pydantic models for validation
│   └── user_api.py                # User API client methods
│
├── common/                        # Common Utilities
│   ├── __init__.py
│   ├── assertions.py              # Custom assertions with detailed messages
│   ├── config_reader.py           # Configuration management (singleton)
│   ├── logger.py                  # Logging setup (singleton)
│   └── request_handler.py         # HTTP client with retry mechanism
│
├── config/                        # Configuration Files
│   ├── config.json                # Environment configurations
│   └── test_data.json             # Test data templates
│
├── testcases/                     # Test Cases by API Module
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures and hooks
│   ├── test_create_user.py        # 7 test cases
│   ├── test_get_user.py           # 6 test cases
│   ├── test_update_user.py        # 6 test cases
│   ├── test_delete_user.py        # 6 test cases
│   └── test_batch_query_users.py  # 13 test cases
│
├── reports/                       # Allure test reports (auto-generated)
├── logs/                          # Test execution logs (auto-generated)
├── requirements.txt               # Python dependencies
└── README.md                      # Project documentation
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **pip** package manager
- **Allure CLI** (for viewing reports)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd novum-user-automation
```

#### 2. Create Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Install Allure Command-Line Tool

**macOS:**
```bash
brew install allure
```

**Windows (using Scoop):**
```bash
scoop install allure
```

**Linux:**
```bash
# Download from GitHub releases
wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz
tar -zxvf allure-2.24.0.tgz
sudo mv allure-2.24.0 /opt/allure
echo 'export PATH="/opt/allure/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

#### 5. Configure Base URL

Edit `config/config.json` and update the base URL for your environment:

```json
{
  "environments": {
    "test": {
      "base_url": "http://your-test-api.example.com",
      "timeout": 30,
      "retry_times": 3,
      "retry_delay": 1
    }
  }
}
```

---

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests with Allure reporting
pytest testcases/ --alluredir=reports

# Run with verbose output
pytest testcases/ --alluredir=reports -v

# Run with real-time log output
pytest testcases/ --alluredir=reports -v -s
```

### Run Specific Tests

```bash
# Run specific test file
pytest testcases/test_create_user.py --alluredir=reports

# Run specific test class
pytest testcases/test_create_user.py::TestCreateUser --alluredir=reports

# Run specific test method
pytest testcases/test_create_user.py::TestCreateUser::test_create_user_normal --alluredir=reports
```

### Environment Switching

```bash
# Run tests in different environments
TEST_ENV=test pytest testcases/ --alluredir=reports
TEST_ENV=staging pytest testcases/ --alluredir=reports
TEST_ENV=production pytest testcases/ --alluredir=reports

# Windows
set TEST_ENV=staging && pytest testcases/ --alluredir=reports
```

---

## 📊 Viewing Test Reports

### Option 1: Serve Allure Report (Recommended)
```bash
# Generate and open Allure report in browser
allure serve reports
```

This command will:
- Generate the report from test results
- Start a local web server
- Automatically open the report in your default browser

### Option 2: Generate Static HTML Report
```bash
# Generate static HTML report
allure generate reports -o reports/html --clean

# Open the report
# Windows
start reports/html/index.html

# macOS
open reports/html/index.html

# Linux
xdg-open reports/html/index.html
```

### Allure Report Features

The Allure report includes:
- ✅ **Overview Dashboard**: Pass rate, total tests, duration
- 📈 **Graphs & Charts**: Test execution trends, severity distribution
- 🗂️ **Test Suites**: Tests organized by feature and story
- ⏱️ **Timeline**: Test execution sequence visualization
- 🐛 **Failed Tests**: Detailed failure analysis with stack traces
- 📨 **Request/Response**: Full HTTP details for each API call
- 📎 **Attachments**: Logs, screenshots, and custom data

---

## 📝 Test Case Design Logic

### Test Coverage Overview

| API Endpoint | Positive | Negative | Edge Cases | Total  |
|--------------|----------|----------|------------|--------|
| **Create User** | 1 | 4 | 2          | 7      |
| **Get User** | 1 | 3 | 2          | 6      |
| **Update User** | 1 | 3 | 2          | 6      |
| **Delete User** | 1 | 3 | 1          | 6      |
| **Batch Query** | 3 | 3 | 3          | 9      |
| **TOTAL** | **7** | **16** | **10**     | **33** |

### Test Categories Explained

#### 1. Positive Tests (Normal Cases)
Tests the happy path with valid inputs and expected successful responses.

**Examples:**
- Create user with valid username, email, and password
- Get user details with existing user ID
- Update user email with valid format
- Delete existing user
- Query users with valid pagination parameters

#### 2. Negative Tests (Abnormal Cases)
Tests error handling and validation with invalid inputs.

**Examples:**
- Create user with duplicate username
- Create user with missing required fields
- Get non-existent user
- Update deleted user
- Delete already deleted user
- Invalid email formats
- Short passwords (< 6 characters)

#### 3. Edge Cases
Tests boundary conditions and unusual but valid scenarios.

**Examples:**
- Very long usernames (256 characters)
- Special characters in usernames (@#$%^&*())
- Unicode characters in keywords (测试用户)
- Zero and negative IDs
- Empty keywords
- Page numbers beyond total pages
- Extremely large page sizes (10000)
- Pagination consistency across pages

### Business Logic Tests

The framework goes beyond simple parameter validation:

- ✅ **Duplicate Detection**: Verify system prevents duplicate usernames
- ✅ **State Management**: Test operations on deleted resources
- ✅ **Data Consistency**: Verify updates are reflected in subsequent queries
- ✅ **Pagination Logic**: Ensure no duplicate records across pages
- ✅ **Search Functionality**: Validate keyword filtering works correctly

---


## 📚 API Documentation

### 1. Create User
**Endpoint:** `POST /api/v1/users`

**Request:**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "Test@123456"
}
```

**Success Response:**
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "testuser"
  },
  "msg": "success"
}
```

### 2. Get User Details
**Endpoint:** `GET /api/v1/users/{user_id}`

**Success Response:**
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "msg": "success"
}
```

### 3. Update User Email
**Endpoint:** `PUT /api/v1/users/{user_id}`

**Request:**
```json
{
  "email": "newemail@example.com"
}
```

**Success Response:**
```json
{
  "code": 200,
  "data": null,
  "msg": "success"
}
```

### 4. Delete User
**Endpoint:** `DELETE /api/v1/users/{user_id}`

**Success Response:**
```json
{
  "code": 200,
  "data": null,
  "msg": "success"
}
```

### 5. Batch Query Users
**Endpoint:** `GET /api/v1/users?page=1&size=10&keyword=test`

**Success Response:**
```json
{
  "code": 200,
  "data": {
    "total": 50,
    "list": [
      {
        "id": 1,
        "username": "testuser"
      }
    ]
  },
  "msg": "success"
}
```

---


## 📦 Dependencies

All dependencies are listed in `requirements.txt`:

```
requests==2.31.0          # HTTP library
pytest==7.4.3             # Testing framework
allure-pytest==2.13.2     # Allure reporting
pydantic==2.5.0           # Data validation
python-dotenv==1.0.0      # Environment management
```

