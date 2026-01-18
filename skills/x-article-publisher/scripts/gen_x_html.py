#!/usr/bin/env python3
"""生成 X Article HTML 并复制到剪贴板"""

import sys
import os
import subprocess
import time

# Ensure we can import from the script directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from copy_to_clipboard import copy_html_to_clipboard_windows
    from parse_html_style import process_file
except ImportError:
    # If running from root, try adding scripts/ path
    sys.path.append(os.path.join(current_dir, 'scripts'))
    try:
        from copy_to_clipboard import copy_html_to_clipboard_windows
        from parse_html_style import process_file
    except ImportError:
        # Fallback for dev environment structure
        sys.path.append(r'c:\dev\tdx_plugin\x-article-publisher-skill\skills\x-article-publisher\scripts')
        try:
             from copy_to_clipboard import copy_html_to_clipboard_windows
             # We need to ensure parse_html_style is also there or in current dir
             # If I just created it in C:\Users\..., it might not be in c:\dev\tdx_plugin\scripts
             # I created it in C:\Users\ys-ro\.gemini\antigravity\skills\x-article-publisher\scripts\parse_html_style.py
             # I should probably copy it to c:\dev\tdx_plugin\scripts as well to be safe.
             from parse_html_style import process_file
        except ImportError:
             print("Error: Could not import required modules. Make sure parse_html_style.py is present.")
             # Temporary fix to allow running if file is in the same folder as this script
             try:
                 import parse_html_style
                 process_file = parse_html_style.process_file
             except:
                 sys.exit(1)

def generate_x_html(md_file):
    if not os.path.exists(md_file):
        print(f"Error: File not found: {md_file}")
        return

    # 1. Output file path
    html_file = md_file.rsplit('.', 1)[0] + '_x.html'
    
    print(f"Converting {md_file} to HTML using Pandoc...")
    
    # 2. Run Pandoc
    # -f markdown -t html (standard)
    try:
        cmd = ['pandoc', md_file, '-f', 'markdown', '-t', 'html', '-o', html_file]
        subprocess.run(cmd, check=True, capture_output=True)
        print("Pandoc conversion successful.")
    except subprocess.CalledProcessError as e:
        print(f"Pandoc execution failed: {e}")
        return
    except FileNotFoundError:
        print("Error: Pandoc not found. Please ensure pandoc is installed and in PATH.")
        return

    # 3. Post-process HTML (Styles, Code Blocks)
    print("Injecting styles and fixing code blocks...")
    # Ensure we use the process_file we imported
    if process_file(html_file):
        print("Style injection successful.")
    else:
        print("Style injection failed.")
        return

    # 4. Read content
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading generated HTML: {e}")
        return

    # 5. Copy to clipboard
    if copy_html_to_clipboard_windows(html_content):
        print(f"Success! HTML content copied to clipboard.")
        print(f"HTML file saved to: {html_file}")
    else:
        print("Failed to copy to clipboard.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gen_x_html.py <markdown_file>")
        # Default for testing
        default_file = r'c:\dev\tdx_plugin\哈尔滨电机厂招商引资分析.md'
        if os.path.exists(default_file):
            print(f"Using default file: {default_file}")
            generate_x_html(default_file)
    else:
        generate_x_html(sys.argv[1])
