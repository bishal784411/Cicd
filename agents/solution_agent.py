
# import os
# import time
# import json
# import requests
# from datetime import datetime
# from pathlib import Path
# from dotenv import load_dotenv
# import difflib

# # Load environment variables
# load_dotenv()

# class SolutionAgent:
#     def __init__(self):
#         self.gemini_api_key = os.getenv('GEMINI_API_KEY')
#         self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}"
#         self.processed_errors = set()
        
#         if not self.gemini_api_key:
#             raise ValueError("GEMINI_API_KEY not found in environment variables")
        
#         print("🔧 Solution Agent initialized")
#         print("🤖 AI Model: Gemini 2.0 Flash")
#         print("=" * 60)
    
#     def load_error_log(self):
#         """Load error log from Monitor Agent"""
#         try:
#             if os.path.exists('error_log.json'):
#                 with open('error_log.json', 'r') as f:
#                     data = json.load(f)
#                     if isinstance(data, dict):
#                         return [data]  # wrap single entry in list
#                     return data
#             return []
#         except Exception as e:
#             print(f"❌ Error loading log: {e}")
#             return []


#     def generate_solution(self, file_path, file_content, errors):
#         """Generate solution using Gemini AI"""
#         try:
#             file_extension = Path(file_path).suffix.lower()
            
#             # Determine file type for context
#             if file_extension == '.html':
#                 file_type = "HTML"
#                 context = "This is an HTML file for a hotel booking system. Focus on proper HTML structure, accessibility, and semantic markup."
#             elif file_extension == '.css':
#                 file_type = "CSS"
#                 context = "This is a CSS file for styling a hotel booking system. Focus on proper CSS syntax, responsive design, and modern styling practices."
#             elif file_extension == '.js':
#                 file_type = "JavaScript"
#                 context = "This is a JavaScript file for a hotel booking system. Focus on proper syntax, error handling, and modern JavaScript practices."
#             else:
#                 file_type = "Code"
#                 context = "This is a code file that needs to be fixed."
            
#             prompt = f"""
#             You are an expert {file_type} HTML, CSS and Javascript developer working on a hotel booking system. 
            
#             Context: {context}
            
#             Original Code:
#             {file_content}
            
#             Detected Issues:
#             {errors}
            
            
#             Please ONLY provide:
#             1. The COMPLETE corrected file content
#             2. ONLY FIX the listed issues — do NOT reformat or make stylistic changes
#             3. DO NOT add unrelated enhancements
#             4. DO NOT explain anything — only the result


#             Format your response as:
#             CORRECTED_CODE:
#             [Complete corrected code here]

#             RECOMMENDATIONS:
#             [Optional brief improvements to consider — outside scope of this fix]
#             """
            
#             payload = {
#                 "contents": [{"parts": [{"text": prompt}]}],
#                 "generationConfig": {
#                     "temperature": 0.2,
#                     "topK": 40,
#                     "topP": 0.95,
#                     "maxOutputTokens": 4000
#                 }
#             }
            
#             response = requests.post(self.gemini_url, json=payload)
            
#             if response.status_code == 200:
#                 result = response.json()
#                 if 'candidates' in result and len(result['candidates']) > 0:
#                     return result['candidates'][0]['content']['parts'][0]['text']
            
#             return "❌ Failed to generate solution"
            
#         except Exception as e:
#             return f"❌ Solution generation error: {str(e)}"
    
#     def parse_solution(self, solution_text):
#         """Parse the AI solution into components"""
#         try:
#             import re
#             corrected_code = ""
#             explanation = ""
#             recommendations = ""

#             lines = solution_text.split('\n')
#             current_section = None

#             for line in lines:
#                 if line.strip().startswith('CORRECTED_CODE:'):
#                     current_section = 'code'
#                     continue
#                 elif line.strip().startswith('EXPLANATION:'):
#                     current_section = 'explanation'
#                     continue
#                 elif line.strip().startswith('RECOMMENDATIONS:'):
#                     current_section = 'recommendations'
#                     continue

#                 if current_section == 'code':
#                     corrected_code += line + '\n'
#                 elif current_section == 'explanation':
#                     explanation += line + '\n'
#                 elif current_section == 'recommendations':
#                     recommendations += line + '\n'

#             corrected_code = re.sub(r'^```[\w]*\n', '', corrected_code)
#             corrected_code = re.sub(r'\n?```[\s]*$', '', corrected_code)
#             corrected_code = corrected_code.strip()
            
#             return {
#                 'corrected_code': corrected_code,
#                 'explanation': explanation.strip(),
#                 'recommendations': recommendations.strip()
#             }

