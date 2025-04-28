
import json
import pandas as pd

from bs4 import BeautifulSoup

from openpyxl import Workbook
from bs4 import BeautifulSoup

lang='en'
with open(f'../data/tableqa_data/{lang}-qa.json') as f, \
    open(f'../data/tableqa_data/{lang}-qa-json.json', 'w', encoding='utf-8') as out:
    data = json.load(f)


    for d in data:
        xml_str = d['tableContent']
        soup = BeautifulSoup(xml_str, 'lxml')
        rows = soup.find_all('tr')

        # 创建 Excel 工作簿
        wb = Workbook()
        ws = wb.active

        # 写入表头
        headers = [th.get_text(strip=True) for th in rows[0].find_all('th')]
        ws.append(headers)

        # 写入数据
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            row_data = [cell.get_text(strip=True) for cell in cells]
            ws.append(row_data)

        # 保存 Excel 文件
        wb.save("output.xlsx")

        df = pd.read_excel("output.xlsx")
        r = df.to_dict(orient='records')
        print(r)
        tableContent=json.dumps(r,ensure_ascii=False)
        d['tableContent'] = tableContent
    json.dump(data, out, ensure_ascii=False,indent=4)


