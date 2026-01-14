import os
import re

def fix_plotly_dicts(filepath):
    """Fix all dict() calls in Plotly code to use {} syntax"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'plotly' not in content.lower():
        return False
    
    original_content = content
    
    # Fix common patterns
    patterns = [
        (r'margin=dict\(l=(\d+),\s*r=(\d+),\s*t=(\d+),\s*b=(\d+)\)', r'margin={"l": \1, "r": \2, "t": \3, "b": \4}'),
        (r'font=dict\(color="([^"]+)"\)', r'font={"color": "\1"}'),
        (r'line=dict\(color="([^"]+)",\s*width=(\d+)\)', r'line={"color": "\1", "width": \2}'),
        (r'line=dict\(([^)]+)\)', r'line={\1}'),
        (r'marker=dict\(([^)]+)\)', r'marker={\1}'),
        (r'xaxis=dict\(title="([^"]*)"\)', r'xaxis={"title": "\1"}'),
        (r'yaxis=dict\(title="([^"]*)"\)', r'yaxis={"title": "\1"}'),
        (r'legend=dict\(([^)]+)\)', r'legend={\1}'),
        (r'tickfont=dict\([^)]+\),?\s*', r''),
        (r'titlefont=dict\([^)]+\),?\s*', r''),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Fix all Python files in current directory
fixed_files = []
current_dir = os.getcwd()
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != 'fix_all_plotly.py':
        filepath = os.path.join(current_dir, filename)
        if os.path.isfile(filepath):
            if fix_plotly_dicts(filepath):
                fixed_files.append(filename)
                print(f"✓ Fixed {filename}")

if fixed_files:
    print(f"\nFixed {len(fixed_files)} file(s): {', '.join(fixed_files)}")
    print("\nPlease review the changes and commit them:")
    print("  git add *.py")
    print('  git commit -m "Fix all Plotly dict() syntax issues"')
    print("  git pull --rebase origin main")
    print("  git push origin main")
else:
    print("No files needed fixing.")
