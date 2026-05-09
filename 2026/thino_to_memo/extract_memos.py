#!/usr/bin/env python3
import os
import re
import json
import argparse
from pathlib import Path

def extract_memos_from_file(file_path):
    """从单个 MD 文件中提取 Memos"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取文件名中的日期
    filename = Path(file_path).stem
    date_match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if not date_match:
        return []

    file_date = date_match.group(1)

    # 查找 ## Memos 部分
    memos_match = re.search(r'## Memos\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if not memos_match:
        return []

    memos_section = memos_match.group(1)

    # 提取每条 memo（支持两种格式：换行缩进 或 直接跟随）
    memo_pattern = r'- (\d{2}:\d{2}:\d{2})\s*(?:\n\t|\s+)(.*?)(?=\n- \d{2}:\d{2}:\d{2}|\n## |\Z)'
    memos = []

    for match in re.finditer(memo_pattern, memos_section, re.DOTALL):
        time_str = match.group(1)
        content = match.group(2).strip()

        # 组合日期和时间
        datetime_str = f"{file_date} {time_str}"

        memos.append({
            'datetime': datetime_str,
            'content': content
        })

    return memos

def scan_directory(directory):
    """递归扫描目录中的所有 MD 文件"""
    all_memos = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md') and re.match(r'\d{4}-\d{2}-\d{2}\.md', file):
                file_path = os.path.join(root, file)
                memos = extract_memos_from_file(file_path)
                all_memos.extend(memos)

    return all_memos

def main():
    parser = argparse.ArgumentParser(description='从 Markdown 文件中提取 Memos 记录')
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('-o', '--output', default='memos.json', help='输出 JSON 文件路径')

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误: {args.directory} 不是有效的目录")
        return

    print(f"正在扫描目录: {args.directory}")
    memos = scan_directory(args.directory)

    # 按时间排序
    memos.sort(key=lambda x: x['datetime'])

    # 写入 JSON 文件
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(memos, f, ensure_ascii=False, indent=2)

    print(f"成功提取 {len(memos)} 条 Memos 记录")
    print(f"已保存到: {args.output}")

if __name__ == '__main__':
    main()
