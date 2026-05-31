import shutil
import os

src = r"C:\Users\ayush\.gemini\antigravity\brain\9ea99121-37fe-4e57-b1c4-c6c8071a7cce\media__1780167988536.jpg"
dst = r"d:\python codes\game\campaign_map.jpg"

try:
    shutil.copy(src, dst)
    print("SUCCESS: Copied image to", dst)
except Exception as e:
    print("ERROR:", e)
