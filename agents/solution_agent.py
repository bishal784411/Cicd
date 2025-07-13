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

METADATA:
created_by: [your current Model Name]
model_confidence: [Give an honest confidence estimate between 0.00 and 1.00 based on your certainty in the correctness of the fix. This should reflect your internal certainty level.
]
time_estimate_fix: [Estimated time to fix the error by ai agent, e.g. "2 minutes"]
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
        metadata = {}
        lines = solution_text.split('\n')
        current_section = None

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('CORRECTED_CODE:'):
                current_section = 'code'
                continue
            elif stripped.startswith('RECOMMENDATIONS:'):
                current_section = 'recommendations'
                continue
            elif stripped.startswith('METADATA:'):
                current_section = 'metadata'
                continue

            if current_section == 'code':
                corrected_code += line + '\n'
            elif current_section == 'recommendations':
                cleaned = stripped.strip('-• ').strip()
                if cleaned:
                    recommendations.append(cleaned)
            elif current_section == 'metadata':
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        corrected_code = re.sub(r'^```[\w]*\n', '', corrected_code)
        corrected_code = re.sub(r'\n?```[\s]*$', '', corrected_code)
        corrected_code = corrected_code.strip()

        if len(recommendations) < 3:
            recommendations += [
                "Use semantic HTML elements to improve accessibility.",
                "Minimize inline styles and use CSS classes instead.",
                "Ensure all tags are properly closed and nested."
            ][:3 - len(recommendations)]

        # Defaults if not present
        metadata.setdefault("created_by", "Gemini 2.0 Flash")
        metadata.setdefault("model_confidence", 0.87)
        metadata.setdefault("time_estimate_fix", "2 minutes")

        return {
            'corrected_code': corrected_code,
            'recommendations': recommendations,
            'metadata': {
                'created_by': metadata["created_by"],
                'model_confidence': float(metadata["model_confidence"]),
                'time_estimate_fix': metadata["time_estimate_fix"]
            }
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

    def save_solution(self, file_path, solution_data, errors, original_code, error_entry):
        try:
            backup_path = self.create_backup(file_path)
            solutions = []
            if os.path.exists('solutions.json'):
                with open('solutions.json', 'r') as f:
                    solutions = json.load(f)

            solution_id = f"SOL-{len(solutions) + 1:03}"

            available_solutions = []
            for err in errors:
                match = next((ex for ex in solution_data['explanation'] if ex['error'] == err), None)
                available_solutions.append({
                    "error": err,
                    "explanation": {
                        "text": match["explanation"] if match else "Explanation not available.",
                        "code_example": match["code"] if match else "[N/A]"
                    }
                })

            file_extension = Path(file_path).suffix.lower()
            context = {
                '.html': "This is an HTML file for a hotel booking system. Focus on proper HTML structure, accessibility, and semantic markup.",
                '.css': "This is a CSS file for styling a hotel booking system. Focus on proper CSS syntax, responsive design, and modern styling practices.",
                '.js': "This is a JavaScript file for a hotel booking system. Focus on proper syntax, error handling, and modern JavaScript practices.",
            }.get(file_extension, "This is a code file that needs to be fixed.")
            file_type = file_extension.upper().strip('.') or 'Code'


            solution_entry = {
                "solution_id": solution_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "file": file_path,
                "backup_path": backup_path,
                "errors": errors,
                "corrected_code": solution_data['corrected_code'],
                "available_solutions": available_solutions,
                "status": "pending_review",
                "auto_apply": False,
                "requires_manual_review": True,
                "error_type": error_entry.get("error_type", "UnknownError"),
                "pipeline_stage": "solving",
                "commit_hash": "not pushed",
                "branch": "main",
                "model_confidence": solution_data['metadata']['model_confidence'],
                "time_estimate_fix": solution_data['metadata']['time_estimate_fix'],
                "created_by": solution_data['metadata']['created_by'],

            }

            solutions.append(solution_entry)
            with open('solutions.json', 'w') as f:
                json.dump(solutions, f, indent=2)

            print("💾 Solution saved to 'solutions.json' in full structure")
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

                    # if self.save_solution(error_entry['file'], solution_data, error_entry['errors'], original_content):
                    if self.save_solution(error_entry['file'], solution_data, error_entry['errors'], original_content, error_entry):

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