#         except Exception as e:
#             return {
#                 'corrected_code': solution_text,
#                 'explanation': f"Parse error: {str(e)}",
#                 'recommendations': ""
#             }

#     def generate_diff(self, original_code, corrected_code):
#         """Generate detailed diff between original and corrected code"""
#         try:
#             original_lines = original_code.splitlines(keepends=True)
#             corrected_lines = corrected_code.splitlines(keepends=True)
            
#             # Generate unified diff
#             diff = list(difflib.unified_diff(
#                 original_lines,
#                 corrected_lines,
#                 fromfile='original',
#                 tofile='corrected',
#                 lineterm=''
#             ))
            
#             # Parse diff to extract changes
#             changes = {
#                 'added_lines': [],
#                 'removed_lines': [],
#                 'modified_lines': [],
#                 'line_changes': []
#             }
            
#             current_line_num = 0
            
#             for line in diff:
#                 if line.startswith('@@'):
#                     # Extract line numbers from diff header
#                     import re
#                     match = re.search(r'-(\d+),?\d* \+(\d+),?\d*', line)
#                     if match:
#                         current_line_num = int(match.group(2))
#                 elif line.startswith('+') and not line.startswith('+++'):
#                     changes['added_lines'].append({
#                         'line_num': current_line_num,
#                         'content': line[1:].rstrip()
#                     })
#                     current_line_num += 1
#                 elif line.startswith('-') and not line.startswith('---'):
#                     changes['removed_lines'].append({
#                         'line_num': current_line_num,
#                         'content': line[1:].rstrip()
#                     })
#                 elif line.startswith(' '):
#                     current_line_num += 1
            
#             # Generate summary
#             changes['summary'] = {
#                 'total_lines_added': len(changes['added_lines']),
#                 'total_lines_removed': len(changes['removed_lines']),
#                 'diff_text': ''.join(diff) if diff else 'No changes detected'
#             }
            
#             return changes
            
#         except Exception as e:
#             return {
#                 'error': f"Diff generation failed: {str(e)}",
#                 'summary': {'total_lines_added': 0, 'total_lines_removed': 0, 'diff_text': ''}
#             }

#     def display_changes(self, changes):
#         """Display changes in a readable format"""
#         print("\n" + "="*50)
#         print("🔍 CODE CHANGES DETECTED")
#         print("="*50)
        
#         if 'error' in changes:
#             print(f"❌ {changes['error']}")
#             return
        
#         summary = changes['summary']
#         print(f"📊 Summary: +{summary['total_lines_added']} lines added, -{summary['total_lines_removed']} lines removed")
        
#         if changes['added_lines']:
#             print("\n✅ ADDED LINES:")
#             for line in changes['added_lines'][:10]:  # Show first 10 changes
#                 print(f"   Line {line['line_num']}: + {line['content']}")
#             if len(changes['added_lines']) > 10:
#                 print(f"   ... and {len(changes['added_lines']) - 10} more additions")
        
#         if changes['removed_lines']:
#             print("\n❌ REMOVED LINES:")
#             for line in changes['removed_lines'][:10]:  # Show first 10 changes
#                 print(f"   Line {line['line_num']}: - {line['content']}")
#             if len(changes['removed_lines']) > 10:
#                 print(f"   ... and {len(changes['removed_lines']) - 10} more removals")
        
#         print("\n" + "="*50)

#     def create_backup(self, file_path):
#         """Create a backup of the original file before any modifications"""
#         try:
#             backup_dir = Path("backups")
#             backup_dir.mkdir(exist_ok=True)
            
#             original_file = Path(file_path)
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             backup_filename = f"{original_file.stem}_{timestamp}{original_file.suffix}"
#             backup_path = backup_dir / backup_filename
            
#             # Read original and save as backup
#             with open(file_path, 'r', encoding='utf-8') as original:
#                 content = original.read()
            
#             with open(backup_path, 'w', encoding='utf-8') as backup:
#                 backup.write(content)
            
#             print(f"📋 Backup created: {backup_path}")
#             return str(backup_path)
            
#         except Exception as e:
#             print(f"❌ Failed to create backup: {e}")
#             return None

#     # def save_solution(self, file_path, solution_data, errors, original_code):
#     #     """Save solution with diff information for Fix Agent - NO FILE OVERWRITING"""
#     #     try:
#     #         # Create backup first
#     #         backup_path = self.create_backup(file_path)
            
#     #         solutions = []
#     #         if os.path.exists('solutions.json'):
#     #             with open('solutions.json', 'r') as f:
#     #                 solutions = json.load(f)
            
