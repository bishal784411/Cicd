# import os
# import time
# import json
# import shutil
# from datetime import datetime
# from pathlib import Path
# from dotenv import load_dotenv
# import difflib

# # Load environment variables
# load_dotenv()

# class FixAgent:
#     def __init__(self):
#         self.processed_solutions = set()
#         self.backup_dir = Path("backups")
#         self.backup_dir.mkdir(exist_ok=True)
        
#         print("🔧 Fix Agent initialized")
#         print("📁 Backup directory: ./backups")
#         print("=" * 60)
    
#     def load_solutions(self):
#         """Load solutions from Solution Agent"""
#         try:
#             if os.path.exists('solutions.json'):
#                 with open('solutions.json', 'r') as f:
#                     return json.load(f)
#             return []
#         except Exception as e:
#             print(f"❌ Error loading solutions: {e}")
#             return []
    
#     def create_backup(self, file_path):
#         """Create backup of original file"""
#         try:
#             file_path = Path(file_path)
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
#             backup_path = self.backup_dir / backup_name
            
#             shutil.copy2(file_path, backup_path)
#             print(f"📋 Backup created: {backup_path}")
#             return backup_path
            
#         except Exception as e:
#             print(f"❌ Backup creation failed: {e}")
#             return None
    
#     def display_diff(self, original_code, fixed_code, file_path):
#         """Display side-by-side comparison of original and fixed code"""
#         print("\n" + "=" * 100)
#         print(f"📄 FILE: {file_path}")
#         print("=" * 100)
        
#         # Create unified diff
#         diff = list(difflib.unified_diff(
#             original_code.splitlines(keepends=True),
#             fixed_code.splitlines(keepends=True),
#             fromfile=f"Original: {file_path}",
#             tofile=f"Fixed: {file_path}",
#             lineterm=''
#         ))
        
#         if diff:
#             print("\n🔍 CHANGES DETECTED:")
#             print("-" * 60)
            
#             for line in diff:
#                 if line.startswith('---') or line.startswith('+++'):
#                     print(f"📁 {line.strip()}")
#                 elif line.startswith('@@'):
#                     print(f"📍 {line.strip()}")
#                 elif line.startswith('-'):
#                     print(f"❌ {line.rstrip()}")
#                 elif line.startswith('+'):
#                     print(f"✅ {line.rstrip()}")
#                 elif line.startswith(' '):
#                     print(f"   {line.rstrip()}")
            
#             print("-" * 60)
#         else:
#             print("\n⚠️  No differences detected")
    
#     def display_side_by_side(self, original_code, fixed_code, file_path):
#         """Display side-by-side comparison"""
#         print("\n" + "=" * 120)
#         print(f"📄 FILE: {file_path}")
#         print("=" * 120)
        
#         original_lines = original_code.split('\n')
#         fixed_lines = fixed_code.split('\n')
        
#         max_lines = max(len(original_lines), len(fixed_lines))
        
#         # Pad shorter list with empty strings
#         while len(original_lines) < max_lines:
#             original_lines.append('')
#         while len(fixed_lines) < max_lines:
#             fixed_lines.append('')
        
#         print(f"{'ORIGINAL CODE':<58} | {'FIXED CODE':<58}")
#         print("-" * 58 + " | " + "-" * 58)
        
#         for i in range(min(max_lines, 30)):  # Show first 30 lines
#             orig_line = original_lines[i][:55] + "..." if len(original_lines[i]) > 55 else original_lines[i]
#             fixed_line = fixed_lines[i][:55] + "..." if len(fixed_lines[i]) > 55 else fixed_lines[i]
            
#             # Highlight differences
#             if orig_line != fixed_line:
#                 print(f"❌ {orig_line:<55} | ✅ {fixed_line:<55}")
#             else:
#                 print(f"   {orig_line:<55} |    {fixed_line:<55}")
        
#         if max_lines > 30:
#             print(f"... ({max_lines - 30} more lines)")
        
#         print("=" * 120)
    
#     def apply_fix(self, file_path, fixed_code):
#         """Apply the fix to the file"""
#         try:
#             with open(file_path, 'w', encoding='utf-8') as f:
#                 f.write(fixed_code)
#             print(f"✅ Fix applied successfully to: {file_path}")
#             return True
#         except Exception as e:
#             print(f"❌ Failed to apply fix: {e}")
#             return False
    
