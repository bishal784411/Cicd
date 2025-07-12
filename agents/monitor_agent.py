# import os
# import cssutils
# import subprocess
# import time
# import json
# import hashlib
# from pathlib import Path
# from datetime import datetime
# import re
# from bs4 import BeautifulSoup
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# class MonitorAgent:
#     def __init__(self, watch_folder="Hotel-demo"):
#         self.watch_folder = Path(watch_folder)
#         self.file_hashes = {}
#         self.error_log = []
#         self.gemini_api_key = os.getenv('GEMINI_API_KEY')
#         self.gemini_Url_env = os.getenv('GEMINI_URL')
#         self.gemini_url = f"{self.gemini_Url_env}={self.gemini_api_key}"

#         if not self.gemini_api_key:
#             raise ValueError("GEMINI_API_KEY not found in environment variables")

#         print(f"Monitor Agent initialized - Watching: {self.watch_folder}")
#         print("=" * 60)

#     def has_pending_errors(self):
#         try:
#             if os.path.exists('error_log.json'):
#                 with open('error_log.json', 'r') as f:
#                     error_log = json.load(f)
#                 return any(error.get('status') == 'detected' for error in error_log)
#             return False
#         except:
#             return False

#     def calculate_file_hash(self, file_path):
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 return hashlib.md5(content.encode()).hexdigest()
#         except Exception as e:
#             print(f"Error reading file {file_path}: {e}")
#             return None

#     def validate_html(self, file_path):
#         errors = []

#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 lines = content.splitlines()

#             for i, line in enumerate(lines, 1):
#                 if re.search(r'<[^>]*$', line) and not re.search(r'/>$', line):
#                     errors.append(f"Line {i}: Incomplete tag (likely missing '>') -> {line.strip()}")

#                 for tag in ['link', 'meta', 'img', 'input', 'br', 'hr', 'source']:
#                     if re.search(fr'<{tag}[^>]*$', line, re.IGNORECASE):
#                         errors.append(f"Line {i}: Possibly malformed <{tag}> tag -> {line.strip()}")

#                 if re.search(r'<a(\s|>)', line):
#                     match = re.search(r'<a[^>]*href\s*=\s*["\']([^"\']*)["\']', line)
#                     if match:
#                         href = match.group(1).strip()
#                         if not href:
#                             errors.append(f"Line {i}: Empty href in <a> tag -> {line.strip()}")
#                     else:
#                         errors.append(f"Line {i}: Missing href attribute in <a> tag -> {line.strip()}")

#                 if '<img' in line:
#                     if not re.search(r'alt\s*=\s*["\'].*?["\']', line):
#                         errors.append(f"Line {i}: Missing alt attribute in <img> tag -> {line.strip()}")

#             soup = BeautifulSoup(content, 'html.parser')

#             if not soup.find('html'):
#                 errors.append("Missing <html> tag")
#             if not soup.find('head'):
#                 errors.append("Missing <head> tag")
#             if not soup.find('body'):
#                 errors.append("Missing <body> tag")
#             if not soup.find('title'):
#                 errors.append("Missing <title> tag in head")

#             open_tags = re.findall(r'<([a-zA-Z][^/> \t\n]*)[^>]*?>', content)
#             close_tags = re.findall(r'</([a-zA-Z][^>]*)>', content)

#             self_closing = {'link', 'img', 'br', 'hr', 'input', 'meta', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr'}

#             for tag in open_tags:
#                 tag_lower = tag.lower()
#                 if tag_lower not in self_closing and tag_lower not in [t.lower() for t in close_tags]:
#                     errors.append(f"Unclosed tag: <{tag}>")

#         except Exception as e:
#             errors.append(f"HTML parsing error: {str(e)}")

#         return errors

#     def validate_css(self, file_path):
#         errors = []
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()

#             # Basic syntax check
#             open_braces = content.count('{')
#             close_braces = content.count('}')
#             if open_braces != close_braces:
#                 errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")

#             lines = content.split('\n')
#             for i, line in enumerate(lines, 1):
#                 line = line.strip()
#                 if line and ':' in line and not line.endswith((';', '{', '}')) and not line.startswith(('/*', '*', '@')):
#                     errors.append(f"Missing semicolon on line {i}: {line}")

