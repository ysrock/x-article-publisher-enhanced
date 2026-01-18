#!/usr/bin/env python3
"""生成 X Article HTML 并复制到剪贴板"""
import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parse_markdown_fixed import parse_markdown_for_x
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("用法: python gen_x_html.py <markdown_file>")
        sys.exit(1)
    
    md_file = sys.argv[1]
    if not os.path.exists(md_file):
        print(f"错误: 文件不存在: {md_file}")
        sys.exit(1)
    
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = parse_markdown_for_x(content, Path(md_file).parent)
    
    # 保存 HTML
    html_file = md_file.replace('.md', '_x.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(result['html'])
    
    print(f"标题: {result['title']}")
    print(f"HTML 已保存到: {html_file}")
    print(f"长度: {len(result['html'])} 字符")
    
    # 尝试复制到剪贴板
    try:
        from clipboard import Clipboard
        with Clipboard() as clipboard:
            clipboard["html"] = result['html']
        print("已复制到剪贴板!")
    except Exception as e:
        print(f"复制到剪贴板失败: {e}")

if __name__ == '__main__':
    main()