#     def update_solution_status(self, solution_index, status):
#         """Update solution status in JSON file"""
#         try:
#             solutions = self.load_solutions()
#             if solution_index < len(solutions):
#                 solutions[solution_index]['status'] = status
#                 solutions[solution_index]['applied_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
#                 with open('solutions.json', 'w') as f:
#                     json.dump(solutions, f, indent=2)
#                 return True
#         except Exception as e:
#             print(f"❌ Error updating solution status: {e}")
#         return False
    
#     def process_solutions(self):
#         """Process pending solutions"""
#         solutions = self.load_solutions()
        
#         for i, solution in enumerate(solutions):
#             solution_id = f"{solution['file']}_{solution['timestamp']}"
            
#             if solution_id not in self.processed_solutions and solution['status'] == 'pending_review':
#                 print(f"\n🔍 NEW SOLUTION AVAILABLE")
#                 print(f"📄 File: {solution['file']}")
#                 print(f"⏰ Generated: {solution['timestamp']}")
#                 print(f"🐛 Errors: {', '.join(solution['errors'])}")
                
#                 # Read current file
#                 try:
#                     with open(solution['file'], 'r', encoding='utf-8') as f:
#                         original_code = f.read()
                    
#                     # Display explanation
#                     print(f"\n💡 EXPLANATION:")
#                     print(f"   {solution['explanation']}")
                    
#                     if solution['recommendations']:
#                         print(f"\n🎯 RECOMMENDATIONS:")
#                         print(f"   {solution['recommendations']}")
                    
#                     # Display code comparison
#                     print(f"\n📊 CODE COMPARISON:")
#                     self.display_diff(original_code, solution['corrected_code'], solution['file'])
                    
#                     # Ask for user confirmation
#                     print(f"\n🤔 APPLY THIS FIX?")
#                     print(f"   Original file will be backed up automatically")
#                     print(f"   Type 'Y' to apply, 'N' to skip, 'S' to show side-by-side view")
                    
#                     while True:
#                         choice = input("👉 Your choice [Y/N/S]: ").strip().upper()
                        
#                         if choice == 'Y':
#                             # Create backup
#                             backup_path = self.create_backup(solution['file'])
#                             if backup_path:
#                                 # Apply fix
#                                 if self.apply_fix(solution['file'], solution['corrected_code']):
#                                     print(f"🎉 SUCCESS! Fix applied and backed up.")
#                                     self.update_solution_status(i, 'applied')
#                                 else:
#                                     print(f"❌ Fix application failed!")
#                                     self.update_solution_status(i, 'failed')
#                             else:
#                                 print(f"❌ Backup failed, fix not applied for safety!")
#                             break
                            
#                         elif choice == 'N':
#                             print(f"⏭️  Fix skipped")
#                             self.update_solution_status(i, 'skipped')
#                             break
                            
#                         elif choice == 'S':
#                             print(f"\n📱 SIDE-BY-SIDE VIEW:")
#                             self.display_side_by_side(original_code, solution['corrected_code'], solution['file'])
#                             print(f"\n🤔 APPLY THIS FIX?")
#                             print(f"   Type 'Y' to apply, 'N' to skip")
#                             continue
                            
#                         else:
#                             print(f"❌ Invalid choice. Please enter Y, N, or S")
                    
#                     self.processed_solutions.add(solution_id)
                    
#                 except Exception as e:
#                     print(f"❌ Error processing solution for {solution['file']}: {e}")
#                     self.update_solution_status(i, 'error')
    
#     def show_statistics(self):
#         """Show fix statistics"""
#         solutions = self.load_solutions()
        
#         if not solutions:
#             return
        
#         applied = sum(1 for s in solutions if s['status'] == 'applied')
#         skipped = sum(1 for s in solutions if s['status'] == 'skipped')
#         pending = sum(1 for s in solutions if s['status'] == 'pending_review')
#         failed = sum(1 for s in solutions if s['status'] == 'failed')
        
#         print(f"\n📊 FIX STATISTICS:")
#         print(f"   ✅ Applied: {applied}")
#         print(f"   ⏭️  Skipped: {skipped}")
#         print(f"   ⏳ Pending: {pending}")
#         print(f"   ❌ Failed: {failed}")
#         print(f"   📁 Total: {len(solutions)}")
    
#     def list_backups(self):
#         """List all available backups"""
#         backups = list(self.backup_dir.glob("*"))
#         if backups:
#             print(f"\n📋 AVAILABLE BACKUPS:")
#             for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
#                 mtime = datetime.fromtimestamp(backup.stat().st_mtime)
#                 print(f"   • {backup.name} (Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
#         else:
#             print(f"\n📋 No backups found")
    