#     #         # Generate diff
#     #         changes = self.generate_diff(original_code, solution_data['corrected_code'])
            
#     #         solution_entry = {
#     #             "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     #             "file": file_path,
#     #             "backup_path": backup_path,
#     #             "errors": errors,
#     #             "corrected_code": solution_data['corrected_code'],
#     #             "explanation": solution_data['explanation'],
#     #             "recommendations": solution_data['recommendations'],
#     #             "changes": changes,
#     #             "status": "pending_review",
#     #             "auto_apply": False,  # IMPORTANT: Prevents automatic application
#     #             "requires_manual_review": True  # IMPORTANT: Requires manual approval
#     #         }
            
#     #         solutions.append(solution_entry)
            
#     #         # Save to solutions.json ONLY - DO NOT modify original files
#     #         with open('solutions.json', 'w') as f:
#     #             json.dump(solutions, f, indent=2)
            
#     #         print("🔒 SAFE MODE: Original file NOT modified")
#     #         print(f"💾 Solution saved to 'solutions.json' for manual review")
#     #         print(f"📋 Backup available at: {backup_path}")
            
#     #         return True
            
#     #     except Exception as e:
#     #         print(f"❌ Error saving solution: {e}")
#     #         return False

#     def save_solution(self, file_path, solution_data, errors, original_code):
#         """Save solution for Fix Agent - NO FILE OVERWRITING and NO diff"""
#         try:
#             # Create backup first
#             backup_path = self.create_backup(file_path)
            
#             solutions = []
#             if os.path.exists('solutions.json'):
#                 with open('solutions.json', 'r') as f:
#                     solutions = json.load(f)

#             # Solution entry without "changes"
#             solution_entry = {
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "file": file_path,
#                 "backup_path": backup_path,
#                 "errors": errors,
#                 "corrected_code": solution_data['corrected_code'],
#                 "explanation": solution_data['explanation'],
#                 "recommendations": solution_data['recommendations'],
#                 "status": "pending_review",
#                 "auto_apply": False,
#                 "requires_manual_review": True
#             }

#             solutions.append(solution_entry)

#             with open('solutions.json', 'w') as f:
#                 json.dump(solutions, f, indent=2)

#             print("🔒 SAFE MODE: Original file NOT modified")
#             print(f"💾 Solution saved to 'solutions.json' for manual review")
#             print(f"📋 Backup available at: {backup_path}")

#             return True

#         except Exception as e:
#             print(f"❌ Error saving solution: {e}")
#             return False


#     def save_solution_preview(self, file_path, solution_data):
#         """Save a preview of the corrected code to a separate file"""
#         try:
#             preview_dir = Path("solution_previews")
#             preview_dir.mkdir(exist_ok=True)
            
#             original_file = Path(file_path)
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             preview_filename = f"{original_file.stem}_corrected_{timestamp}{original_file.suffix}"
#             preview_path = preview_dir / preview_filename
            
#             with open(preview_path, 'w', encoding='utf-8') as preview:
#                 preview.write(solution_data['corrected_code'])
            
#             print(f"👀 Solution preview saved: {preview_path}")
#             return str(preview_path)
            
#         except Exception as e:
#             print(f"❌ Failed to save preview: {e}")
#             return None
    
#     def process_errors(self):
#         """Process new errors and generate solutions - SAFE MODE"""
#         error_log = self.load_error_log()
        
#         for error_entry in error_log:
#             # Create unique identifier for this error
#             error_id = f"{error_entry['file']}_{error_entry['timestamp']}"
            
#             if error_id not in self.processed_errors and error_entry['status'] == 'detected':
#                 print(f"\n🔍 Processing error in: {error_entry['file']}")
#                 print(f"⏰ Detected at: {error_entry['timestamp']}")
                
#                 # Read current file content (READ ONLY)
#                 try:
#                     with open(error_entry['file'], 'r', encoding='utf-8') as f:
#                         original_content = f.read()
                    
#                     print(f"🤖 Generating AI solution for {error_id}")
#                     print("🔒 SAFE MODE: Original file will NOT be modified")
                    
#                     # Generate solution
#                     solution_text = self.generate_solution(
#                         error_entry['file'],
#                         original_content,
#                         error_entry['errors'],
#                     )
                    
#                     # Parse solution
#                     solution_data = self.parse_solution(solution_text)
                    
#                     print("✅ Solution generated successfully!")
#                     print(f"📝 Explanation: {solution_data['explanation'][:100]}...")
                    
#                     # Generate and display diff
#                     # changes = self.generate_diff(original_content, solution_data['corrected_code'])
#                     # self.display_changes(changes)
                    
