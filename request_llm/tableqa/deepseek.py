# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import json
from request_llm.tableqa.prompts.qa_prompts import *
from request_llm.tableqa.prompts.eval_prompt import *
from eval.my_rouge import calc_rouge
import re
import traceback
import os
from request_llm.tableqa.prompts.hint_map import *
from arg_helper import args
import requests

client = OpenAI(api_key="sk-ee481c03d2734de8ad7bdc8008452fca", base_url="https://api.deepseek.com")
qwen_32b_config={
    # 'url':'http://192.168.1.137:8440/qwen201/v1/chat/completions',
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
    if args.llm_name=='deepseek':
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            stream=False
        )
        res = response.choices[0].message.content
    elif args.llm_name=='qwen32b':
        res = _request_vllm( url=qwen_32b_config['url'], query=user, system=system, model=qwen_32b_config['model'],
                       authorization = qwen_32b_config['creds'],max_tokens = 2048)

    return res

def request_deepseek(system, user):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        stream=False
    )

    return response.choices[0].message.content

def _get_examples_prompt(examples, lang='en'):
    """

    :param examples:
    :return:
    """
    example_result=""
    for i, d in enumerate(examples):
        articleTitle = d['articleTitle']
        tableInSec = d['tableInSec']
        tableInContext = d['tableInContext']
        tableType = d['tableType']
        tableTitle = d['tableTitle']
        tableContent = d['tableContent']
        questionType = d['questionType']
        question = d['question']
        answer = d['answer']
        reasonStepDetails = d['reasonStepDetails']

        a="""
    ## example{index}
    ### related table info
        **article title**
        {articleTitle}
        **table in section**
        {tableInSec}
        **table in context**
        {tableInContext}
        **table title**
        {tableTitle}
        **table content with {content_format} format**
        {tableContent}
        **question type**
        {questionType}
    
    ### question	
    {question}
    
    ### answer
    reasoning: {reasoning}
    last answer is: {answer}
        """
        reasoning = ' '.join([list(r.items())[0][0]+', ' + list(r.items())[0][1] for r in reasonStepDetails])
        d['reasoning']=reasoning
        d['index']=i+1
        d['content_format'] = args.table_content_type
        b= a.format_map(d)
        example_result += b
    return example_result


def _get_last_answer(text):
    print('raw answer: ', text)
    n = len('last answer is:')
    index = text.find('last answer is:')
    while index > 0:
        text = text[index+n:]
        index = text.find('last answer is:')
    return text

def _get_total_deepseek_score(text):
    print('text: ',text)
    m=re.search(r'Total Score[^0-9]{,4}([0-9]{1,})',text)
    score = float(m.groups()[0])
    return score

def _get_history_result(file_path):
    history_result_dict={}
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line:
                    d = json.loads(line)
                    history_result_dict[d['d']['tableId']] = d
    return history_result_dict


def _get_root_path():
    root_path = os.path.join(os.path.dirname(__file__),'../../')
    return root_path

