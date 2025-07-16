import os
import time
import json
import shutil
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import difflib

# Load environment variables
load_dotenv()

class AIFixAgent:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}"
        self.processed_solutions = set()
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        print("🤖 AI Fix Agent initialized")
        print("🧠 AI Model: Gemini 2.0 Flash")
        print("🌐 Multi-language support: Python, JavaScript, HTML, CSS, Java, C++, and more")
        print("📁 Backup directory: ./backups")
        print("=" * 60)
    
    def load_solutions(self):
        """Load solutions from Solution Agent"""
        try:
            if os.path.exists('solutions.json'):
                with open('solutions.json', 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            print(f"❌ Error loading solutions: {e}")
            return []
    
    def create_backup(self, file_path):
        """Create backup of original file"""
        try:
            file_path = Path(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            shutil.copy2(file_path, backup_path)
            print(f"📋 Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            return None
    
    def get_file_language(self, file_path):
        """Determine programming language from file extension"""
        extension = Path(file_path).suffix.lower()
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.go': 'Go',
            '.rs': 'Rust',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.vue': 'Vue.js',
            '.sql': 'SQL',
            '.sh': 'Shell Script',
            '.json': 'JSON',
            '.xml': 'XML',
            '.yaml': 'YAML',
            '.yml': 'YAML'
        }
        return language_map.get(extension, 'Code')
    
    def analyze_fix_with_ai(self, file_path, original_code, proposed_fix, errors):
        """Use AI to analyze if the fix should be applied"""
        try:
            language = self.get_file_language(file_path)
            
            prompt = f"""
            You are an expert code reviewer and fix analyst. Analyze the proposed fix and determine if it should be applied.
            
            CONTEXT:
            - File: {file_path}
            - Language: {language}
            - Original errors detected: {', '.join(errors)}
            
            ORIGINAL CODE:
            {original_code[:2000]}...
            
            PROPOSED FIX:
            {proposed_fix[:2000]}...
            
            ANALYSIS REQUIRED:
            1. Safety: Will this fix break existing functionality?
            2. Correctness: Does it properly address the detected errors?
            3. Quality: Does it follow best practices for {language}?
            4. Risk Level: Low/Medium/High risk of introducing new issues?
            
            DECISION CRITERIA:
            - Apply if: Fix is safe, correct, and low-risk
            - Skip if: Fix might break functionality or introduce new issues
            - Manual review if: Complex changes that need human verification
            
            Respond with EXACTLY this format:
            DECISION: [APPLY/SKIP/MANUAL_REVIEW]
            RISK_LEVEL: [LOW/MEDIUM/HIGH]
            CONFIDENCE: [0-100]%
            REASONING: [Brief explanation of your decision]
            SAFETY_NOTES: [Any safety concerns or recommendations]
            """
            
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "topK": 20,
                    "topP": 0.8,
                    "maxOutputTokens": 1000
                }
            }
            
            response = requests.post(self.gemini_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            
            return "❌ AI analysis failed"
            
        except Exception as e:
            return f"❌ AI analysis error: {str(e)}"
    
    def parse_ai_decision(self, ai_response):
        """Parse AI decision response"""
        try:
            lines = ai_response.split('\n')
            decision = "MANUAL_REVIEW"
            risk_level = "HIGH"
            confidence = 0
            reasoning = "Failed to parse AI response"
            safety_notes = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith('DECISION:'):
                    decision = line.split(':', 1)[1].strip()
                elif line.startswith('RISK_LEVEL:'):
                    risk_level = line.split(':', 1)[1].strip()
                elif line.startswith('CONFIDENCE:'):
                    confidence_str = line.split(':', 1)[1].strip().replace('%', '')
                    try:
                        confidence = int(confidence_str)
                    except:
                        confidence = 0
                elif line.startswith('REASONING:'):
                    reasoning = line.split(':', 1)[1].strip()
                elif line.startswith('SAFETY_NOTES:'):
                    safety_notes = line.split(':', 1)[1].strip()
            
            return {
                'decision': decision,
                'risk_level': risk_level,
                'confidence': confidence,
                'reasoning': reasoning,
                'safety_notes': safety_notes
            }
            
        except Exception as e:
            return {
                'decision': 'MANUAL_REVIEW',
                'risk_level': 'HIGH',
                'confidence': 0,
                'reasoning': f"Parse error: {str(e)}",
                'safety_notes': 'Failed to parse AI response'
            }
    
    def display_diff(self, original_code, fixed_code, file_path):
        """Display code differences"""
        print("\n" + "=" * 80)
        print(f"📄 FILE: {file_path}")
        print("=" * 80)
        
        # Create unified diff
        diff = list(difflib.unified_diff(
            original_code.splitlines(keepends=True),
            fixed_code.splitlines(keepends=True),
            fromfile=f"Original",
            tofile=f"Fixed",
            lineterm=''
        ))
        
        if diff:
            print("\n🔍 CHANGES DETECTED")
            
            

    
    def apply_fix(self, file_path, fixed_code):
        """Apply the fix to the file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            print(f"✅ Fix applied successfully to: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to apply fix: {e}")
            return False
    
    
    def update_error_log_status(self, file_path, new_status):
        """Update error log status and track previous status"""
        try:
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    error_log = json.load(f)

                for entry in error_log:
                    if entry['file'] == file_path and entry['status'] == 'detected':
                        # Track previous status only if it's changing
                        if entry['status'] != new_status:
                            entry['previous_status'] = entry['status']
                            entry['status'] = new_status
                            entry['fixed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open('error_log.json', 'w') as f:
                    json.dump(error_log, f, indent=2)

                print(f"📝 Error log updated: {file_path} marked as {new_status}")
        
        except Exception as e:
            print(f"❌ Error updating error log: {e}")
            
    def update_process_flow_with_fix(self, file_path, err_id, fix_id, ai_analysis):
        try:
            if not os.path.exists('process_flow.json'):
                print("⚠️ process_flow.json not found.")
                return False

            with open('process_flow.json', 'r') as f:
                process_log = json.load(f)

            matched = False
            for item in process_log:
                filename_match = item.get('filename', '').strip().lower() == file_path.strip().lower()
                error_id_match = item.get('monitor', {}).get('error_id', '').strip() == err_id.strip()

                if filename_match and error_id_match:
                    reasoning_text = " | ".join([
                        f"{a['reasoning']}" for a in ai_analysis if 'reasoning' in a
                    ])

                    item['Fix'] = {
                        "fix_id": fix_id,
                        "status": "completed",
                        "time": datetime.now().strftime("%I:%M:%S %p"),
                        "analysis": reasoning_text
                    }

                    matched = True
                    break

            if matched:
                with open('process_flow.json', 'w') as f:
                    json.dump(process_log, f, indent=2)
                print(f"📝 process_flow.json updated with fix_id: {fix_id}")
                return True
            else:
                print(f"⚠️ No matching entry found in process_flow.json for err_id: {err_id}")
                return False

        except Exception as e:
            print(f"❌ Error updating process_flow.json: {e}")
            return False
        
    def save_to_fix_log(self, solution, ai_analysis):
        """Save applied solution to fix_log.json with sequential fix_id (FIX-001, FIX-002, ...)"""
        try:
            fix_log_path = Path("fix_log.json")
            fix_log = []

            if fix_log_path.exists():
                with open(fix_log_path, 'r') as f:
                    fix_log = json.load(f)

            # Generate the next FIX ID
            existing_ids = [
                int(entry['fix_id'].split('-')[1])
                for entry in fix_log
                if 'fix_id' in entry and entry['fix_id'].startswith('FIX-') and entry['fix_id'].split('-')[1].isdigit()
            ]
            next_id = max(existing_ids, default=0) + 1
            fix_id = f"FIX-{next_id:03d}"  # Format as FIX-001, FIX-002, etc.

            solution_entry = {
                'fix_id': fix_id,
                'solution_id': solution.get('solution_id', 'N/A'),
                'err_id': solution.get('err_id', 'N/A'),
                'timestamp': solution['timestamp'],
                'file': solution['file'],
                'language': self.get_file_language(solution['file']),
                'errors': solution['errors'],
                'status': solution.get('fix_status', 'unknown'),
                'applied_at': solution.get('applied_at', ''),
                'ai_analysis': ai_analysis if isinstance(ai_analysis, list) else [ai_analysis],
                'error_type': solution.get('error_type', 'unknown'),
                'recommendations': solution.get('recommendations', ''),
                "commit_hash": "not pushed",
                "branch": "main",
                "git_push": "not pushed",
                'error_push': None
            }

            fix_log.append(solution_entry)

            with open(fix_log_path, 'w') as f:
                json.dump(fix_log, f, indent=2)

            print(f"📦 Fix saved to fix_log.json with ID: {fix_id}")
            return fix_id

        except Exception as e:
            print(f"❌ Failed to save to fix_log.json: {e}")
            return None

    def process_solutions(self):
        """Process pending solutions with AI analysis"""
        solutions = self.load_solutions()

        def clean_solution_entry(solution, fix_status, was_applied=False):
            """Clean and standardize the solution format"""
            if solution.get('status') != fix_status:
                solution['previous_status'] = solution.get('status', 'unknown')

            solution['fix_status'] = 'applied' if was_applied else 'not_applied_yet'

            if was_applied:
                solution['applied_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                solution.pop('applied_at', None)

            # Remove unnecessary fields
            for field in ['status', 'auto_apply', 'requires_manual_review', 'ai_decision']:
                solution.pop(field, None)

        for i, solution in enumerate(solutions):
            solution_id = f"{solution['file']}_{solution['timestamp']}"

            if (
                solution_id not in self.processed_solutions and
                solution.get('status') == 'pending_review' and
                solution.get('requires_manual_review', False)
            ):
                print(f"\n🔍 PROCESSING SOLUTION")
                print(f"📄 File: {solution['file']} ({self.get_file_language(solution['file'])})")
                print(f"⏰ Generated: {solution['timestamp']}")
                print(f"🐛 Errors: {', '.join(solution['errors'])}")

                try:
                    with open(solution['file'], 'r', encoding='utf-8') as f:
                        original_code = f.read()

                    # print(f"\n💡 AI EXPLANATION:")

                    self.display_diff(original_code, solution['corrected_code'], solution['file'])

                    print(f"\n🧠 AI ANALYSIS IN PROGRESS...")
                    ai_response = self.analyze_fix_with_ai(
                        solution['file'],
                        original_code,
                        solution['corrected_code'],
                        solution['errors']
                    )
                    # ai_analysis = self.parse_ai_decision(ai_response)
                    ai_analysis = []
                    for err in solution['errors']:
                        ai_resp = self.analyze_fix_with_ai(
                            solution['file'],
                            original_code,
                            solution['corrected_code'],
                            [err]  # wrap single error in list
                        )
                        parsed = self.parse_ai_decision(ai_resp)
                        parsed['related_error'] = err
                        ai_analysis.append(parsed)

                    print(f"\n🤖 AI DECISION PER ERROR:")
                    for analysis in ai_analysis:
                        print(f"   Error: {analysis.get('related_error', 'N/A')}")
                        print(f"   Decision: {analysis['decision']}")
                        print(f"   Risk Level: {analysis['risk_level']}")
                        print(f"   Confidence: {analysis['confidence']}%")
                        print(f"   Reasoning: {analysis['reasoning']}")
                        print(f"   For Detail view watch the filecard Below")
                        if analysis['safety_notes']:
                            print(f"   Safety Notes: {analysis['safety_notes']}")
                        print("-" * 40)


                    # Decision branch
                    if all(a['decision'] == 'APPLY' and a['confidence'] >= 70 for a in ai_analysis):
                        print(f"\n🚀 APPLYING FIX (AI Approved)...")
                        backup_path = self.create_backup(solution['file'])

                        if backup_path and self.apply_fix(solution['file'], solution['corrected_code']):
                            print(f"✅ SUCCESS! Fix applied automatically")
                            print(f"📋 Original backed up to: {backup_path}")

                            clean_solution_entry(solution, fix_status='applied_auto', was_applied=True)
                            self.save_to_fix_log(solution, ai_analysis)
                            self.update_error_log_status(solution['file'], 'fixed')
                            # Call the function to update process_flow.json
                            fix_id = self.save_to_fix_log(solution, ai_analysis)
                            if fix_id:
                                self.update_process_flow_with_fix(
                                    file_path=solution['file'],
                                    err_id=solution['err_id'],
                                    fix_id=fix_id,
                                    ai_analysis=ai_analysis
                                )



                        else:
                            print(f"❌ Fix application failed or backup failed")
                            clean_solution_entry(solution, fix_status='failed', was_applied=False)

                    elif ai_analysis['decision'] == 'SKIP':
                        print(f"\n⏭️  SKIPPING FIX (AI Recommendation)")
                        clean_solution_entry(solution, fix_status='skipped_ai', was_applied=False)

                    else:
                        print(f"\n⏸️  MANUAL REVIEW REQUIRED")
                        print(f"   Reason: {ai_analysis['reasoning']}")
                        clean_solution_entry(solution, fix_status='manual_review_required', was_applied=False)

                    with open('solutions.json', 'w') as f:
                        json.dump(solutions, f, indent=2)

                    self.processed_solutions.add(solution_id)

                except Exception as e:
                    print(f"❌ Error processing solution for {solution['file']}: {e}")
                    clean_solution_entry(solution, fix_status='error', was_applied=False)

                    with open('solutions.json', 'w') as f:
                        json.dump(solutions, f, indent=2)


    def show_statistics(self):
        """Show fix statistics"""
        solutions = self.load_solutions()
        
        if not solutions:
            print("📊 No solutions found")
            return
        
        applied_auto = sum(1 for s in solutions if s['status'] == 'applied_auto')
        skipped_ai = sum(1 for s in solutions if s['status'] == 'skipped_ai')
        manual_review = sum(1 for s in solutions if s['status'] == 'manual_review_required')
        pending = sum(1 for s in solutions if s['status'] == 'pending_review')
        failed = sum(1 for s in solutions if s['status'] == 'failed')
        
        print(f"\n📊 AI FIX STATISTICS:")
        print(f"   🤖 Auto-Applied: {applied_auto}")
        print(f"   ⏭️  AI Skipped: {skipped_ai}")
        print(f"   👤 Manual Review: {manual_review}")
        print(f"   ⏳ Pending: {pending}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Total: {len(solutions)}")
    
    def run(self):
        """Main AI fix processing loop"""
        print("🚀 Starting AI-powered fix processing...")
        print("🧠 AI will analyze each fix before applying")
        print("🔄 Monitoring for solutions from Solution Agent...")
        print("⚡ Safe fixes will be applied automatically")
        print("🛑 Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.process_solutions()
                time.sleep(3)  # Check every 3 seconds
                
        except KeyboardInterrupt:
            print("\n\n🛑 AI Fix Agent stopped by user")
            self.show_statistics()
            print("💾 All solutions and backups preserved")
            print("🤖 AI decisions logged for review")

if __name__ == "__main__":
    try:
        ai_fix_agent = AIFixAgent()
        ai_fix_agent.run()
    except Exception as e:
        print(f"❌ AI Fix Agent failed to start: {e}")
        print("💡 Make sure you have GEMINI_API_KEY in your .env file")