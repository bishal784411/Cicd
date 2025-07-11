# import os
# import time
# import json
# import requests
# from datetime import datetime
# from pathlib import Path
# from dotenv import load_dotenv

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
#                     return json.load(f)
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
            
            
            
#             Please provide:
#             1. Complete corrected code (full file content)
#             2. No explanation of each fix
#             3. Best practices recommendations
#             4. Any additional improvements for hotel booking functionality
            
#             Important: 
#             - Provide the COMPLETE corrected file content only
#             - Do NOT add any comments in the code
#             - Maintain the original functionality while fixing errors
#             - Follow modern coding standards

            
#             Format your response as:
#             CORRECTED_CODE:
#             [Complete corrected code here]

            
#             RECOMMENDATIONS:
#             [Additional recommendations]
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
    
#     # def parse_solution(self, solution_text):
#     #     """Parse the AI solution into components"""
#     #     try:
#     #         # Extract corrected code
#     #         corrected_code = ""
#     #         explanation = ""
#     #         recommendations = ""
            
#     #         lines = solution_text.split('\n')
#     #         current_section = None
            
#     #         for line in lines:
#     #             if line.strip().startswith('CORRECTED_CODE:'):
#     #                 current_section = 'code'
#     #                 continue
#     #             elif line.strip().startswith('EXPLANATION:'):
#     #                 current_section = 'explanation'
#     #                 continue
#     #             elif line.strip().startswith('RECOMMENDATIONS:'):
#     #                 current_section = 'recommendations'
#     #                 continue
                
#     #             if current_section == 'code':
#     #                 corrected_code += line + '\n'
#     #             elif current_section == 'explanation':
#     #                 explanation += line + '\n'
#     #             elif current_section == 'recommendations':
#     #                 recommendations += line + '\n'
            
#     #         # If structured format not found, try to extract code blocks
#     #         if not corrected_code.strip():
#     #             import re
#     #             code_blocks = re.findall(r'```[\w]*\n(.*?)```', solution_text, re.DOTALL)
#     #             if code_blocks:
#     #                 corrected_code = code_blocks[0]
#     #             else:
#     #                 corrected_code = solution_text
            
#     #         return {
#     #             'corrected_code': corrected_code.strip(),
#     #             'explanation': explanation.strip(),
#     #             'recommendations': recommendations.strip()
#     #         }
            
#     #     except Exception as e:
#     #         return {
#     #             'corrected_code': solution_text,
#     #             'explanation': f"Parse error: {str(e)}",
#     #             'recommendations': ""
#     #         }
    
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
#             # corrected_code = re.sub(r'\n```$', '', corrected_code)
#             corrected_code = re.sub(r'\n?```[\s]*$', '', corrected_code)
#             corrected_code = corrected_code.strip()
#             # corrected_code = re.sub(r'^\s*```\s*$', '', corrected_code, flags=re.MULTILINE).strip()


            
            
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

#     def save_solution(self, file_path, solution_data, errors):
#         """Save solution for Fix Agent"""
#         try:
#             solutions = []
#             if os.path.exists('solutions.json'):
#                 with open('solutions.json', 'r') as f:
#                     solutions = json.load(f)
            
#             solution_entry = {
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                 "file": file_path,
#                 "errors": errors,
#                 "corrected_code": solution_data['corrected_code'],
#                 "explanation": solution_data['explanation'],
#                 "recommendations": solution_data['recommendations'],
#                 "status": "pending_review"
#             }
            
#             solutions.append(solution_entry)
            
#             with open('solutions.json', 'w') as f:
#                 json.dump(solutions, f, indent=2)
            
#             return True
            
#         except Exception as e:
#             print(f"❌ Error saving solution: {e}")
#             return False
    
#     def process_errors(self):
#         """Process new errors and generate solutions"""
#         error_log = self.load_error_log()
        
#         for error_entry in error_log:
#             # Create unique identifier for this error
#             error_id = f"{error_entry['file']}_{error_entry['timestamp']}"
            
#             if error_id not in self.processed_errors and error_entry['status'] == 'detected':
#                 print(f"\n🔍 Processing error in: {error_entry['file']}")
#                 print(f"⏰ Detected at: {error_entry['timestamp']}")
                
#                 # Read current file content
#                 try:
#                     with open(error_entry['file'], 'r', encoding='utf-8') as f:
#                         file_content = f.read()
                    
#                     print(f"🤖 Generating AI solution for {error_id}")
                    
#                     # Generate solution
#                     solution_text = self.generate_solution(
#                         error_entry['file'],
#                         file_content,
#                         error_entry['errors'],
                        
#                     )
                    
#                     # Parse solution
#                     solution_data = self.parse_solution(solution_text)
                    
#                     print("✅ Solution generated successfully!")
#                     print(f"📝 Explanation: {solution_data['explanation'][:100]}...")
                    
#                     # Save solution
#                     if self.save_solution(error_entry['file'], solution_data, error_entry['errors']):
#                         print("💾 Solution saved for Fix Agent")
#                         self.processed_errors.add(error_id)
#                     else:
#                         print("❌ Failed to save solution")
                