def test1():

    lang = args.lang
    is_hint=args.is_hint
    # is_hint=True
    each_max_num=200
    # each_max_num=5

    is_hint_str = 'is-hint' if is_hint else 'no-hint'

    root_path = _get_root_path()
    if lang == 'en':
        infile = os.path.join(root_path, f'data/tableqa_data/en-qa-{args.table_content_type}.json')
        outfile = os.path.join(root_path, f'data/tableqa_data/result/en-qa-result-{is_hint_str}-each_max_num{each_max_num}-{args.llm_name}.json')
    else:
        infile = os.path.join(root_path, f'data/tableqa_data/zh-qa-{args.table_content_type}.json')
        outfile = os.path.join(root_path, f'data/tableqa_data/result/zh-qa-result-{is_hint_str}-each_max_num{each_max_num}-{args.llm_name}.json')
    data_dict_with_question_type={}

    history_result_dict = _get_history_result(outfile)

    with open(infile) as f:
        data = json.load(f)
        for d in data:
            questionType = d['questionType']
            if questionType in data_dict_with_question_type:
                v = data_dict_with_question_type[questionType]
                v.append(d)
            else:
                v=[]
                v.append(d)
                data_dict_with_question_type[questionType] = v
    total_n = 0
    result_list=[]
    total_score=0
    pred_list=[]
    true_list=[]
    with open(outfile, 'a', encoding='utf-8') as out:
        for k,v in data_dict_with_question_type.items():
            examples = v[:3]
            examples_str = _get_examples_prompt(examples, lang)
            for d in v[:each_max_num]:
                try:
                    total_n+=1
                    print('===当前记录数：',total_n)
                    answer=d['answer']

                    if d['tableId'] in history_result_dict:
                        r = history_result_dict[d['tableId']]
                        total_score += r['deepseek_score']
                        pred_list.append(r['last_pred'])
                        true_list.append([answer])
                        # rouge = calc_rouge([last_pred], [[answer]])
                        # print('deepseek_score: ', deepseek_score)
                        # print('rouge: ', rouge)
                        result_list.append(r)
                        break
                    d['examples']=examples_str
                    d['content_format']=args.table_content_type
                    if is_hint:
                        if lang=='en':
                            system_prompt =  en_qa_prompt_with_hint_system
                            d['reasoning_hint'] = table_class_hint_map[d['tableType'].lower()]
                        else:
                            pass
                    else:
                        if lang == 'en':
                            system_prompt = en_qa_prompt_no_hint_system
                        else:
                            pass

                    system = system_prompt.format_map(d)
                    user = "# question\n" + d['question']
                    print(system)
                    print(user)
                    raw_pred = request_llm(system, user)
                    last_pred = _get_last_answer(raw_pred)
                    deepseek_score_raw = request_deepseek(deepseek_eval_prompt_system, deepseek_eval_prompt_user.format(answer, last_pred))
                    deepseek_score = _get_total_deepseek_score(deepseek_score_raw)
                    total_score += deepseek_score
                    pred_list.append(last_pred)
                    true_list.append([answer])
                    # rouge = calc_rouge([last_pred], [[answer]])
                    print('true answer: ', answer)
                    print('deepseek_score: ', deepseek_score)
                    # print('rouge: ', rouge)
                    r = {
                        'system':system,
                        'user':user,
                        'raw_pred':raw_pred,
                        'last_pred':last_pred,
                        'deepseek_score':deepseek_score,
                        'd':d
                    }
                    result_list.append(r)
                    line = json.dumps(r, ensure_ascii=False)
                    out.write(line+'\n')
                except:
                    traceback.print_exc()
            # break
    rouge_res = calc_rouge(pred_list, true_list)
    print(rouge_res)
    print('total_score: ',total_score, 'mean deepscore: ', total_score / total_n)


def test2():
    lang = 'en'
    lang = 'zh'
    is_hint=False
    is_hint=True

    is_hint = 'is-hint' if is_hint else 'no-hint'
    root_path = _get_root_path()
    if lang=='en':
        infile=os.path.join(root_path, 'data/tableqa_data/en-qa.json')
        outfile = os.path.join(root_path, f'data/tableqa_data/result/en-qa-result-{is_hint}.json')
    else:
        infile = os.path.join(root_path, 'data/tableqa_data/zh-qa.json')
        outfile = os.path.join(root_path, f'data/tableqa_data/result/zh-qa-result-{is_hint}.json')
    data_dict_with_question_type={}

    history_result_dict = _get_history_result(outfile)

    with open(infile) as f:
        data = json.load(f)
        for d in data:
            questionType = d['questionType']
            if questionType in data_dict_with_question_type:
                v = data_dict_with_question_type[questionType]
                v.append(d)
            else:
                v=[]
                v.append(d)
                data_dict_with_question_type[questionType] = v
    total_n = len(data)
    result_list=[]
    total_score=0
    pred_list=[]
    true_list=[]
    for k,v in data_dict_with_question_type.items():
        examples = v[:3]
        examples_str = _get_examples_prompt(examples, lang)
        for d in v:
            answer=d['answer']

            if d['tableId'] in history_result_dict:
                r = history_result_dict[d['tableId']]
                total_score += r['deepseek_score']
                pred_list.append(r['last_pred'])
                true_list.append([answer])
                # rouge = calc_rouge([last_pred], [[answer]])
                # print('deepseek_score: ', deepseek_score)
                # print('rouge: ', rouge)
                result_list.append(r)
                break
            d['examples']=examples_str
            if is_hint:
                if lang=='en':
                    system_prompt = en_qa_prompt_no_hint_system
                    print(d['tableType'].lower())
                    assert d['tableType'].lower() in  table_class_hint_map
                    total_score += 1
                    print('ok')
                else:
                    pass
            else:
                if lang == 'en':
                    system_prompt = en_qa_prompt_with_hint_system
                else:
                    pass

    print('total_score:',total_score, 'data', len(data))


    

if __name__ == '__main__':
    test1()
    # test2()