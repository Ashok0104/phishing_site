import requests
import json
import sys

def test_analyze_url(url):
    """
    Test the comprehensive URL analysis endpoint
    """
    print(f"\n=== Testing comprehensive analysis for {url} ===")
    try:
        response = requests.post(
            'http://localhost:5000/api/analyze',
            json={'url': url},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status', 'Unknown')}")
            print(f"Score: {result.get('score', 'N/A')}")
            
            # Print details
            if 'details' in result:
                print("\nDetails:")
                for key, value in result['details'].items():
                    if isinstance(value, dict) and 'value' in value:
                        print(f"  {key}: {value['value']} ({value.get('status', 'Unknown')})")
                    elif key == 'javascriptAnalysis':
                        print(f"  JavaScript Analysis: {value.get('vulnerabilities', 0)} vulnerabilities found")
                        if value.get('vulnerabilities', 0) > 0 and 'vulnerable_libraries' in value:
                            print("    Vulnerable libraries:")
                            for lib in value['vulnerable_libraries']:
                                print(f"      {lib['library']} v{lib['version']}")
                    else:
                        print(f"  {key}: {value}")
            
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

def test_quick_analyze_url(url):
    """
    Test the quick URL analysis endpoint
    """
    print(f"\n=== Testing quick analysis for {url} ===")
    try:
        response = requests.post(
            'http://localhost:5000/api/quick-analyze',
            json={'url': url},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"Status: {result.get('status', 'Unknown')}")
            
            # Print details
            if 'details' in result:
                print("\nDetails:")
                for key, value in result['details'].items():
                    if isinstance(value, dict) and 'value' in value:
                        print(f"  {key}: {value['value']} ({value.get('status', 'Unknown')})")
                    else:
                        print(f"  {key}: {value}")
            
            return True
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Exception: {e}")
        return False

if __name__ == "__main__":
    # Get URL from command line or use default
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.google.com"
    
    # Test both endpoints
    quick_result = test_quick_analyze_url(url)
    comprehensive_result = test_analyze_url(url)
    
    # Print summary
    print("\n=== Test Summary ===")
    print(f"Quick Analysis: {'PASSED' if quick_result else 'FAILED'}")
    print(f"Comprehensive Analysis: {'PASSED' if comprehensive_result else 'FAILED'}")
    
    # Exit with appropriate code
    sys.exit(0 if quick_result and comprehensive_result else 1)
