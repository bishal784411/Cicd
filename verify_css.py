# import subprocess
# import json

# file_path = "Hotel-demo/styles.css"

# def validate_css_with_stylelint(self, file_path):
#     """Use Stylelint to validate a CSS file and return errors"""
#     try:
#         result = subprocess.run(
#             ["npx", "stylelint", file_path, "--formatter", "json"],
#             capture_output=True, text=True, check=False
#         )
#         if result.returncode == 0:
#             return []  # No errors
#         else:
#             import json
#             lint_results = json.loads(result.stdout)
#             errors = []
#             for issue in lint_results:
#                 for warning in issue.get("warnings", []):
#                     errors.append(f"Line {warning['line']}, Col {warning['column']}: {warning['text']}")
#             return errors
#     except Exception as e:
#         return [f"Stylelint error: {str(e)}"]
