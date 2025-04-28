
import json
import requests
import pandas as pd

qwen_config={
    'url': 'http://192.168.1.14:19997/v1/chat/completions',
    'model': 'SAGI-SXHBT-32B',
    'creds': 'Bearer sk-ALTbgl6ut981w'
}


def _request_vllm(url:str, query:str, system:str, model, authorization=None, temperature=0.01, top_p=0.95, max_tokens=2048):
    response = requests.post(
        url,
        json={
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": query}
            ],
            "model": model,
            "max_tokens": max_tokens,
            "temperature":temperature,
            "top_p":top_p
        },
        headers={'Authorization': authorization}
    )
    if response.status_code == 200:
        res = response.json()
        content = res['choices'][0]['message']['content']
        return content
    return ''

def request_llm(system, user):

    res = _request_vllm(url=qwen_config['url'], query=user, system=system, model=qwen_config['model'],
                        authorization = qwen_config['creds'], max_tokens = 32)

    return res


def main():
    infile='../data/tableqa_data/train/test-en-qa-table-cls.json'
    outfile='../data/tableqa_data/train/test-en-qa-table-cls-pred.xlsx'
    result_list=[]
    with open(infile) as f:
        data = json.load(f)
        for d in data:
            messages = d['messages']
            for msg in messages:
                if msg['role']=='system':
                    system=msg['content']
                elif msg['role']=='user':
                    user = msg['content']
                else:
                    answer = msg['content']
            pred = request_llm(system, user)
            r={
                'system':system,
                'user':user,
                'answer':answer,
                'pred':pred,
                'is_true': 1 if answer==pred else 0
            }
            result_list.append(r)
            break
    df = pd.DataFrame(result_list)
    df.to_excel(outfile, index=False)

if __name__ == '__main__':
    main()