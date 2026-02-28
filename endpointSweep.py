#!/usr/bin/env python3
import requests
import os
import sys
import argparse

# Configuration
API_KEY = os.environ.get('key')
AUTH_TOKEN = os.environ.get('token')
PROXY = {'http': '127.0.0.1:8080', 'https': '127.0.0.1:8080'}

def make_request(method, path, base_url, proxy):
    """Make HTTP request and return path, status code, and body"""
    headers = {}
    
    # Add API key if present
    if API_KEY:
        headers['x-Api-Key'] = API_KEY
    
    # Add Authorization header if token is present
    if AUTH_TOKEN:
        headers['Authorization'] = f"Bearer {AUTH_TOKEN}"
    
    url = f"{base_url}{path}"
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            proxies=proxy,
            verify=False,  # equivalent to curl -k
            timeout=30
        )
        
        return {
            'path': path,
            'method': method,
            'status_code': response.status_code,
            'body': response.text
        }
    except requests.exceptions.RequestException as e:
        return {
            'path': path,
            'method': method,
            'status_code': 'ERROR',
            'body': str(e)
        }

def format_output(results, body_length):
    """Format results with color coding"""
    # ANSI color codes
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

    # Find max widths for columns
    max_path = max(len(r['path']) for r in results)
    max_method = max(len(r['method']) for r in results)

    # Print header
    print(f"{'METHOD':<{max_method}} | {'PATH':<{max_path}} | STATUS | RESPONSE")
    print(f"{'-' * max_method}-+-{'-' * max_path}-+--------+-{'-' * body_length}")

    # Print rows
    for r in results:
        status = str(r['status_code'])

        # Color code by status
        if status.startswith('2'):
            color = GREEN
        elif status.startswith('4') or status.startswith('5'):
            color = RED
        else:
            color = YELLOW

        # Collapse whitespace, then truncate with ellipsis if needed
        body = ' '.join(r['body'].split())
        if len(body) > body_length:
            body = body[:body_length - 3] + '...'
        print(f"{r['method']:<{max_method}} | {r['path']:<{max_path}} | {color}{status:^6}{RESET} | {body}")

def main():
    parser = argparse.ArgumentParser(
        description='Execute HTTP requests from a file and display results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s requests.txt --url https://api.example.com
  %(prog)s requests.txt --url https://api.example.com --methods GET POST
  %(prog)s requests.txt --url https://api.example.com --exclude DELETE POST
        '''
    )
    
    parser.add_argument('input_file', help='File containing METHOD /path lines')
    parser.add_argument('--url', '-u', required=True, help='Base URL for API (e.g., https://api.example.com)')
    parser.add_argument('--methods', '-m', nargs='+', 
                        help='Only execute these HTTP methods (e.g., --methods GET POST)')
    parser.add_argument('--exclude', '-e', nargs='+',
                        help='Exclude these HTTP methods (e.g., --exclude DELETE POST)')
    parser.add_argument('--no-proxy', action='store_true',
                        help='Send requests directly, bypassing the Burp proxy')
    parser.add_argument('--body-length', '-b', type=int, default=100, metavar='N',
                        help='Maximum characters to display from response body (default: 100)')
    
    args = parser.parse_args()
    
    # Validate that both --methods and --exclude aren't used together
    if args.methods and args.exclude:
        print("Error: Cannot use both --methods and --exclude")
        sys.exit(1)
    
    # Normalize method filters to uppercase
    allowed_methods = set(m.upper() for m in args.methods) if args.methods else None
    excluded_methods = set(m.upper() for m in args.exclude) if args.exclude else set()
    
    base_url = args.url.rstrip('/')  # Remove trailing slash if present
    proxy = None if args.no_proxy else PROXY
    
    # Suppress SSL warnings when using verify=False
    requests.packages.urllib3.disable_warnings()
    
    results = []
    skipped = []
    
    with open(args.input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse line: "GET /path" or just "/path" (defaults to GET)
            parts = line.split(None, 1)
            if len(parts) == 2:
                method, path = parts
            else:
                method, path = 'GET', parts[0]
            
            method = method.upper()
            
            # Check if method should be executed
            if allowed_methods and method not in allowed_methods:
                skipped.append((method, path, 'not in allowed methods'))
                continue
            
            if method in excluded_methods:
                skipped.append((method, path, 'excluded'))
                continue
            
            result = make_request(method, path, base_url, proxy)
            results.append(result)
    
    # Format and print all results
    if results:
        format_output(results, args.body_length)
    else:
        print("No requests executed.")
    
    # Show skipped requests if any
    if skipped:
        print(f"\n⚠ Skipped {len(skipped)} request(s):")
        for method, path, reason in skipped:
            print(f"  {method} {path} ({reason})")

if __name__ == '__main__':
    main()
