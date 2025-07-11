import os, cssutils, subprocess
import time
import json
import hashlib
from pathlib import Path
from datetime import datetime
import re
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv

load_dotenv()

class MonitorAgent:
    def __init__(self, watch_folder="Hotel-demo"):
        self.watch_folder = Path(watch_folder)
        self.file_hashes = {}
        self.error_log = []
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_Url_env = os.getenv('GEMINI_URL')
        self.gemini_url = f"{self.gemini_Url_env}={self.gemini_api_key}"
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        print(f"Monitor Agent initialized - Watching: {self.watch_folder}")
        print("=" * 60)
    
    def has_pending_errors(self):
        try:
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    error_log = json.load(f)
                return any(error.get('status') == 'detected' for error in error_log)
            return False
        except:
            return False
    
    def calculate_file_hash(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return hashlib.md5(content.encode()).hexdigest()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    
    
    def validate_html(self, file_path):
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()

            for i, line in enumerate(lines, 1):
                if re.search(r'<[^>]*$', line) and not re.search(r'/>$', line):
                    errors.append(f"Line {i}: Incomplete tag (likely missing '>') -> {line.strip()}")

                for tag in ['link', 'meta', 'img', 'input', 'br', 'hr', 'source']:
                    if re.search(fr'<{tag}[^>]*$', line, re.IGNORECASE):
                        errors.append(f"Line {i}: Possibly malformed <{tag}> tag -> {line.strip()}")

                if re.search(r'<a(\s|>)', line):
                    match = re.search(r'<a[^>]*href\s*=\s*["\']([^"\']*)["\']', line)
                    if match:
                        href = match.group(1).strip()
                        if not href:
                            errors.append(f"Line {i}: Empty href in <a> tag -> {line.strip()}")
                    else:
                        errors.append(f"Line {i}: Missing href attribute in <a> tag -> {line.strip()}")


                if '<img' in line:
                    if not re.search(r'alt\s*=\s*["\'].*?["\']', line):
                        errors.append(f"Line {i}: Missing alt attribute in <img> tag -> {line.strip()}")

            soup = BeautifulSoup(content, 'html.parser')

            if not soup.find('html'):
                errors.append("Missing <html> tag")
            if not soup.find('head'):
                errors.append("Missing <head> tag")
            if not soup.find('body'):
                errors.append("Missing <body> tag")
            if not soup.find('title'):
                errors.append("Missing <title> tag in head")

            open_tags = re.findall(r'<([a-zA-Z][^/> \t\n]*)[^>]*?>', content)
            close_tags = re.findall(r'</([a-zA-Z][^>]*)>', content)

            self_closing = {'link', 'img', 'br', 'hr', 'input', 'meta', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}

            for tag in open_tags:
                tag_lower = tag.lower()
                if tag_lower not in self_closing and tag_lower not in [t.lower() for t in close_tags]:
                    errors.append(f"Unclosed tag: <{tag}>")

        except Exception as e:
            errors.append(f"HTML parsing error: {str(e)}")

        return errors

   
    def validate_css(self, file_path):
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            open_braces = content.count('{')
            close_braces = content.count('}')
            if open_braces != close_braces:
                errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")
            
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and ':' in line and not line.endswith((';', '{', '}')) and not line.startswith(('/*', '*', '@')):
                    errors.append(f"Missing semicolon on line {i}: {line}")
            
        except Exception as e:
            errors.append(f"CSS parsing error: {str(e)}")

        return errors
    
    
    def validate_javascript(self, file_path):
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            open_braces = content.count('{')
            close_braces = content.count('}')
            if open_braces != close_braces:
                errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")

            open_parens = content.count('(')
            close_parens = content.count(')')
            if open_parens != close_parens:
                errors.append(f"Mismatched parentheses: {open_parens} opening, {close_parens} closing")

            if 'console.log' in content:
                errors.append("Found console.log statements (should be removed in production)")

        except Exception as e:
            errors.append(f"JavaScript parsing error: {str(e)}")

        return errors
    
    def ai_analyze_error(self, file_path, errors):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            prompt = f"""
            Analyze the following code file and the detected errors.

            File: {file_path}
            Detected Errors: {errors}

            Code Content:
            {file_content}

            Please provide detail anlysis of the error in list.
            

            Keep the response concise but informative.
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 32,
                    "topP": 1,
                    "maxOutputTokens": 1000
                }
            }
            
            response = requests.post(self.gemini_url, json=payload)
            
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            return "AI analysis unavailable"
            
        except Exception as e:
            return f"AI analysis error: {str(e)}"
    
    def scan_files(self):
        if not self.watch_folder.exists():
            print(f"Watch folder '{self.watch_folder}' not found!")
            return
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        changes_detected = False
        
        for file_path in self.watch_folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.html', '.css', '.js']:
                current_hash = self.calculate_file_hash(file_path)
                file_key = str(file_path)
                
                if file_key not in self.file_hashes or self.file_hashes[file_key] != current_hash:
                    changes_detected = True
                    self.file_hashes[file_key] = current_hash
                    
                    print(f"\nCHANGE DETECTED: {file_path}")
                    print(f"Time: {current_time}")
                    
                    errors = []
                    if file_path.suffix.lower() == '.html':
                        errors = self.validate_html(file_path)
                    elif file_path.suffix.lower() == '.css':
                        errors = self.validate_css(file_path)
                    elif file_path.suffix.lower() == '.js':
                        errors = self.validate_javascript(file_path)
                    
                    if errors:
                        print(f"ERRORS FOUND in {file_path}:")
                        for error in errors:
                            print(f"   • {error}")
                        
                        print("\nAI Analysis:")
                        time.sleep(10)
                        ai_analysis = self.ai_analyze_error(file_path, errors)
                        time.sleep(5)

                        print(f" {ai_analysis}")
                        
                        error_entry = {
                            "timestamp": current_time,
                            "file": str(file_path),
                            "errors": errors,
                            "ai_analysis": ai_analysis,
                            "status": "detected"
                        }
                        self.error_log.append(error_entry)
                        
                        self.save_error_log()
                        
                        print(f"\nError logged for Solution Agent processing")
                        
                    else:
                        if hasattr(self, 'error_log') and self.error_log:
                            for error_entry in self.error_log:
                                if error_entry['file'] == str(file_path) and error_entry['status'] == 'detected':
                                    error_entry['status'] = 'resolved'
                            self.save_error_log()
                        
                        print(f"No errors found in {file_path}")
        
        if not changes_detected and not self.has_pending_errors():
            print(f"🔍 [{current_time}] No changes detected - System monitoring...")

    def save_error_log(self):
        try:
            existing_errors = []
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    existing_errors = json.load(f)

            # Merge old + new, without duplicating the same timestamp+file
            combined = existing_errors + [
                e for e in self.error_log
                if not any(e['timestamp'] == old['timestamp'] and e['file'] == old['file'] for old in existing_errors)
            ]

            with open('error_log.json', 'w') as f:
                json.dump(combined, f, indent=2)

            # Also update self.error_log in memory
            self.error_log = combined

        except Exception as e:
            print(f"Error saving log: {e}")

    
    def load_existing_hashes(self):
        print("Loading existing file states...")
        for file_path in self.watch_folder.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in ['.html', '.css', '.js']:
                self.file_hashes[str(file_path)] = self.calculate_file_hash(file_path)
                print(f"   • {file_path}")
    
    def run(self):
        print("Starting continuous monitoring...")
        print("Supported file types: HTML, CSS, JavaScript")
        print("Press Ctrl+C to stop monitoring\n")
        
        self.load_existing_hashes()
        
        try:
            while True:
                self.scan_files()
                time.sleep(2) 
                
        except KeyboardInterrupt:
            print("\n\nonitoring stopped by user")
            print("Session Summary:")
            print(f"   • Total errors detected: {len(self.error_log)}")
            print(f"   • Files monitored: {len(self.file_hashes)}")
            print("Error log saved to 'error_log.json'")

if __name__ == "__main__":
    try:
        monitor = MonitorAgent()
        monitor.run()
    except Exception as e:
        print(f"Monitor Agent failed to start: {e}")
        print("Make sure you have GEMINI_API_KEY in your .env file")