#                     print("🧪 Diff generation skipped as per config")
#                     # Save solution preview
#                     preview_path = self.save_solution_preview(error_entry['file'], solution_data)
                    
#                     # Save solution to JSON for manual review (NO FILE OVERWRITING)
#                     if self.save_solution(error_entry['file'], solution_data, error_entry['errors'], original_content):
#                         print("💾 Solution saved for manual review")
#                         print(f"👀 Preview available at: {preview_path}")
#                         self.processed_errors.add(error_id)
#                     else:
#                         print("❌ Failed to save solution")
                
#                 except Exception as e:
#                     print(f"❌ Error processing {error_entry['file']}: {e}")
    
#     def run(self):
#         print("🔄 Waiting for errors from Monitor Agent...")
#         print("📋 Solutions will be saved for manual review")
        
#         try:
#             while True:
#                 self.process_errors()
#                 time.sleep(3)  # Check every 3 seconds
                
#         except KeyboardInterrupt:
#             print("\n\n🛑 Solution Agent stopped by user")
#             print(f"📊 Session Summary:")
#             print(f"   • Errors processed: {len(self.processed_errors)}")
#             print("💾 Solutions saved to 'solutions.json' for manual review")
#             print("📋 Backups available in 'backups/' directory")
#             print("👀 Solution previews available in 'solution_previews/' directory")
#             print("🔒 SAFE MODE: No original files were modified")

# if __name__ == "__main__":
#     try:
#         solution_agent = SolutionAgent()
#         solution_agent.run()
#     except Exception as e:
#         print(f"❌ Solution Agent failed to start: {e}")
#         print("💡 Make sure you have GEMINI_API_KEY in your .env file")


# Full updated SolutionAgent class with:
# - Error log status/stage/last_checked update
# - Structured explanation per error
# - Minimum 3 recommendations in list form

from datetime import datetime
import os
import time
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

class SolutionAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}"
        self.processed_errors = set()

        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        print("🔧 Solution Agent initialized")
        print("🤖 AI Model: Gemini 2.0 Flash")
        print("=" * 60)

    def load_error_log(self):
        try:
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading log: {e}")
            return []

    def generate_solution(self, file_path, file_content, errors):
        file_extension = Path(file_path).suffix.lower()

        context = {
            '.html': "This is an HTML file for a hotel booking system. Focus on proper HTML structure, accessibility, and semantic markup.",
            '.css': "This is a CSS file for styling a hotel booking system. Focus on proper CSS syntax, responsive design, and modern styling practices.",
            '.js': "This is a JavaScript file for a hotel booking system. Focus on proper syntax, error handling, and modern JavaScript practices.",
        }.get(file_extension, "This is a code file that needs to be fixed.")

        file_type = file_extension.upper().strip('.') or 'Code'

        prompt = f"""
You are an expert {file_type} developer working on a hotel booking system.

Context: {context}

Original Code:
{file_content}

Detected Issues:
{errors}

Please ONLY provide:
1. The COMPLETE corrected file content
2. ONLY FIX the listed issues — do NOT reformat or make stylistic changes
3. DO NOT add unrelated enhancements
4. DO NOT explain anything — only the result

Format your response as:
CORRECTED_CODE:
[Complete corrected code here]

RECOMMENDATIONS:
[Optional brief improvements to consider — outside scope of this fix]
        """

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 4000
            }
        }

        response = requests.post(self.gemini_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                return result['candidates'][0]['content']['parts'][0]['text']
        return "❌ Failed to generate solution"

    def parse_solution(self, solution_text):
        corrected_code = ""
        recommendations = []
        lines = solution_text.split('\n')
        current_section = None

        for line in lines:
            if line.strip().startswith('CORRECTED_CODE:'):
                current_section = 'code'
                continue
            elif line.strip().startswith('RECOMMENDATIONS:'):
                current_section = 'recommendations'
                continue

            if current_section == 'code':
                corrected_code += line + '\n'
            elif current_section == 'recommendations':
                cleaned = line.strip('-• ').strip()
                if cleaned:
                    recommendations.append(cleaned)

        corrected_code = re.sub(r'^```[\w]*\n', '', corrected_code)
        corrected_code = re.sub(r'\n?```[\s]*$', '', corrected_code)
        corrected_code = corrected_code.strip()

        if len(recommendations) < 3:
            recommendations += [
                "Use semantic HTML elements to improve accessibility.",
                "Minimize inline styles and use CSS classes instead.",
                "Ensure all tags are properly closed and nested."
            ][:3 - len(recommendations)]

        return {
            'corrected_code': corrected_code,
            'recommendations': recommendations
        }

    def build_explanation_list(self, errors):
        explanation_list = []

        for err in errors:
            entry = {"error": err}
            if "Missing <title>" in err:
                entry["explanation"] = "The HTML document is missing a <title> tag, which is important for SEO and accessibility."
                entry["code"] = "<title>Your Hotel Name</title>"
            elif "Incomplete tag" in err:
                entry["explanation"] = "A tag is missing a closing bracket '>'. This causes rendering issues in HTML."
                entry["code"] = "<p>&copy; 2025 The Meridian Grand. All rights reserved.</p>"
            else:
                entry["explanation"] = "This issue needs to be reviewed manually."
                entry["code"] = "[Review required]"
            explanation_list.append(entry)

        return explanation_list

    def create_backup(self, file_path):
        try:
            backup_dir = Path("backups")
            backup_dir.mkdir(exist_ok=True)

            original_file = Path(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{original_file.stem}_{timestamp}{original_file.suffix}"
            backup_path = backup_dir / backup_filename

            with open(file_path, 'r', encoding='utf-8') as original:
                content = original.read()

            with open(backup_path, 'w', encoding='utf-8') as backup:
                backup.write(content)

            print(f"📋 Backup created: {backup_path}")
            return str(backup_path)

        except Exception as e:
            print(f"❌ Failed to create backup: {e}")
            return None

    def save_solution(self, file_path, solution_data, errors, original_code):
        try:
            backup_path = self.create_backup(file_path)

            solutions = []
            if os.path.exists('solutions.json'):
                with open('solutions.json', 'r') as f:
                    solutions = json.load(f)

            solution_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file": file_path,
                "backup_path": backup_path,
                "errors": errors,
                "corrected_code": solution_data['corrected_code'],
                "explanation": solution_data['explanation'],
                "recommendations": solution_data['recommendations'],
                "status": "pending_review",
                "auto_apply": False,
                "requires_manual_review": True
            }

            solutions.append(solution_entry)

            with open('solutions.json', 'w') as f:
                json.dump(solutions, f, indent=2)

            print("💾 Solution saved to 'solutions.json' for manual review")
            return True

        except Exception as e:
            print(f"❌ Error saving solution: {e}")
            return False

    def save_solution_preview(self, file_path, solution_data):
        try:
            preview_dir = Path("solution_previews")
            preview_dir.mkdir(exist_ok=True)

            original_file = Path(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            preview_filename = f"{original_file.stem}_corrected_{timestamp}{original_file.suffix}"
            preview_path = preview_dir / preview_filename

            with open(preview_path, 'w', encoding='utf-8') as preview:
                preview.write(solution_data['corrected_code'])

            print(f"👀 Solution preview saved: {preview_path}")
            return str(preview_path)

        except Exception as e:
            print(f"❌ Failed to save preview: {e}")
            return None

    def process_errors(self):
        error_log = self.load_error_log()

        for error_entry in error_log:
            error_id = f"{error_entry['file']}_{error_entry['timestamp']}"

            if error_id not in self.processed_errors and error_entry['status'] == 'detected':
                error_entry['status'] = 'fixing'
                error_entry['pipeline_stage'] = 'solving'
                error_entry['last_checked'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                with open('error_log.json', 'w') as f:
                    json.dump(error_log, f, indent=2)

                print(f"\n🔍 Processing error in: {error_entry['file']}")
                try:
                    with open(error_entry['file'], 'r', encoding='utf-8') as f:
                        original_content = f.read()

                    solution_text = self.generate_solution(
                        error_entry['file'],
                        original_content,
                        error_entry['errors']
                    )

                    solution_data = self.parse_solution(solution_text)
                    solution_data['explanation'] = self.build_explanation_list(error_entry['errors'])

                    preview_path = self.save_solution_preview(error_entry['file'], solution_data)

                    if self.save_solution(error_entry['file'], solution_data, error_entry['errors'], original_content):
                        print(f"✅ Saved solution. Preview at: {preview_path}")
                        self.processed_errors.add(error_id)
                    else:
                        print("❌ Failed to save solution")

                except Exception as e:
                    print(f"❌ Error processing {error_entry['file']}: {e}")

    def run(self):
        print("🔄 Waiting for errors from Monitor Agent...")
        try:
            while True:
                self.process_errors()
                time.sleep(3)
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user")
            print(f"🧾 Processed: {len(self.processed_errors)} entries")

if __name__ == "__main__":
    try:
        agent = SolutionAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Failed to start: {e}")
