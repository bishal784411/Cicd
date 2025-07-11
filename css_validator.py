# """
# CSS Validator Module
# """

# import re


# class CSSValidator:
#     def __init__(self):
#         # Common CSS properties - basic dictionary for validation
#         self.valid_css_properties = {
#             'color', 'background', 'background-color', 'background-image', 'background-repeat',
#             'background-position', 'background-size', 'background-attachment', 'border',
#             'border-color', 'border-style', 'border-width', 'border-radius', 'margin',
#             'margin-top', 'margin-right', 'margin-bottom', 'margin-left', 'padding',
#             'padding-top', 'padding-right', 'padding-bottom', 'padding-left', 'width',
#             'height', 'max-width', 'max-height', 'min-width', 'min-height', 'display',
#             'position', 'top', 'right', 'bottom', 'left', 'float', 'clear', 'visibility',
#             'overflow', 'overflow-x', 'overflow-y', 'z-index', 'font', 'font-family',
#             'font-size', 'font-weight', 'font-style', 'font-variant', 'line-height',
#             'text-align', 'text-decoration', 'text-indent', 'text-transform', 'letter-spacing',
#             'word-spacing', 'white-space', 'vertical-align', 'list-style', 'list-style-type',
#             'list-style-position', 'list-style-image', 'table-layout', 'border-collapse',
#             'border-spacing', 'caption-side', 'empty-cells', 'cursor', 'outline',
#             'outline-color', 'outline-style', 'outline-width', 'box-shadow', 'text-shadow',
#             'opacity', 'filter', 'transform', 'transition', 'animation', 'flex', 'flex-direction',
#             'flex-wrap', 'justify-content', 'align-items', 'align-content', 'grid',
#             'grid-template-columns', 'grid-template-rows', 'grid-gap', 'gap', 'object-fit',
#             'object-position', 'resize', 'user-select', 'pointer-events', 'box-sizing'
#         }
        
#         # Font families that don't need quotes
#         self.system_fonts = {
#             'arial', 'helvetica', 'times', 'courier', 'verdana', 'georgia', 'palatino',
#             'garamond', 'bookman', 'trebuchet', 'arial black', 'impact', 'sans-serif',
#             'serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-serif',
#             'ui-sans-serif', 'ui-monospace', 'ui-rounded'
#         }

#     def validate(self, file_path):
#         """
#         Main validation method that checks CSS file for common issues.
        
#         Args:
#             file_path (str): Path to the CSS file to validate
            
#         Returns:
#             list: List of error messages found during validation
#         """
#         errors = []
#         try:
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 content = f.read()
            
#             # Remove comments to avoid false positives
#             content_no_comments = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            
#             # Check for unclosed braces
#             open_braces = content_no_comments.count('{')
#             close_braces = content_no_comments.count('}')
#             if open_braces != close_braces:
#                 errors.append(f"Mismatched braces: {open_braces} opening, {close_braces} closing")
            
#             # Check for missing semicolons (basic check)
#             lines = content.split('\n')
#             for i, line in enumerate(lines, 1):
#                 line = line.strip()
#                 if line and ':' in line and not line.endswith((';', '{', '}')) and not line.startswith(('/*', '*', '@')):
#                     errors.append(f"Missing semicolon on line {i}: {line}")
            
#             # Advanced validation checks
#             property_errors = self._check_property_names(content_no_comments)
#             errors.extend(property_errors)
            
#             value_errors = self._check_property_values(content_no_comments)
#             errors.extend(value_errors)
            
#             font_errors = self._check_font_family_quotes(content_no_comments)
#             errors.extend(font_errors)
            
#             color_errors = self._check_color_notations(content_no_comments)
#             errors.extend(color_errors)
            
#             class_errors = self._check_class_names(content_no_comments)
#             errors.extend(class_errors)
            
#             selector_errors = self._check_selector_ordering(content_no_comments)
#             errors.extend(selector_errors)
            
#         except Exception as e:
#             errors.append(f"CSS parsing error: {str(e)}")
        
#         return errors

#     def _check_property_names(self, content):
#         """Check for invalid CSS property names"""
#         errors = []
#         property_pattern = r'([a-zA-Z-]+)\s*:'
#         matches = re.finditer(property_pattern, content)
        
#         for match in matches:
#             prop_name = match.group(1).strip().lower()
#             if prop_name not in self.valid_css_properties:
#                 errors.append(f"Invalid or unknown property: '{prop_name}'")
        
#         return errors

#     def _check_property_values(self, content):
#         """Check for common invalid property values"""
#         errors = []
        
#         # Check for invalid display values
#         display_pattern = r'display\s*:\s*([^;]+);'
#         valid_display_values = {'block', 'inline', 'inline-block', 'flex', 'grid', 'none', 'table', 'table-cell', 'table-row'}
        
#         matches = re.finditer(display_pattern, content, re.IGNORECASE)
#         for match in matches:
#             value = match.group(1).strip().lower()
#             if value not in valid_display_values:
#                 errors.append(f"Invalid display value: '{value}'")
        
#         # Check for invalid position values
#         position_pattern = r'position\s*:\s*([^;]+);'
#         valid_position_values = {'static', 'relative', 'absolute', 'fixed', 'sticky'}
        