#             # --- Extract CSS custom properties used and defined ---
#             used_vars = set(re.findall(r'var\(\s*(--[\w-]+)', content))
#             defined_vars = set()

#             # Find defined variables inside :root only
#             root_match = re.search(r':root\s*{([^}]*)}', content, re.DOTALL)
#             if root_match:
#                 root_block = root_match.group(1)
#                 defined_vars = set(re.findall(r'(--[\w-]+)\s*:', root_block))

#             # Compare and find missing ones
#             undefined_vars = used_vars - defined_vars
#             for var in undefined_vars:
#                 errors.append(f"CSS variable {var} used but not defined in :root")

#         except Exception as e:
#             errors.append(f"CSS parsing error: {str(e)}")

#         return errors

#     def validate_javascript(self, file_path):
#         errors = []
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
#             open_braces = content.count('{')
#             close_braces = content.count('}')
#             if open_braces != close_braces:
#                 errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")

#             open_parens = content.count('(')
#             close_parens = content.count(')')
#             if open_parens != close_parens:
#                 errors.append(f"Mismatched parentheses: {open_parens} opening, {close_parens} closing")

#             if 'console.log' in content:
#                 errors.append("Found console.log statements (should be removed in production)")

#         except Exception as e:
#             errors.append(f"JavaScript parsing error: {str(e)}")

#         return errors

#     def ai_analyze_error(self, file_path, errors):
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 file_content = f.read()

#             prompt = f"""
# You are an AI code reviewer. Analyze the following file and detected errors.

# File: {file_path}
# Errors: {errors}

# Code:
# {file_content}

# Please respond ONLY in this exact format:
# ---
# Error:
# [One-line short description of the error if the error is simple, but provide a concise explanation if the error is more complex.]

# Analysis:
# [Brief, clear explanation tailored to error complexity]

# Correction:
# [One or two sentence explanation of the fix, followed by fix or corrected code snippet, no repetition of error or analysis]
# ---
# """


#             payload = {
#                 "contents": [{"parts": [{"text": prompt}]}],
#                 "generationConfig": {
#                     "temperature": 0.1,
#                     "topK": 32,
#                     "topP": 1,
#                     "maxOutputTokens": 1000
#                 }
#             }

#             response = requests.post(self.gemini_url, json=payload)
#             if response.status_code == 200:
#                 result = response.json()
#                 if 'candidates' in result and len(result['candidates']) > 0:
#                     return result['candidates'][0]['content']['parts'][0]['text']

#             return "AI analysis unavailable"
#         except Exception as e:
#             return f"AI analysis error: {str(e)}"

#     def scan_files(self):
#         if not self.watch_folder.exists():
#             print(f"Watch folder '{self.watch_folder}' not found!")
#             return

#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         changes_detected = False

#         for file_path in self.watch_folder.rglob('*'):
#             if file_path.is_file() and file_path.suffix.lower() in ['.html', '.css', '.js']:
#                 current_hash = self.calculate_file_hash(file_path)
#                 file_key = str(file_path)

#                 if file_key not in self.file_hashes or self.file_hashes[file_key] != current_hash:
#                     changes_detected = True
#                     self.file_hashes[file_key] = current_hash

#                     print(f"\nCHANGE DETECTED: {file_path}")
#                     print(f"Time: {current_time}")

#                     errors = []
#                     if file_path.suffix.lower() == '.html':
#                         errors = self.validate_html(file_path)
#                     elif file_path.suffix.lower() == '.css':
#                         errors = self.validate_css(file_path)
#                     elif file_path.suffix.lower() == '.js':
#                         errors = self.validate_javascript(file_path)

#                     if errors:
#                         print(f"ERRORS FOUND in {file_path}:")
#                         for error in errors:
#                             print(f"   • {error}")

#                         print("\nAI Analysis:")
#                         time.sleep(10)
#                         ai_analysis_raw = self.ai_analyze_error(file_path, errors)
#                         time.sleep(5)

