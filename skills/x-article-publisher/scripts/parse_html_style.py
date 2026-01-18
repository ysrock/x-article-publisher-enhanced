
from bs4 import BeautifulSoup
import re
import sys

def process_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Process Tables
    # Style reference: 
    # table { border-collapse: collapse; width: 100%; border: 1px solid #000; margin-bottom: 1em; }
    # th, td { border: 1px solid #000; padding: 8px; vertical-align: top; }
    # th { background-color: #f2f2f2; font-weight: bold; text-align: left; }
    
    for table in soup.find_all('table'):
        table['style'] = "border-collapse: collapse; width: 100%; border: 1px solid #000; margin-bottom: 1em; font-family: sans-serif;"
        
        # Process Headers
        for th in table.find_all('th'):
            # Merge existing style if any
            existing_style = th.get('style', '')
            new_style = "border: 1px solid #000; padding: 8px; vertical-align: top; background-color: #f2f2f2; font-weight: bold; text-align: left;"
            th['style'] = f"{existing_style}; {new_style}" if existing_style else new_style
            
        # Process Cells
        for td in table.find_all('td'):
            existing_style = td.get('style', '')
            new_style = "border: 1px solid #000; padding: 8px; vertical-align: top;"
            td['style'] = f"{existing_style}; {new_style}" if existing_style else new_style

    # 2. Process Code Blocks (Pandoc structure)
    # Pandoc: <div class="sourceCode" id="cbX"><pre class="sourceCode python"><code ...>...</code></pre></div>
    # Target: <p><strong>language</strong></p><blockquote><pre><code class="language-python">...</code></pre></blockquote>
    
    for div in soup.find_all('div', class_='sourceCode'):
        pre = div.find('pre')
        code = div.find('code')
        
        if not pre or not code:
            continue
            
        # Get language from classes
        # Classes are usually ['sourceCode', 'python'] or similar
        classes = pre.get('class', []) + code.get('class', [])
        language = ''
        for cls in classes:
            if cls != 'sourceCode' and not cls.startswith('sourceCode'):
                language = cls
                break
        
        # Extract Text Content (strip generated spans to get clean code)
        code_text = code.get_text()
        
        # Clean up whitespace? Usually code blocks should preserve it. 
        # But Pandoc might output clean text.
        
        # Create new structure
        new_container = soup.new_tag('div')
        
        # 2.1 Language Label
        if language:
             p_label = soup.new_tag('p')
             strong_label = soup.new_tag('strong')
             strong_label.string = language
             p_label.append(strong_label)
             new_container.append(p_label)
        
        # 2.2 Blockquote / Pre / Code
        blockquote = soup.new_tag('blockquote')
        pre_tag = soup.new_tag('pre')
        code_tag = soup.new_tag('code')
        
        if language:
             code_tag['class'] = f"language-{language}"
        
        code_tag.string = code_text # Handles escaping
        
        pre_tag.append(code_tag)
        blockquote.append(pre_tag)
        new_container.append(blockquote)
        
        div.replace_with(new_container)

    # 3. Process H4-H6 (Convert to Bold Paragraphs)
    # Pandoc keeps them as h4-h6. X Article may not prefer them.
    for tag_name in ['h4', 'h5', 'h6']:
        for tag in soup.find_all(tag_name):
            new_tag = soup.new_tag('p')
            strong = soup.new_tag('strong')
            # Move content
            strong.extend(tag.contents)  # Keep inner tags like links/bold
            new_tag.append(strong)
            tag.replace_with(new_tag)

    return str(soup)

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = process_html_content(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Successfully processed {filepath}")
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
    else:
        print("Usage: python parse_html_style.py <html_file>")