#     def restore_backup(self, backup_name, target_file):
#         """Restore a backup file"""
#         try:
#             backup_path = self.backup_dir / backup_name
#             if backup_path.exists():
#                 shutil.copy2(backup_path, target_file)
#                 print(f"✅ Restored {backup_name} to {target_file}")
#                 return True
#             else:
#                 print(f"❌ Backup {backup_name} not found")
#                 return False
#         except Exception as e:
#             print(f"❌ Restore failed: {e}")
#             return False
    
#     def interactive_menu(self):
#         """Interactive menu for additional operations"""
#         print(f"\n🎛️  INTERACTIVE MENU:")
#         print(f"   1. Show statistics")
#         print(f"   2. List backups")
#         print(f"   3. Restore backup")
#         print(f"   4. Continue monitoring")
#         print(f"   5. Exit")
        
#         choice = input("👉 Select option [1-5]: ").strip()
        
#         if choice == '1':
#             self.show_statistics()
#         elif choice == '2':
#             self.list_backups()
#         elif choice == '3':
#             self.list_backups()
#             backup_name = input("Enter backup filename: ").strip()
#             target_file = input("Enter target file path: ").strip()
#             if backup_name and target_file:
#                 self.restore_backup(backup_name, target_file)
#         elif choice == '4':
#             return True
#         elif choice == '5':
#             return False
#         else:
#             print("❌ Invalid choice")
        
#         return self.interactive_menu()
    
#     def run(self):
#         """Main fix processing loop"""
#         print("🚀 Starting fix processing...")
#         print("🔄 Waiting for solutions from Solution Agent...")
#         print("🎛️  Press Ctrl+C for interactive menu\n")
        
#         try:
#             while True:
#                 self.process_solutions()
#                 time.sleep(3)  # Check every 3 seconds
                
#         except KeyboardInterrupt:
#             print("\n\n🎛️  Interactive mode activated")
            
#             try:
#                 continue_monitoring = self.interactive_menu()
#                 if continue_monitoring:
#                     print("\n🔄 Resuming monitoring...")
#                     self.run()
#                 else:
#                     print("\n🛑 Fix Agent stopped by user")
#                     self.show_statistics()
#                     print("💾 All solutions and backups preserved")
#             except KeyboardInterrupt:
#                 print("\n\n🛑 Fix Agent stopped by user")
#                 self.show_statistics()
#                 print("💾 All solutions and backups preserved")

# if __name__ == "__main__":
#     try:
#         fix_agent = FixAgent()
#         fix_agent.run()
#     except Exception as e:
#         print(f"❌ Fix Agent failed to start: {e}")
#         print("💡 Make sure the solutions.json file is accessible")

import os
import time
import json
import shutil
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import difflib

# Load environment variables
load_dotenv()

