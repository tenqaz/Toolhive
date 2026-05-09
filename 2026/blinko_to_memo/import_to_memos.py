#!/usr/bin/env python3
import json
import requests

MEMOS_URL = "https://xxx/api/v1/memos"
AUTH_TOKEN = "xxx"

def import_notes():
    with open("notes.json", "r", encoding="utf-8") as f:
        notes = json.load(f)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    success_count = 0
    fail_count = 0

    for note in notes:
        payload = {
            "state": "NORMAL",
            "content": note["content"],
            "visibility": "PRIVATE",
            "createTime": note["createdAt"],
            "updateTime": note["createdAt"]
        }

        try:
            response = requests.post(MEMOS_URL, headers=headers, json=payload)
            if response.status_code in [200, 201]:
                success_count += 1
                print(f"✓ 导入成功 ID {note['id']}")
            else:
                fail_count += 1
                print(f"✗ 导入失败 ID {note['id']}: {response.status_code} - {response.text}")
        except Exception as e:
            fail_count += 1
            print(f"✗ 导入失败 ID {note['id']}: {str(e)}")

    print(f"\n导入完成: 成功 {success_count}, 失败 {fail_count}")

if __name__ == "__main__":
    import_notes()
