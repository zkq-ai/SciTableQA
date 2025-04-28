# coding=utf-8
"""
author: 卓可秋
date:2025/4/26
修改：
功能：

"""
import argparse

# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser()
parser.add_argument('--lang', help='语言', default='en')
parser.add_argument('--is_hint', help='是否加入表格类型提示', action='store_true')
parser.add_argument('--llm_name', help='deepseek, qwen32b, qwen72b,qwen7b,LLaMa3–8B,LLaMa3–70B', type=str, default='qwen32b')
parser.add_argument('--table_content_type', help='json, xml, csv, plaintext, markdown', type=str, default='xml')

# 解析参数
args = parser.parse_args()