class FixAgent:
    def __init__(self):
        self.processed_solutions = set()
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
        
        print("🔧 Fix Agent initialized")
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
    
    def display_diff(self, original_code, fixed_code, file_path):
        """Display side-by-side comparison of original and fixed code"""
        print("\n" + "=" * 100)
        print(f"📄 FILE: {file_path}")
        print("=" * 100)
        
        # Create unified diff
        diff = list(difflib.unified_diff(
            original_code.splitlines(keepends=True),
            fixed_code.splitlines(keepends=True),
            fromfile=f"Original: {file_path}",
            tofile=f"Fixed: {file_path}",
            lineterm=''
        ))
        
        if diff:
            print("\n🔍 CHANGES DETECTED:")
            print("-" * 60)
            
            for line in diff:
                if line.startswith('---') or line.startswith('+++'):
                    print(f"📁 {line.strip()}")
                elif line.startswith('@@'):
                    print(f"📍 {line.strip()}")
                elif line.startswith('-'):
                    print(f"❌ {line.rstrip()}")
                elif line.startswith('+'):
                    print(f"✅ {line.rstrip()}")
                elif line.startswith(' '):
                    print(f"   {line.rstrip()}")
            
            print("-" * 60)
        else:
            print("\n⚠️  No differences detected")
    
    def display_side_by_side(self, original_code, fixed_code, file_path):
        """Display side-by-side comparison"""
        print("\n" + "=" * 120)
        print(f"📄 FILE: {file_path}")
        print("=" * 120)
        
        original_lines = original_code.split('\n')
        fixed_lines = fixed_code.split('\n')
        
        max_lines = max(len(original_lines), len(fixed_lines))
        
        # Pad shorter list with empty strings
        while len(original_lines) < max_lines:
            original_lines.append('')
        while len(fixed_lines) < max_lines:
            fixed_lines.append('')
        
        print(f"{'ORIGINAL CODE':<58} | {'FIXED CODE':<58}")
        print("-" * 58 + " | " + "-" * 58)
        
        for i in range(min(max_lines, 30)):  # Show first 30 lines
            orig_line = original_lines[i][:55] + "..." if len(original_lines[i]) > 55 else original_lines[i]
            fixed_line = fixed_lines[i][:55] + "..." if len(fixed_lines[i]) > 55 else fixed_lines[i]
            
            # Highlight differences
            if orig_line != fixed_line:
                print(f"❌ {orig_line:<55} | ✅ {fixed_line:<55}")
            else:
                print(f"   {orig_line:<55} |    {fixed_line:<55}")
        
        if max_lines > 30:
            print(f"... ({max_lines - 30} more lines)")
        
        print("=" * 120)
    
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
    
    def update_error_log_status(self, file_path, status):
        """Update error log status when fix is applied"""
        try:
            if os.path.exists('error_log.json'):
                with open('error_log.json', 'r') as f:
                    error_log = json.load(f)
                
                # Update all pending errors for this file
                for error_entry in error_log:
                    if error_entry['file'] == file_path and error_entry['status'] == 'detected':
                        error_entry['status'] = status
                        error_entry['fixed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open('error_log.json', 'w') as f:
                    json.dump(error_log, f, indent=2)
                
                print(f"📝 Error log updated: {file_path} marked as {status}")
                
        except Exception as e:
            print(f"❌ Error updating error log: {e}")
    
    def update_solution_status(self, solution_index, status):
        """Update solution status in JSON file"""
        try:
            solutions = self.load_solutions()
            if solution_index < len(solutions):
                solutions[solution_index]['status'] = status
                solutions[solution_index]['applied_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open('solutions.json', 'w') as f:
                    json.dump(solutions, f, indent=2)
                return True
        except Exception as e:
            print(f"❌ Error updating solution status: {e}")
        return False
    
    def process_solutions(self):
        """Process pending solutions and automatically apply fixes"""
        solutions = self.load_solutions()
        
        for i, solution in enumerate(solutions):
            solution_id = f"{solution['file']}_{solution['timestamp']}"
            
            if solution_id not in self.processed_solutions and solution['status'] == 'pending_review':
                print(f"\n🔍 PROCESSING SOLUTION")
                print(f"📄 File: {solution['file']}")
                print(f"⏰ Generated: {solution['timestamp']}")
                print(f"🐛 Errors: {', '.join(solution['errors'])}")
                
                # Read current file
                try:
                    with open(solution['file'], 'r', encoding='utf-8') as f:
                        original_code = f.read()
                    
                    # Display explanation
                    print(f"\n💡 AI EXPLANATION:")
                    print(f"   {solution['explanation']}")
                    
                    if solution['recommendations']:
                        print(f"\n🎯 RECOMMENDATIONS:")
                        print(f"   {solution['recommendations']}")
                    
                    # Display code comparison
                    print(f"\n📊 CODE CHANGES:")
                    self.display_diff(original_code, solution['corrected_code'], solution['file'])
                    
                    # Create backup automatically
                    print(f"\n🔄 APPLYING FIX...")
                    backup_path = self.create_backup(solution['file'])
                    
                    if backup_path:
                        # Apply fix automatically
                        if self.apply_fix(solution['file'], solution['corrected_code']):
                            print(f"✅ SUCCESS! Fix applied automatically")
                            print(f"📋 Original backed up to: {backup_path}")
                            # self.update_solution_status(i, 'applied')
                            solution['status'] = 'applied'
                            solution['applied_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # Save this solution to fix_log.json
                            self.save_to_fix_log(solution)

                            
                            # Update error log to mark as fixed
                            self.update_error_log_status(solution['file'], 'fixed')
                        else:
                            print(f"❌ Fix application failed!")
                            self.update_solution_status(i, 'failed')
                    else:
                        print(f"❌ Backup failed, fix not applied for safety!")
                        self.update_solution_status(i, 'failed')
                    
                    self.processed_solutions.add(solution_id)
                    
                except Exception as e:
                    print(f"❌ Error processing solution for {solution['file']}: {e}")
                    self.update_solution_status(i, 'error')
    def save_to_fix_log(self, solution):
        """Append applied solution to fix_log.json"""
        try:
            fix_log_path = Path("fix_log.json")
            fix_log = []

            if fix_log_path.exists():
                with open(fix_log_path, 'r') as f:
                    fix_log = json.load(f)

            solution_copy = dict(solution)
            solution_copy.pop('corrected_code', None)
            if 'changes' in solution and 'summary' in solution_copy['changes']:
                solution_copy['changes']['summary'].pop('diff_text', None)

            fix_log.append(solution_copy)

            with open(fix_log_path, 'w') as f:
                json.dump(fix_log, f, indent=2)

            print("📦 Fix saved to fix_log.json")
            return True

        except Exception as e:
            print(f"❌ Failed to save to fix_log.json: {e}")
            return False

    
    def show_statistics(self):
        """Show fix statistics"""
        solutions = self.load_solutions()
        
        if not solutions:
            return
        
        applied = sum(1 for s in solutions if s['status'] == 'applied')
        skipped = sum(1 for s in solutions if s['status'] == 'skipped')
        pending = sum(1 for s in solutions if s['status'] == 'pending_review')
        failed = sum(1 for s in solutions if s['status'] == 'failed')
        
        print(f"\n📊 FIX STATISTICS:")
        print(f"   ✅ Applied: {applied}")
        print(f"   ⏭️  Skipped: {skipped}")
        print(f"   ⏳ Pending: {pending}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📁 Total: {len(solutions)}")
    
    def list_backups(self):
        """List all available backups"""
        backups = list(self.backup_dir.glob("*"))
        if backups:
            print(f"\n📋 AVAILABLE BACKUPS:")
            for backup in sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True):
                mtime = datetime.fromtimestamp(backup.stat().st_mtime)
                print(f"   • {backup.name} (Created: {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
        else:
            print(f"\n📋 No backups found")
    
    def restore_backup(self, backup_name, target_file):
        """Restore a backup file"""
        try:
            backup_path = self.backup_dir / backup_name
            if backup_path.exists():
                shutil.copy2(backup_path, target_file)
                print(f"✅ Restored {backup_name} to {target_file}")
                return True
            else:
                print(f"❌ Backup {backup_name} not found")
                return False
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def interactive_menu(self):
        """Interactive menu for additional operations"""
        print(f"\n🎛️  INTERACTIVE MENU:")
        print(f"   1. Show statistics")
        print(f"   2. List backups")
        print(f"   3. Restore backup")
        print(f"   4. Continue monitoring")
        print(f"   5. Exit")
        
        choice = input("👉 Select option [1-5]: ").strip()
        
        if choice == '1':
            self.show_statistics()
        elif choice == '2':
            self.list_backups()
        elif choice == '3':
            self.list_backups()
            backup_name = input("Enter backup filename: ").strip()
            target_file = input("Enter target file path: ").strip()
            if backup_name and target_file:
                self.restore_backup(backup_name, target_file)
        elif choice == '4':
            return True
        elif choice == '5':
            return False
        else:
            print("❌ Invalid choice")
        
        return self.interactive_menu()
    
    def run(self):
        """Main fix processing loop"""
        print("🚀 Starting automatic fix processing...")
        print("🔄 Monitoring for solutions from Solution Agent...")
        print("⚡ Fixes will be applied automatically with backup creation")
        print("🎛️  Press Ctrl+C for interactive menu\n")
        
        try:
            while True:
                self.process_solutions()
                time.sleep(2)  # Check every 2 seconds for faster response
                
        except KeyboardInterrupt:
            print("\n\n🎛️  Interactive mode activated")
            
            try:
                continue_monitoring = self.interactive_menu()
                if continue_monitoring:
                    print("\n🔄 Resuming automatic fix processing...")
                    self.run()
                else:
                    print("\n🛑 Fix Agent stopped by user")
                    self.show_statistics()
                    print("💾 All solutions and backups preserved")
            except KeyboardInterrupt:
                print("\n\n🛑 Fix Agent stopped by user")
                self.show_statistics()
                print("💾 All solutions and backups preserved")

if __name__ == "__main__":
    try:
        fix_agent = FixAgent()
        fix_agent.run()
    except Exception as e:
        print(f"❌ Fix Agent failed to start: {e}")
        print("💡 Make sure the solutions.json file is accessible")