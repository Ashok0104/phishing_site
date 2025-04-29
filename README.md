# SafeBank Shield - Phishing Detection System

A comprehensive phishing detection system that analyzes URLs for potential threats, including JavaScript vulnerabilities similar to retire.js.

## Features

- Domain analysis (age, registration details)
- SSL certificate validation
- Content analysis for suspicious patterns
- JavaScript vulnerability detection (similar to retire.js)
- Reputation scoring based on multiple factors
- Quick analysis for basic checks
- Comprehensive analysis for detailed reports

## Backend Architecture

The backend is built with Python and Flask, providing a RESTful API for the frontend to consume. The main components are:

1. **URL Analyzer**: Analyzes URLs for phishing indicators
2. **JavaScript Analyzer**: Detects vulnerable JavaScript libraries (similar to retire.js)
3. **Vulnerability Database**: Contains information about known vulnerable JavaScript libraries

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/phishing_site.git
   cd phishing_site
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## API Endpoints

### 1. Analyze URL (Comprehensive)

**Endpoint**: `/api/analyze`
**Method**: POST
**Request Body**:
```json
{
  "url": "https://example.com"
}
```

**Response**:
```json
{
  "url": "https://example.com",
  "status": "safe", // or "unsafe" or "warning"
  "score": 85,
  "details": {
    "domainAge": {
      "value": "2 years",
      "status": "safe"
    },
    "sslStatus": {
      "value": "Valid",
      "status": "safe"
    },
    "ipAddress": {
      "value": "192.168.1.1",
      "status": "info"
    },
    "suspiciousKeywords": {
      "value": "None",
      "status": "safe"
    },
    "javascriptAnalysis": {
      "vulnerabilities": 0,
      "vulnerable_libraries": [],
      "status": "safe"
    }
    // Additional details...
  }
}
```

### 2. Quick Analyze URL

**Endpoint**: `/api/quick-analyze`
**Method**: POST
**Request Body**:
```json
{
  "url": "https://example.com"
}
```

**Response**:
```json
{
  "url": "https://example.com",
  "status": "safe", // or "unsafe" or "warning"
  "details": {
    "domainAge": {
      "value": "2 years",
      "status": "safe"
    },
    "sslStatus": {
      "value": "Valid",
      "status": "safe"
    }
  }
}
```

## JavaScript Vulnerability Detection

The system detects vulnerable JavaScript libraries by:

1. Extracting JavaScript files from the target website
2. Analyzing file names and content to identify libraries and versions
3. Comparing detected versions against a database of known vulnerabilities
4. Reporting any matches as potential security risks

The vulnerability database is stored in `backend/data/jsdb.json` and includes information about common libraries like jQuery, Bootstrap, Angular, React, and more.