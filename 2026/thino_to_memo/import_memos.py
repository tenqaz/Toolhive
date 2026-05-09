#!/usr/bin/env python3
import json
import requests
import argparse
from datetime import datetime, timezone, timedelta

MEMOS_URL = "https://xxx/api/v1/memos"
AUTH_TOKEN = "xxx"

def convert_to_iso(datetime_str):
    """将 'YYYY-MM-DD HH:MM:SS' 转换为 ISO 8601 格式（东八区）"""
    dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
    return dt.isoformat()

def import_memos(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        memos = json.load(f)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    success_count = 0
    fail_count = 0

    for memo in memos:
        created_time = convert_to_iso(memo["datetime"])

        payload = {
            "state": "NORMAL",
            "content": memo["content"],
            "visibility": "PRIVATE",
            "createTime": created_time,
            "updateTime": created_time
        }

        try:
            response = requests.post(MEMOS_URL, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                success_count += 1
                print(f"✓ 导入成功: {memo['datetime']}")
            else:
                fail_count += 1
                print(f"✗ 导入失败: {memo['datetime']} - {response.status_code} - {response.text}")
        except Exception as e:
            fail_count += 1
            print(f"✗ 导入失败: {memo['datetime']} - {str(e)}")

    print(f"\n导入完成: 成功 {success_count}, 失败 {fail_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='导入 Memos 到服务')
    parser.add_argument('-f', '--file', default='memos.json', help='JSON 文件路径')
    parser.add_argument('-u', '--url', help='Memos API URL')
    parser.add_argument('-t', '--token', help='认证 Token')

    args = parser.parse_args()

    if args.url:
        MEMOS_URL = args.url
    if args.token:
        AUTH_TOKEN = args.token

    import_memos(args.file)