#         matches = re.finditer(position_pattern, content, re.IGNORECASE)
#         for match in matches:
#             value = match.group(1).strip().lower()
#             if value not in valid_position_values:
#                 errors.append(f"Invalid position value: '{value}'")
        
#         # Check for invalid color values (basic check)
#         color_pattern = r'color\s*:\s*([^;]+);'
#         matches = re.finditer(color_pattern, content, re.IGNORECASE)
#         for match in matches:
#             value = match.group(1).strip()
#             if not self._is_valid_color(value):
#                 errors.append(f"Invalid color value: '{value}'")
        
#         return errors

#     def _is_valid_color(self, color_value):
#         """Basic color validation"""
#         color_value = color_value.strip().lower()
        
#         # Named colors (basic set)
#         named_colors = {'red', 'green', 'blue', 'black', 'white', 'yellow', 'cyan', 'magenta', 'transparent'}
#         if color_value in named_colors:
#             return True
        
#         # Hex colors
#         if re.match(r'^#([0-9a-f]{3}|[0-9a-f]{6})$', color_value):
#             return True
        
#         # RGB/RGBA
#         if re.match(r'^rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*(,\s*[\d.]+\s*)?\)$', color_value):
#             return True
        
#         # HSL/HSLA
#         if re.match(r'^hsla?\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%\s*(,\s*[\d.]+\s*)?\)$', color_value):
#             return True
        
#         return False

#     def _check_font_family_quotes(self, content):
#         """Check for unnecessary quotes around font-family names"""
#         errors = []
        
#         font_pattern = r'font-family\s*:\s*([^;]+);'
#         matches = re.finditer(font_pattern, content, re.IGNORECASE)
        
#         for match in matches:
#             font_value = match.group(1).strip()
#             fonts = [f.strip() for f in font_value.split(',')]
            
#             for font in fonts:
#                 if (font.startswith('"') and font.endswith('"')) or (font.startswith("'") and font.endswith("'")):
#                     font_name = font[1:-1].lower()
#                     if font_name in self.system_fonts:
#                         errors.append(f"Unnecessary quotes around system font: {font}")
        
#         return errors

#     def _check_color_notations(self, content):
#         """Check for deprecated rgba() usage and invalid color notations"""
#         errors = []
        
#         # Check for rgba() with alpha = 1 (could use rgb() instead)
#         rgba_pattern = r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*1(\.0*)?\s*\)'
#         matches = re.finditer(rgba_pattern, content, re.IGNORECASE)
        
#         for match in matches:
#             errors.append(f"Deprecated: rgba() with alpha=1 should use rgb(): {match.group(0)}")
        
#         # Check for invalid hex colors (wrong length)
#         hex_pattern = r'#([0-9a-f]+)'
#         matches = re.finditer(hex_pattern, content, re.IGNORECASE)
        
#         for match in matches:
#             hex_value = match.group(1)
#             if len(hex_value) not in [3, 6]:
#                 errors.append(f"Invalid hex color length: #{hex_value}")
        
#         return errors

#     def _check_class_names(self, content):
#         """Check if class names follow kebab-case convention"""
#         errors = []
        
#         class_pattern = r'\.([a-zA-Z][a-zA-Z0-9_-]*)'
#         matches = re.finditer(class_pattern, content)
        
#         for match in matches:
#             class_name = match.group(1)
#             if not re.match(r'^[a-z][a-z0-9-]*$', class_name):
#                 errors.append(f"Class name doesn't follow kebab-case: '.{class_name}'")
        
#         return errors

#     def _check_selector_ordering(self, content):
#         """Basic check for selector ordering issues"""
#         errors = []
        
#         selector_pattern = r'([^{]+)\s*{'
#         matches = list(re.finditer(selector_pattern, content))
        
#         prev_specificity = 0
#         for match in matches:
#             selector = match.group(1).strip()
#             specificity = self._calculate_basic_specificity(selector)
            
#             if specificity < prev_specificity and specificity == 1:
#                 errors.append(f"Possible selector ordering issue: general selector '{selector}' after more specific selectors")
            
#             prev_specificity = max(prev_specificity, specificity)
        
#         return errors

#     def _calculate_basic_specificity(self, selector):
#         """Calculate very basic CSS specificity score"""
#         score = 0
        
#         # Count IDs
#         score += selector.count('#') * 100
        
#         # Count classes and attributes
#         score += selector.count('.') * 10
#         score += selector.count('[') * 10
        
#         # Count elements
#         elements = re.findall(r'\b[a-z]+\b', selector)
#         score += len([e for e in elements if not e.startswith(':')])
        
#         return score


# # Convenience function for direct usage
# def validate_css_file(file_path):
#     """
#     Convenience function to validate a CSS file.
    
#     Args:
#         file_path (str): Path to the CSS file to validate
        
#     Returns:
#         list: List of error messages found during validation
#     """
#     validator = CSSValidator()
#     return validator.validate(file_path)


# # Example usage
# if __name__ == "__main__":
#     # Test the validator
#     errors = validate_css_file('Hotel-demo/styles.css')
    
#     if errors:
#         print("CSS Validation Errors:")
#         for error in errors:
#             print(f"  - {error}")
#     else:
#         print("CSS validation passed!")
