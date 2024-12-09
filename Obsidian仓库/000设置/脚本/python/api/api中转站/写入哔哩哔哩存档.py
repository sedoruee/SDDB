import time
import webbrowser

def print_and_open_webpage(text, url):
  """打印文本，打开网页，并保持控制台窗口打开。"""
  print(text)
  webbrowser.open(url)
  print("按下 Enter 键关闭窗口...")
  input()

# 使用示例
print_and_open_webpage("这是一段示例文本。", "https://bgm.tv/")