#                         # Extract structured fields from AI analysis
#                         parsed_analysis, parsed_correction = "", ""
#                         match = re.search(r"Analysis:\s*(.*?)\n+Correction:\s*(.*)", ai_analysis_raw, re.DOTALL)
#                         if match:
#                             parsed_analysis = match.group(1).strip()
#                             parsed_correction = match.group(2).strip()

#                         # Metadata
#                         error_type = "SyntaxError"  # placeholder, refine as needed
#                         severity = "high" if "unclosed" in ' '.join(errors).lower() else "medium"
#                         pipeline_stage = "monitoring"
#                         commit_hash = "not pushed"
#                         branch = "main"

#                         error_entry = {
#                             "timestamp": current_time,
#                             "last_checked": current_time,
#                             "file": str(file_path),
#                             "errors": errors,
#                             "error_type": error_type,
#                             "severity": severity,
#                             "pipeline_stage": pipeline_stage,
#                             "commit_hash": commit_hash,
#                             "branch": branch,
#                             "ai_analysis": parsed_analysis,
#                             "fix_solution": parsed_correction,
#                             "status": "detected"
#                         }

#                         print(f" {parsed_analysis}\n\nSuggested Fix:\n{parsed_correction}")
#                         self.error_log.append(error_entry)
#                         self.save_error_log()

#                         print(f"\nError logged for Solution Agent processing")

#                     else:
#                         if hasattr(self, 'error_log') and self.error_log:
#                             for error_entry in self.error_log:
#                                 if error_entry['file'] == str(file_path) and error_entry['status'] == 'detected':
#                                     error_entry['status'] = 'resolved'
#                                     error_entry['last_checked'] = current_time
#                             self.save_error_log()

#                         print(f"No errors found in {file_path}")

#         if not changes_detected and not self.has_pending_errors():
#             print(f"🔍 [{current_time}] No changes detected - System monitoring...")

#     def save_error_log(self):
#         try:
#             existing_errors = []
#             if os.path.exists('error_log.json'):
#                 with open('error_log.json', 'r') as f:
#                     existing_errors = json.load(f)

#             # Merge old + new, without duplicating same timestamp+file
#             combined = existing_errors + [
#                 e for e in self.error_log
#                 if not any(e['timestamp'] == old['timestamp'] and e['file'] == old['file'] for old in existing_errors)
#             ]

#             with open('error_log.json', 'w') as f:
#                 json.dump(combined, f, indent=2)

#             # Update in-memory log
#             self.error_log = combined

#         except Exception as e:
#             print(f"Error saving log: {e}")

#     def load_existing_hashes(self):
#         print("Loading existing file states...")
#         for file_path in self.watch_folder.rglob('*'):
#             if file_path.is_file() and file_path.suffix.lower() in ['.html', '.css', '.js']:
#                 self.file_hashes[str(file_path)] = self.calculate_file_hash(file_path)
#                 print(f"   • {file_path}")

#     def run(self):
#         print("Starting continuous monitoring...")
#         print("Supported file types: HTML, CSS, JavaScript")
#         print("Press Ctrl+C to stop monitoring\n")

#         self.load_existing_hashes()

#         try:
#             while True:
#                 self.scan_files()
#                 time.sleep(2)

#         except KeyboardInterrupt:
#             print("\n\nMonitoring stopped by user")
#             print("Session Summary:")
#             print(f"   • Total errors detected: {len(self.error_log)}")
#             print(f"   • Files monitored: {len(self.file_hashes)}")
#             print("Error log saved to 'error_log.json'")


# if __name__ == "__main__":
#     try:
#         monitor = MonitorAgent()
#         monitor.run()
#     except Exception as e:
#         print(f"Monitor Agent failed to start: {e}")
#         print("Make sure you have GEMINI_API_KEY in your .env file")


