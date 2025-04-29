import requests
import re
import json
import os
import hashlib
from urllib.parse import urlparse
import urllib.parse

class JavaScriptAnalyzer:
    """
    Analyzes JavaScript files for known vulnerabilities, similar to retire.js
    """
    def __init__(self):
        # Load vulnerability database
        self.db_path = os.path.join(os.path.dirname(__file__), 'data', 'jsdb.json')
        self.ensure_db_exists()
        self.load_vulnerability_db()
        
        # Headers for requests
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def ensure_db_exists(self):
        """
        Ensure the vulnerability database exists, create if not
        """
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            # Create a basic database if it doesn't exist
            basic_db = {
                "jquery": {
                    "vulnerabilities": [
                        {
                            "below": "1.9.0",
                            "severity": "medium",
                            "identifiers": {
                                "CVE": ["CVE-2012-6708"]
                            },
                            "info": ["https://github.com/advisories/GHSA-gxr4-xjj5-5px2"]
                        },
                        {
                            "below": "3.5.0",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2019-11358"]
                            },
                            "info": ["https://github.com/advisories/GHSA-jpcq-cgw6-v4j6"]
                        }
                    ],
                    "extractors": {
                        "filename": [
                            "jquery-(\\d+)\\.(\\d+)\\.(\\d+)(\\.min)?\\.js"
                        ],
                        "filecontent": [
                            "/*! jQuery v(\\d+)\\.(\\d+)\\.(\\d+)",
                            "\\* jQuery JavaScript Library v(\\d+)\\.(\\d+)\\.(\\d+)"
                        ]
                    }
                },
                "bootstrap": {
                    "vulnerabilities": [
                        {
                            "below": "3.4.0",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2018-14040", "CVE-2018-14042"]
                            },
                            "info": ["https://github.com/advisories/GHSA-9v3m-8fp8-mj99"]
                        },
                        {
                            "below": "4.3.1",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2019-8331"]
                            },
                            "info": ["https://github.com/advisories/GHSA-9v3m-8fp8-mj99"]
                        }
                    ],
                    "extractors": {
                        "filename": [
                            "bootstrap-(\\d+)\\.(\\d+)\\.(\\d+)(\\.min)?\\.js"
                        ],
                        "filecontent": [
                            "\\* Bootstrap v(\\d+)\\.(\\d+)\\.(\\d+)",
                            "Bootstrap v(\\d+)\\.(\\d+)\\.(\\d+)"
                        ]
                    }
                },
                "angular": {
                    "vulnerabilities": [
                        {
                            "below": "1.6.9",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2018-1000006"]
                            },
                            "info": ["https://github.com/advisories/GHSA-prcx-m3jj-wh36"]
                        },
                        {
                            "below": "1.7.0",
                            "severity": "medium",
                            "identifiers": {
                                "CVE": ["CVE-2018-1000006"]
                            },
                            "info": ["https://github.com/advisories/GHSA-prcx-m3jj-wh36"]
                        }
                    ],
                    "extractors": {
                        "filename": [
                            "angular(?:-core)?-(\\d+)\\.(\\d+)\\.(\\d+)(\\.min)?\\.js"
                        ],
                        "filecontent": [
                            "* AngularJS v(\\d+)\\.(\\d+)\\.(\\d+)",
                            "angular(?:-core)?/?(\\d+)\\.(\\d+)\\.(\\d+)"
                        ]
                    }
                },
                "react": {
                    "vulnerabilities": [
                        {
                            "below": "16.3.0",
                            "severity": "medium",
                            "identifiers": {
                                "CVE": ["CVE-2018-6341"]
                            },
                            "info": ["https://github.com/advisories/GHSA-m7mg-mrm3-rcpf"]
                        }
                    ],
                    "extractors": {
                        "filename": [
                            "react-(\\d+)\\.(\\d+)\\.(\\d+)(\\.min)?\\.js"
                        ],
                        "filecontent": [
                            "React v(\\d+)\\.(\\d+)\\.(\\d+)"
                        ]
                    }
                },
                "lodash": {
                    "vulnerabilities": [
                        {
                            "below": "4.17.11",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2019-10744"]
                            },
                            "info": ["https://github.com/advisories/GHSA-jf85-cpcp-j695"]
                        },
                        {
                            "below": "4.17.15",
                            "severity": "high",
                            "identifiers": {
                                "CVE": ["CVE-2019-10744"]
                            },
                            "info": ["https://github.com/advisories/GHSA-jf85-cpcp-j695"]
                        }
                    ],
                    "extractors": {
                        "filename": [
                            "lodash(?:\\.min)?\\.(\\d+)\\.(\\d+)\\.(\\d+)\\.js"
                        ],
                        "filecontent": [
                            "lodash v(\\d+)\\.(\\d+)\\.(\\d+)"
                        ]
                    }
                }
            }
            
            with open(self.db_path, 'w') as f:
                json.dump(basic_db, f, indent=2)

    def load_vulnerability_db(self):
        """
        Load the vulnerability database
        """
        try:
            with open(self.db_path, 'r') as f:
                self.vuln_db = json.load(f)
        except Exception as e:
            print(f"Error loading vulnerability database: {e}")
            self.vuln_db = {}

    def analyze(self, js_urls, inline_scripts):
        """
        Analyze JavaScript files and inline scripts for vulnerabilities
        """
        result = {
            'vulnerabilities': 0,
            'vulnerable_libraries': [],
            'status': 'safe'
        }
        
        # Analyze external JavaScript files
        for url in js_urls:
            try:
                # Extract filename from URL
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                
                # Check if the filename matches any known patterns
                lib_info = self._check_filename(filename)
                
                if not lib_info:
                    # If no match by filename, download and check content
                    response = requests.get(url, headers=self.headers, timeout=10, verify=False)
                    content = response.text
                    lib_info = self._check_content(content)
                
                if lib_info:
                    result['vulnerabilities'] += len(lib_info['vulnerabilities'])
                    result['vulnerable_libraries'].append(lib_info)
            except Exception as e:
                print(f"Error analyzing JavaScript URL {url}: {e}")
        
        # Analyze inline scripts
        for script in inline_scripts:
            try:
                lib_info = self._check_content(script)
                if lib_info:
                    result['vulnerabilities'] += len(lib_info['vulnerabilities'])
                    result['vulnerable_libraries'].append(lib_info)
            except Exception as e:
                print(f"Error analyzing inline script: {e}")
        
        # Update status based on vulnerabilities
        if result['vulnerabilities'] > 0:
            # Check for high severity vulnerabilities
            has_high_severity = any(
                vuln.get('severity') == 'high' 
                for lib in result['vulnerable_libraries'] 
                for vuln in lib['vulnerabilities']
            )
            
            if has_high_severity:
                result['status'] = 'unsafe'
            else:
                result['status'] = 'warning'
        
        return result

    def _check_filename(self, filename):
        """
        Check if the filename matches any known vulnerable library patterns
        """
        for lib_name, lib_data in self.vuln_db.items():
            if 'extractors' in lib_data and 'filename' in lib_data['extractors']:
                for pattern in lib_data['extractors']['filename']:
                    match = re.search(pattern, filename)
                    if match:
                        version = self._extract_version(match)
                        return self._check_vulnerabilities(lib_name, version)
        
        return None

    def _check_content(self, content):
        """
        Check if the content contains any known vulnerable library patterns
        """
        for lib_name, lib_data in self.vuln_db.items():
            if 'extractors' in lib_data and 'filecontent' in lib_data['extractors']:
                for pattern in lib_data['extractors']['filecontent']:
                    match = re.search(pattern, content)
                    if match:
                        version = self._extract_version(match)
                        return self._check_vulnerabilities(lib_name, version)
        
        return None

    def _extract_version(self, match):
        """
        Extract version from regex match
        """
        if match.groups():
            # Assume the first 3 groups are major, minor, patch
            version_parts = []
            for i in range(1, min(4, len(match.groups()) + 1)):
                if match.group(i) and not match.group(i).startswith('.'):
                    version_parts.append(match.group(i))
            
            if len(version_parts) >= 3:
                return '.'.join(version_parts[:3])
        
        return None

    def _check_vulnerabilities(self, lib_name, version):
        """
        Check if the library version has known vulnerabilities
        """
        if not version or lib_name not in self.vuln_db:
            return None
        
        lib_data = self.vuln_db[lib_name]
        if 'vulnerabilities' not in lib_data:
            return None
        
        # Parse version
        try:
            major, minor, patch = map(int, version.split('.'))
        except:
            return None
        
        # Check for vulnerabilities
        vulnerabilities = []
        for vuln in lib_data['vulnerabilities']:
            if 'below' in vuln:
                below_version = vuln['below']
                below_major, below_minor, below_patch = map(int, below_version.split('.'))
                
                if (major < below_major) or \
                   (major == below_major and minor < below_minor) or \
                   (major == below_major and minor == below_minor and patch < below_patch):
                    vulnerabilities.append(vuln)
        
        if vulnerabilities:
            return {
                'library': lib_name,
                'version': version,
                'vulnerabilities': vulnerabilities
            }
        
        return None
