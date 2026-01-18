# X Article Publisher Enhanced

[English](#english) | [中文](#中文)

---

## English

An enhanced Markdown to X (Twitter) Article publisher with improved parsing for code blocks, lists, and inline code formatting.

This is a fork of [wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill) with significant improvements to the Markdown parser.

### What's Improved

| Feature | Original | Enhanced |
|---------|----------|----------|
| Unordered lists (`* item`) | Misinterpreted as italic | Correctly parsed as `<ul><li>` |
| Inline code (`` `code` ``) | Not supported | Converted to `<code>` |
| Horizontal rules (`---`) | Treated as text | Converted to `<hr/>` |
| Tables | Basic support | Text-based display |
| Code blocks | Basic blockquote | Proper blockquote with line breaks |

### Requirements

- Python 3.9+
- Windows: `pip install Pillow pywin32 clip-util`
- macOS: `pip install Pillow pyobjc-framework-Cocoa`

### Usage

```bash
# Parse Markdown and copy to clipboard
python scripts/gen_x_html.py your_article.md

# Then paste in X Article editor (Ctrl+V / Cmd+V)
```

### Files

- `parse_markdown_fixed.py` - Enhanced Markdown parser
- `copy_to_clipboard.py` - Cross-platform clipboard utility
- `scripts/gen_x_html.py` - Main script for generating and copying HTML

---

## 中文

增强版 Markdown 转 X (Twitter) Article 发布工具，改进了代码块、列表和行内代码的解析。

这是 [wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill) 的改进版，主要改进了 Markdown 解析器。

### 改进内容

| 功能 | 原版 | 改进版 |
|------|------|--------|
| 无序列表 (`* item`) | 错误解析为斜体 | 正确解析为 `<ul><li>` |
| 行内代码 (`` `code` ``) | 不支持 | 转换为 `<code>` |
| 分隔线 (`---`) | 当作文本 | 转换为 `<hr/>` |
| 表格 | 基础支持 | 文本格式显示 |
| 代码块 | 基础引用块 | 带换行的标准引用块 |

### 环境要求

- Python 3.9+
- Windows: `pip install Pillow pywin32 clip-util`
- macOS: `pip install Pillow pyobjc-framework-Cocoa`

### 使用方法

```bash
# 解析 Markdown 并复制到剪贴板
python scripts/gen_x_html.py 你的文章.md

# 然后在 X Article 编辑器中粘贴 (Ctrl+V / Cmd+V)
```

### 发布流程

1. 运行脚本生成 HTML 并复制到剪贴板
2. 打开 https://x.com/compose/articles
3. 点击 **create** 创建新文章
4. 填写标题
5. 在编辑器中按 **Ctrl+V** 粘贴内容
6. 预览并发布

### 注意事项

- X Article 不支持原生代码块，代码用引用块 (`<blockquote>`) 替代
- X Article 不支持表格，用文本形式展示

---

## License

MIT License

## Credits

Based on [wshuyi/x-article-publisher-skill](https://github.com/wshuyi/x-article-publisher-skill)