import os
import cssutils
import subprocess
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
                    if match and not match.group(1).strip():
                        errors.append(f"Line {i}: Empty href in <a> tag -> {line.strip()}")
                    elif not match:
                        errors.append(f"Line {i}: Missing href attribute in <a> tag -> {line.strip()}")
                if '<img' in line and not re.search(r'alt\s*=\s*["\'].*?["\']', line):
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

            used_vars = set(re.findall(r'var\(\s*(--[\w-]+)', content))
            defined_vars = set()
            root_match = re.search(r':root\s*{([^}]*)}', content, re.DOTALL)
            if root_match:
                root_block = root_match.group(1)
                defined_vars = set(re.findall(r'(--[\w-]+)\s*:', root_block))

            undefined_vars = used_vars - defined_vars
            for var in undefined_vars:
                errors.append(f"CSS variable {var} used but not defined in :root")

        except Exception as e:
            errors.append(f"CSS parsing error: {str(e)}")

        return errors

    def validate_javascript(self, file_path):
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if content.count('{') != content.count('}'):
                errors.append("Mismatched braces in JavaScript")
            if content.count('(') != content.count(')'):
                errors.append("Mismatched parentheses in JavaScript")
            if 'console.log' in content:
                errors.append("Found console.log statements (should be removed in production)")
        except Exception as e:
            errors.append(f"JavaScript parsing error: {str(e)}")
        return errors

    def ai_analyze_error(self, file_path, errors):
        results = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

            for error in errors:
                prompt = f"""
You are an AI code reviewer. Analyze the following file and the specific error below.

File: {file_path}
Error: {error}

Code:
{file_content}

Please respond ONLY in this exact format:
---

Error:
[One-line short description of the error if the error is simple, but provide a concise explanation if the error is more complex.]

Analysis:
[Brief, clear explanation tailored to error complexity]

Correction:
[One or two sentence explanation of the fix, followed by fix or corrected code snippet, no repetition of error or analysis]

---
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
                        text = result['candidates'][0]['content']['parts'][0]['text']
                        match = re.search(r"Analysis:\s*(.*?)\n+Correction:\s*(.*)", text, re.DOTALL)
                        if match:
                            results.append({
                                "error": error,
                                "analysis": match.group(1).strip(),
                                "correction": match.group(2).strip()
                            })
                else:
                    results.append({
                        "error": error,
                        "analysis": "AI analysis failed to respond.",
                        "correction": "N/A"
                    })

                time.sleep(5)  # delay to avoid rate limit

        except Exception as e:
            results.append({
                "error": "General Error",
                "analysis": f"AI analysis error: {str(e)}",
                "correction": "N/A"
            })

        return results

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
                        for err in errors:
                            print(f"   • {err}")

                        ai_results = self.ai_analyze_error(file_path, errors)
                        ai_analysis_list = []
                        fix_solution_list = []

                        print("\nAI Analyses and Suggested Fixes:")
                        for i, item in enumerate(ai_results, 1):
                            ai_analysis_list.append({
                                "analysis": item["analysis"]
                            })
                            fix_solution_list.append({
                                "correction": item["correction"]
                            })
                            print(f"\nError {i}: {item['error']}")
                            print(f"  Analysis: {item['analysis']}")
                            print(f"  Correction: {item['correction']}")

                        error_entry = {
                            "timestamp": current_time,
                            "last_checked": current_time,
                            "file": str(file_path),
                            "errors": errors,
                            "error_type": "SyntaxError",
                            "severity": "high" if "unclosed" in ' '.join(errors).lower() else "medium",
                            "pipeline_stage": "monitoring",
                            "commit_hash": "not pushed",
                            "branch": "main",
                            "ai_analysis": ai_analysis_list,
                            "fix_solution": fix_solution_list,
                            "status": "detected"
                        }

                        self.error_log.append(error_entry)
                        self.save_error_log()
                        print("\nError logged for Solution Agent processing")
                    else:
                        for error_entry in self.error_log:
                            if error_entry['file'] == str(file_path) and error_entry['status'] == 'detected':
                                error_entry['status'] = 'resolved'
                                error_entry['last_checked'] = current_time
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

            combined = existing_errors + [
                e for e in self.error_log
                if not any(e['timestamp'] == old['timestamp'] and e['file'] == old['file'] for old in existing_errors)
            ]

            with open('error_log.json', 'w') as f:
                json.dump(combined, f, indent=2)

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
            print("\n\nMonitoring stopped by user")
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