#                 except Exception as e:
#                     print(f"❌ Error processing {error_entry['file']}: {e}")
    
#     def run(self):
#         """Main solution generation loop"""
#         print("🚀 Starting solution generation monitoring...")
#         print("🔄 Waiting for errors from Monitor Agent...")
#         print("🔄 Press Ctrl+C to stop\n")
        
#         try:
#             while True:
#                 self.process_errors()
#                 time.sleep(3)  # Check every 3 seconds
                
#         except KeyboardInterrupt:
#             print("\n\n🛑 Solution Agent stopped by user")
#             print(f"📊 Session Summary:")
#             print(f"   • Errors processed: {len(self.processed_errors)}")
#             print("💾 Solutions saved to 'solutions.json'")

# if __name__ == "__main__":
#     try:
#         solution_agent = SolutionAgent()
#         solution_agent.run()
#     except Exception as e:
#         print(f"❌ Solution Agent failed to start: {e}")
#         print("💡 Make sure you have GEMINI_API_KEY in your .env file")

import os
import time
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import difflib

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
        """Load error log from Monitor Agent"""
        try:
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading log: {e}")
            return []

    def generate_solution(self, file_path, file_content, errors):
        """Generate solution using Gemini AI"""
        try:
            file_extension = Path(file_path).suffix.lower()
            
            # Determine file type for context
            if file_extension == '.html':
                file_type = "HTML"
                context = "This is an HTML file for a hotel booking system. Focus on proper HTML structure, accessibility, and semantic markup."
            elif file_extension == '.css':
                file_type = "CSS"
                context = "This is a CSS file for styling a hotel booking system. Focus on proper CSS syntax, responsive design, and modern styling practices."
            elif file_extension == '.js':
                file_type = "JavaScript"
                context = "This is a JavaScript file for a hotel booking system. Focus on proper syntax, error handling, and modern JavaScript practices."
            else:
                file_type = "Code"
                context = "This is a code file that needs to be fixed."
            
            prompt = f"""
            You are an expert {file_type} HTML, CSS and Javascript developer working on a hotel booking system. 
            
            Context: {context}
            
            Original Code:
            {file_content}
            
            Detected Issues:
            {errors}
            
            Please provide:
            1. Complete corrected code (full file content)
            2. No explanation of each fix
            3. Best practices recommendations
            4. Any additional improvements for hotel booking functionality
            
            Important: 
            - Provide the COMPLETE corrected file content only
            - Do NOT add any comments in the code
            - Maintain the original functionality while fixing errors
            - Follow modern coding standards

            Format your response as:
            CORRECTED_CODE:
            [Complete corrected code here]

            RECOMMENDATIONS:
            [Additional recommendations]
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
            
        except Exception as e:
            return f"❌ Solution generation error: {str(e)}"
    
    def parse_solution(self, solution_text):
        """Parse the AI solution into components"""
        try:
            import re
            corrected_code = ""
            explanation = ""
            recommendations = ""

            lines = solution_text.split('\n')
            current_section = None

            for line in lines:
                if line.strip().startswith('CORRECTED_CODE:'):
                    current_section = 'code'
                    continue
                elif line.strip().startswith('EXPLANATION:'):
                    current_section = 'explanation'
                    continue
                elif line.strip().startswith('RECOMMENDATIONS:'):
                    current_section = 'recommendations'
                    continue

                if current_section == 'code':
                    corrected_code += line + '\n'
                elif current_section == 'explanation':
                    explanation += line + '\n'
                elif current_section == 'recommendations':
                    recommendations += line + '\n'

            corrected_code = re.sub(r'^```[\w]*\n', '', corrected_code)
            corrected_code = re.sub(r'\n?```[\s]*$', '', corrected_code)
            corrected_code = corrected_code.strip()
            
            return {
                'corrected_code': corrected_code,
                'explanation': explanation.strip(),
                'recommendations': recommendations.strip()
            }

        except Exception as e:
            return {
                'corrected_code': solution_text,
                'explanation': f"Parse error: {str(e)}",
                'recommendations': ""
            }

    def generate_diff(self, original_code, corrected_code):
        """Generate detailed diff between original and corrected code"""
        try:
            original_lines = original_code.splitlines(keepends=True)
            corrected_lines = corrected_code.splitlines(keepends=True)
            
            # Generate unified diff
            diff = list(difflib.unified_diff(
                original_lines,
                corrected_lines,
                fromfile='original',
                tofile='corrected',
                lineterm=''
            ))
            
            # Parse diff to extract changes
            changes = {
                'added_lines': [],
                'removed_lines': [],
                'modified_lines': [],
                'line_changes': []
            }
            
            current_line_num = 0
            
            for line in diff:
                if line.startswith('@@'):
                    # Extract line numbers from diff header
                    import re
                    match = re.search(r'-(\d+),?\d* \+(\d+),?\d*', line)
                    if match:
                        current_line_num = int(match.group(2))
                elif line.startswith('+') and not line.startswith('+++'):
                    changes['added_lines'].append({
                        'line_num': current_line_num,
                        'content': line[1:].rstrip()
                    })
                    current_line_num += 1
                elif line.startswith('-') and not line.startswith('---'):
                    changes['removed_lines'].append({
                        'line_num': current_line_num,
                        'content': line[1:].rstrip()
                    })
                elif line.startswith(' '):
                    current_line_num += 1
            
            # Generate summary
            changes['summary'] = {
                'total_lines_added': len(changes['added_lines']),
                'total_lines_removed': len(changes['removed_lines']),
                'diff_text': ''.join(diff) if diff else 'No changes detected'
            }
            
            return changes
            
        except Exception as e:
            return {
                'error': f"Diff generation failed: {str(e)}",
                'summary': {'total_lines_added': 0, 'total_lines_removed': 0, 'diff_text': ''}
            }

    def display_changes(self, changes):
        """Display changes in a readable format"""
        print("\n" + "="*50)
        print("🔍 CODE CHANGES DETECTED")
        print("="*50)
        
        if 'error' in changes:
            print(f"❌ {changes['error']}")
            return
        
        summary = changes['summary']
        print(f"📊 Summary: +{summary['total_lines_added']} lines added, -{summary['total_lines_removed']} lines removed")
        
        if changes['added_lines']:
            print("\n✅ ADDED LINES:")
            for line in changes['added_lines'][:10]:  # Show first 10 changes
                print(f"   Line {line['line_num']}: + {line['content']}")
            if len(changes['added_lines']) > 10:
                print(f"   ... and {len(changes['added_lines']) - 10} more additions")
        
        if changes['removed_lines']:
            print("\n❌ REMOVED LINES:")
            for line in changes['removed_lines'][:10]:  # Show first 10 changes
                print(f"   Line {line['line_num']}: - {line['content']}")
            if len(changes['removed_lines']) > 10:
                print(f"   ... and {len(changes['removed_lines']) - 10} more removals")
        
        print("\n" + "="*50)

    def save_solution(self, file_path, solution_data, errors, original_code):
        """Save solution with diff information for Fix Agent"""
        try:
            solutions = []
            if os.path.exists('solutions.json'):
                with open('solutions.json', 'r') as f:
                    solutions = json.load(f)
            
            # Generate diff
            changes = self.generate_diff(original_code, solution_data['corrected_code'])
            
            solution_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file": file_path,
                "errors": errors,
                "corrected_code": solution_data['corrected_code'],
                "explanation": solution_data['explanation'],
                "recommendations": solution_data['recommendations'],
                "changes": changes,
                "status": "pending_review"
            }
            
            solutions.append(solution_entry)
            
            with open('solutions.json', 'w') as f:
                json.dump(solutions, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Error saving solution: {e}")
            return False
    
    def process_errors(self):
        """Process new errors and generate solutions"""
        error_log = self.load_error_log()
        
        for error_entry in error_log:
            # Create unique identifier for this error
            error_id = f"{error_entry['file']}_{error_entry['timestamp']}"
            
            if error_id not in self.processed_errors and error_entry['status'] == 'detected':
                print(f"\n🔍 Processing error in: {error_entry['file']}")
                print(f"⏰ Detected at: {error_entry['timestamp']}")
                
                # Read current file content
                try:
                    with open(error_entry['file'], 'r', encoding='utf-8') as f:
                        original_content = f.read()
                    
                    print(f"🤖 Generating AI solution for {error_id}")
                    
                    # Generate solution
                    solution_text = self.generate_solution(
                        error_entry['file'],
                        original_content,
                        error_entry['errors'],
                    )
                    
                    # Parse solution
                    solution_data = self.parse_solution(solution_text)
                    
                    print("✅ Solution generated successfully!")
                    print(f"📝 Explanation: {solution_data['explanation'][:100]}...")
                    
                    # Generate and display diff
                    changes = self.generate_diff(original_content, solution_data['corrected_code'])
                    self.display_changes(changes)
                    
                    # Save solution with diff
                    if self.save_solution(error_entry['file'], solution_data, error_entry['errors'], original_content):
                        print("💾 Solution saved for Fix Agent")
                        self.processed_errors.add(error_id)
                    else:
                        print("❌ Failed to save solution")
                
                except Exception as e:
                    print(f"❌ Error processing {error_entry['file']}: {e}")
    
    def run(self):
        """Main solution generation loop"""
        print("🚀 Starting solution generation monitoring...")
        print("🔄 Waiting for errors from Monitor Agent...")
        print("🔄 Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.process_errors()
                time.sleep(3)  # Check every 3 seconds
                
        except KeyboardInterrupt:
            print("\n\n🛑 Solution Agent stopped by user")
            print(f"📊 Session Summary:")
            print(f"   • Errors processed: {len(self.processed_errors)}")
            print("💾 Solutions saved to 'solutions.json'")

if __name__ == "__main__":
    try:
        solution_agent = SolutionAgent()
        solution_agent.run()
    except Exception as e:
        print(f"❌ Solution Agent failed to start: {e}")
        print("💡 Make sure you have GEMINI_API_KEY in your .env file")