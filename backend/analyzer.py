import requests
import validators
import whois
import ssl
import socket
import datetime
import tldextract
import urllib.parse
from bs4 import BeautifulSoup
import re
import json
import os
from urllib.parse import urlparse
from .js_analyzer import JavaScriptAnalyzer

class URLAnalyzer:
    """
    Main class for analyzing URLs for phishing and vulnerabilities
    """
    def __init__(self):
        self.js_analyzer = JavaScriptAnalyzer()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Load suspicious keywords
        self.suspicious_keywords = [
            'login', 'signin', 'verify', 'verification', 'secure', 'account',
            'password', 'credential', 'confirm', 'update', 'banking', 'security',
            'authenticate', 'wallet', 'recover', 'unlock', 'authorize'
        ]
        
        # Common phishing targets
        self.common_targets = [
            'paypal', 'apple', 'microsoft', 'amazon', 'facebook', 'google',
            'bank', 'ebay', 'instagram', 'netflix', 'linkedin', 'twitter',
            'chase', 'wellsfargo', 'citi', 'bankofamerica', 'coinbase', 'binance'
        ]

    def analyze(self, url):
        """
        Perform a comprehensive analysis of the URL
        """
        # Validate URL format
        if not validators.url(url):
            return {
                'status': 'error',
                'message': 'Invalid URL format'
            }
        
        # Initialize result structure
        result = {
            'url': url,
            'status': 'safe',  # Default status
            'score': 0,
            'details': {}
        }
        
        try:
            # Domain analysis
            domain_info = self._analyze_domain(url)
            result['details'].update(domain_info)
            
            # SSL analysis
            ssl_info = self._analyze_ssl(url)
            result['details'].update(ssl_info)
            
            # Content analysis
            content_info = self._analyze_content(url)
            result['details'].update(content_info)
            
            # Calculate overall score and status
            result = self._calculate_score(result)
            
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f'Analysis error: {str(e)}'
        
        return result

    def quick_analyze(self, url):
        """
        Perform a quick analysis with fewer checks
        """
        # Validate URL format
        if not validators.url(url):
            return {
                'status': 'error',
                'message': 'Invalid URL format'
            }
        
        # Initialize result structure
        result = {
            'url': url,
            'status': 'safe',  # Default status
            'details': {}
        }
        
        try:
            # Domain analysis (basic)
            domain_info = self._analyze_domain(url, quick=True)
            result['details'].update(domain_info)
            
            # SSL analysis (basic)
            ssl_info = self._analyze_ssl(url, quick=True)
            result['details'].update(ssl_info)
            
            # Determine status based on quick checks
            if domain_info.get('domainAge', {}).get('value', 'Unknown') == 'Unknown' or \
               domain_info.get('domainAge', {}).get('value', 0) < 30:  # Less than 30 days
                result['status'] = 'warning'
            
            if ssl_info.get('sslStatus', {}).get('value', 'Invalid') == 'Invalid':
                result['status'] = 'warning'
                
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f'Analysis error: {str(e)}'
        
        return result

    def _analyze_domain(self, url, quick=False):
        """
        Analyze domain information
        """
        result = {}
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Extract domain parts
        ext = tldextract.extract(url)
        domain_name = f"{ext.domain}.{ext.suffix}"
        
        # Check domain age
        try:
            w = whois.whois(domain_name)
            creation_date = w.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
                
            if creation_date:
                domain_age_days = (datetime.datetime.now() - creation_date).days
                if domain_age_days < 30:
                    domain_age_status = 'suspicious'
                elif domain_age_days < 180:
                    domain_age_status = 'warning'
                else:
                    domain_age_status = 'safe'
                
                if domain_age_days < 365:
                    domain_age_text = f"{domain_age_days} days"
                else:
                    domain_age_years = domain_age_days / 365
                    domain_age_text = f"{domain_age_years:.1f} years"
                
                result['domainAge'] = {
                    'value': domain_age_text,
                    'raw_value': domain_age_days,
                    'status': domain_age_status
                }
            else:
                result['domainAge'] = {
                    'value': 'Unknown',
                    'status': 'warning'
                }
        except Exception:
            result['domainAge'] = {
                'value': 'Unknown',
                'status': 'warning'
            }
        
        # Check for suspicious domain name
        suspicious_domain = False
        for target in self.common_targets:
            if target in domain_name.lower() and ext.domain.lower() != target:
                suspicious_domain = True
                break
        
        result['suspiciousDomain'] = {
            'value': 'Yes' if suspicious_domain else 'No',
            'status': 'unsafe' if suspicious_domain else 'safe'
        }
        
        # Get IP address
        if not quick:
            try:
                ip_address = socket.gethostbyname(domain)
                result['ipAddress'] = {
                    'value': ip_address,
                    'status': 'info'
                }
            except:
                result['ipAddress'] = {
                    'value': 'Unknown',
                    'status': 'warning'
                }
        
        return result

    def _analyze_ssl(self, url, quick=False):
        """
        Analyze SSL certificate
        """
        result = {}
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Check if HTTPS is used
        is_https = parsed_url.scheme == 'https'
        result['isHttps'] = {
            'value': 'Yes' if is_https else 'No',
            'status': 'safe' if is_https else 'warning'
        }
        
        # If not HTTPS, no need to check certificate
        if not is_https:
            result['sslStatus'] = {
                'value': 'Not Used',
                'status': 'warning'
            }
            return result
        
        # Check SSL certificate
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate expiration
                    not_after = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.datetime.now()).days
                    
                    if days_until_expiry < 0:
                        ssl_status = 'Invalid (Expired)'
                        status_code = 'unsafe'
                    elif days_until_expiry < 30:
                        ssl_status = 'Valid (Expiring Soon)'
                        status_code = 'warning'
                    else:
                        ssl_status = 'Valid'
                        status_code = 'safe'
                    
                    result['sslStatus'] = {
                        'value': ssl_status,
                        'status': status_code
                    }
                    
                    if not quick:
                        # Get certificate issuer
                        issuer = dict(x[0] for x in cert['issuer'])
                        result['sslIssuer'] = {
                            'value': issuer.get('organizationName', 'Unknown'),
                            'status': 'info'
                        }
        except:
            result['sslStatus'] = {
                'value': 'Invalid',
                'status': 'unsafe'
            }
        
        return result

    def _analyze_content(self, url):
        """
        Analyze page content for suspicious elements
        """
        result = {}
        
        try:
            # Fetch the page content
            response = requests.get(url, headers=self.headers, timeout=10, verify=False)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            
            # Check for login forms
            forms = soup.find_all('form')
            login_form_count = 0
            password_field_count = 0
            
            for form in forms:
                # Check if it's a login form
                if any(keyword in str(form).lower() for keyword in ['login', 'signin', 'password']):
                    login_form_count += 1
                
                # Check for password fields
                password_fields = form.find_all('input', {'type': 'password'})
                password_field_count += len(password_fields)
            
            result['loginForms'] = {
                'value': login_form_count,
                'status': 'warning' if login_form_count > 0 else 'safe'
            }
            
            result['passwordFields'] = {
                'value': password_field_count,
                'status': 'warning' if password_field_count > 0 else 'safe'
            }
            
            # Check for suspicious keywords in content
            text_content = soup.get_text().lower()
            found_keywords = [keyword for keyword in self.suspicious_keywords if keyword in text_content]
            
            result['suspiciousKeywords'] = {
                'value': ', '.join(found_keywords) if found_keywords else 'None',
                'status': 'warning' if found_keywords else 'safe'
            }
            
            # Analyze JavaScript for vulnerabilities
            scripts = soup.find_all('script')
            js_urls = []
            
            # Extract inline scripts
            inline_scripts = []
            for script in scripts:
                if script.string:
                    inline_scripts.append(script.string)
                if script.get('src'):
                    js_urls.append(urllib.parse.urljoin(url, script.get('src')))
            
            # Analyze JavaScript
            js_analysis = self.js_analyzer.analyze(js_urls, inline_scripts)
            result['javascriptAnalysis'] = js_analysis
            
            # Check for iframes
            iframes = soup.find_all('iframe')
            result['iframeCount'] = {
                'value': len(iframes),
                'status': 'warning' if len(iframes) > 0 else 'safe'
            }
            
            # Check for redirects
            meta_refresh = soup.find('meta', {'http-equiv': re.compile(r'refresh', re.I)})
            js_redirects = len(re.findall(r'window\.location', content)) + len(re.findall(r'document\.location', content))
            
            result['redirects'] = {
                'value': 'Yes' if meta_refresh or js_redirects > 0 else 'No',
                'status': 'warning' if meta_refresh or js_redirects > 0 else 'safe'
            }
            
        except Exception as e:
            result['contentAnalysis'] = {
                'value': f'Error: {str(e)}',
                'status': 'error'
            }
        
        return result

    def _calculate_score(self, result):
        """
        Calculate the overall security score and determine status
        """
        # Define weights for different factors
        weights = {
            'domainAge': 15,
            'suspiciousDomain': 20,
            'isHttps': 10,
            'sslStatus': 15,
            'loginForms': 5,
            'passwordFields': 5,
            'suspiciousKeywords': 10,
            'javascriptAnalysis': 15,
            'iframeCount': 5,
            'redirects': 5
        }
        
        total_weight = 0
        weighted_score = 0
        
        # Calculate weighted score
        for key, weight in weights.items():
            if key in result['details']:
                total_weight += weight
                
                detail = result['details'][key]
                if isinstance(detail, dict) and 'status' in detail:
                    if detail['status'] == 'safe':
                        weighted_score += weight * 100
                    elif detail['status'] == 'warning':
                        weighted_score += weight * 50
                    elif detail['status'] == 'unsafe':
                        weighted_score += weight * 0
                    elif detail['status'] == 'info':
                        # Info doesn't affect score
                        total_weight -= weight
                elif key == 'javascriptAnalysis':
                    # Handle JavaScript analysis specially
                    if detail.get('vulnerabilities', 0) == 0:
                        weighted_score += weight * 100
                    else:
                        vuln_count = detail.get('vulnerabilities', 0)
                        if vuln_count <= 2:
                            weighted_score += weight * 50
                        else:
                            weighted_score += weight * 0
        
        # Calculate final score
        if total_weight > 0:
            final_score = int(weighted_score / total_weight)
        else:
            final_score = 50  # Default score if no weights applied
        
        result['score'] = final_score
        
        # Determine status based on score
        if final_score >= 80:
            result['status'] = 'safe'
        elif final_score >= 50:
            result['status'] = 'warning'
        else:
            result['status'] = 'unsafe'
        
        return result
