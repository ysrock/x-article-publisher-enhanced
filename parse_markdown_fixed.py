#!/usr/bin/env python3
"""
增强版 Markdown 解析器，专为 X Article 优化
解决原版的列表、表格、行内代码等问题
"""

import re
import os
import json
import sys
from pathlib import Path


def parse_markdown_for_x(markdown: str, base_path: Path = None) -> dict:
    """解析 Markdown 为 X Article 格式"""
    
    # 提取标题
    title = "Untitled"
    lines = markdown.strip().split('\n')
    content_start = 0
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('# '):
            title = stripped[2:].strip()
            content_start = idx + 1
            break
    
    # 移除标题行
    content = '\n'.join(lines[content_start:])
    
    # 转换为 HTML
    html = markdown_to_html_enhanced(content)
    
    return {
        "title": title,
        "cover_image": None,
        "content_images": [],
        "html": html,
        "total_blocks": content.count('\n\n') + 1,
    }


def markdown_to_html_enhanced(markdown: str) -> str:
    """增强版 Markdown 转 HTML"""
    
    # 按块处理
    blocks = split_markdown_blocks(markdown)
    html_blocks = []
    
    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # 水平分隔线
        if block == '---' or block == '***' or block == '___':
            html_blocks.append('<hr/>')
            continue
        
        # 代码块
        if block.startswith('```'):
            code_content = extract_code_block(block)
            # X Article 不支持 <pre><code>，用 blockquote 替代
            escaped = code_content.replace('<', '&lt;').replace('>', '&gt;')
            lines = escaped.split('\n')
            html_blocks.append(f'<blockquote>{("<br>".join(lines))}</blockquote>')
            continue
        
        # 表格
        if '|' in block and block.count('|') >= 2:
            table_html = parse_table(block)
            if table_html:
                html_blocks.append(table_html)
                continue
        
        # 标题
        if block.startswith('## '):
            text = process_inline(block[3:])
            html_blocks.append(f'<h2>{text}</h2>')
            continue
        if block.startswith('### '):
            text = process_inline(block[4:])
            html_blocks.append(f'<h3>{text}</h3>')
            continue
        
        # 引用块
        if block.startswith('> '):
            quote_text = process_inline(block[2:])
            html_blocks.append(f'<blockquote>{quote_text}</blockquote>')
            continue
        
        # 无序列表
        if is_unordered_list(block):
            html_blocks.append(parse_unordered_list(block))
            continue
        
        # 有序列表
        if is_ordered_list(block):
            html_blocks.append(parse_ordered_list(block))
            continue
        
        # 普通段落
        text = process_inline(block)
        text = text.replace('\n', '<br>')
        html_blocks.append(f'<p>{text}</p>')
    
    return ''.join(html_blocks)


def split_markdown_blocks(markdown: str) -> list:
    """将 Markdown 分割成块"""
    blocks = []
    current = []
    in_code_block = False
    
    for line in markdown.split('\n'):
        # 检测代码块边界
        if line.strip().startswith('```'):
            if in_code_block:
                current.append(line)
                blocks.append('\n'.join(current))
                current = []
                in_code_block = False
            else:
                if current:
                    blocks.append('\n'.join(current))
                    current = []
                current.append(line)
                in_code_block = True
            continue
        
        if in_code_block:
            current.append(line)
            continue
        
        # 空行分隔块
        if not line.strip():
            if current:
                blocks.append('\n'.join(current))
                current = []
        else:
            current.append(line)
    
    if current:
        blocks.append('\n'.join(current))
    
    return blocks


def extract_code_block(block: str) -> str:
    """提取代码块内容"""
    lines = block.split('\n')
    # 去掉首尾的 ```
    if lines[0].startswith('```'):
        lines = lines[1:]
    if lines and lines[-1].strip() == '```':
        lines = lines[:-1]
    return '\n'.join(lines)


def is_unordered_list(block: str) -> bool:
    """检测是否为无序列表"""
    lines = block.split('\n')
    has_list_item = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('* ') or stripped.startswith('- '):
            has_list_item = True
        else:
            return False
    return has_list_item


def is_ordered_list(block: str) -> bool:
    """检测是否为有序列表"""
    lines = block.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped and not re.match(r'^\d+\. ', stripped):
            return False
    return True


def parse_unordered_list(block: str) -> str:
    """解析无序列表"""
    items = []
    for line in block.split('\n'):
        stripped = line.strip()
        if stripped.startswith('* '):
            items.append(process_inline(stripped[2:]))
        elif stripped.startswith('- '):
            items.append(process_inline(stripped[2:]))
    
    li_tags = ''.join(f'<li>{item}</li>' for item in items)
    return f'<ul>{li_tags}</ul>'


def parse_ordered_list(block: str) -> str:
    """解析有序列表"""
    items = []
    for line in block.split('\n'):
        stripped = line.strip()
        match = re.match(r'^\d+\. (.+)$', stripped)
        if match:
            items.append(process_inline(match.group(1)))
    
    li_tags = ''.join(f'<li>{item}</li>' for item in items)
    return f'<ol>{li_tags}</ol>'


def parse_table(block: str) -> str:
    """解析表格"""
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    if len(lines) < 2:
        return None
    
    # 检查是否有分隔行
    has_separator = False
    separator_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^[\|\s\-:]+$', line):
            has_separator = True
            separator_idx = i
            break
    
    if not has_separator:
        return None
    
    # 解析表头
    header_line = lines[0]
    headers = [cell.strip() for cell in header_line.split('|') if cell.strip()]
    
    # 解析数据行
    data_lines = lines[separator_idx + 1:]
    rows = []
    for line in data_lines:
        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
        if cells:
            rows.append(cells)
    
    # 生成 HTML - 简化表格表示（X Article 可能不完全支持 table）
    # 使用粗体表头 + 换行的方式
    result = '<p>'
    header_text = ' | '.join(f'<strong>{h}</strong>' for h in headers)
    result += header_text + '<br>'
    result += '-' * 20 + '<br>'
    for row in rows:
        result += ' | '.join(process_inline(cell) for cell in row) + '<br>'
    result += '</p>'
    
    return result


def process_inline(text: str) -> str:
    """处理行内格式"""
    # 行内代码 `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # 粗体 **text**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # 斜体 *text* (注意不要匹配列表项)
    text = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', text)
    
    # 链接 [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    return text


def main():
    if len(sys.argv) < 2:
        print("用法: python parse_markdown_fixed.py <markdown_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    base_path = Path(filepath).parent
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = parse_markdown_for_x(content, base_path)
    
    if '--html-only' in sys.argv:
        print(result['html'])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
