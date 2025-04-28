import json

lang='en'

def _get_message(data):
    _prompt="""# task
1. Given the following table from a scientific paper, classify the table into one of the following categories: 
"result table", "statistical table", "method comparison table", "configuration or parameter table", "summary or review table", "timeline and schedule table", "other types of table" 
2. Follow the Chain of Thought (CoT) reasoning steps to ensure accurate classification. 

# Table Context:
{table_context}
# Table Title:
{table_title}
# Table Content:
{table_content}
# Chain of Thought Reasoning Steps:
1)Identify the primary focus and objective of the table.
Determine the main purpose of the table based on its title and context.
2)Highlight the key metrics or data points presented.
List the main metrics, data points, or categories included in the table.
3)Analyze the structure and content of the table.
Examine how the data is organized and what kind of information is emphasized.
4)Compare the characteristics of the table with common features of known table types.
Match the identified characteristics with those typical of "Results Table", "Statistical Table", "Method Comparison Table", "Configuration or Parameter Table", "Summary or Review Table", "Timeline and Schedule Table", or "Other Table".
5)Conclude the classification and justify the decision.
Provide a final classification of the table and explain the reasoning behind the classification.
    """

    result_list=[]
    for d in data:
        try:
            system = _prompt.format_map({'table_context': d['tableInContext'],'table_title':d['tableTitle'],'table_content':d['tableContent']})
        except:
            continue
        r = {
            'messages':[
                {
                    'role':'system',
                    'content':system
                },
                {
                    'role': 'user',
                    'content': ''
                },
                {
                    'role':'assistant',
                    'content':d['tableType'].lower()
                },
            ]
        }
        result_list.append(r)
    return result_list

def main():
    with open(f'../data/tableqa_data/{lang}-qa.json') as f, \
        open(f'../data/tableqa_data/train/train-{lang}-qa-table-cls.json', 'w', encoding='utf-8') as out1,\
        open(f'../data/tableqa_data/train/test-{lang}-qa-table-cls.json', 'w', encoding='utf-8') as out2:
        train_result_list=[]
        test_result_list = []
        data_dict_with_question_type={}
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
        for k,v in data_dict_with_question_type.items():
            train_n = int(len(v)*0.7)
            test_n = len(v) - train_n
            train_v = v[:train_n]
            test_v = v[train_n:]
            res_list = _get_message(train_v)
            train_result_list.extend(res_list)
            res_list = _get_message(test_v)
            test_result_list.extend(res_list)

        json.dump(train_result_list, out1, ensure_ascii=False,indent=4)
        json.dump(test_result_list, out2, ensure_ascii=False, indent=4)
        print('训练数：',len(train_result_list))
        print('测试数：',len(test_result_list))


if __name__ == '__main__':
    main()
