from rouge_metric import PyRouge
import copy
from statistics import mean



def get_list_combination(a_list):
    """
    列表组合
    :param a_list:
    :return:
    """
    print('len(a_list): ', len(a_list))
    out_list=[]
    def _zuhe(a, b_list, start_index=0,):
        if start_index>=len(a):
            out_list.append(b_list)
            return
        es = a[start_index]
        for e in es:
            new_b_list = copy.deepcopy(b_list)
            new_b_list.append(e)
            _zuhe(a, new_b_list, start_index+1)

    _zuhe(a_list,[],0)
    print('len(out_list): ', len(out_list))
    return out_list

def calc_rouge(pred_lines, true_lines, is_single_answer=True):
    """

    :param pred_lines: [str1, str2,...]
    :param true_lines:[[str1,str2],[str1, str2,...],...]
    :return:{'rouge-1': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-2': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-4': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-l': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-s4': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-su4': {'r': 1.0, 'p': 1.0, 'f': 1.0}}
    https://pypi.org/project/rouge-metric/
    """
    if not pred_lines or not true_lines:
        return {}
    # rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_s=True, rouge_su=True, skip_gap=4)
    rouge = PyRouge(rouge_n=(1, 2), rouge_su=True, skip_gap=4)

    rouge_1_max_list = []
    rouge_2_max_list = []
    for pred , trues in zip(pred_lines, true_lines):
        # print('pred , trues:',pred , trues)
        rouge_1_max = -1
        rouge_1_max_ = {}
        rouge_2_max = -1
        rouge_2_max_ = {}
        for true in trues:
            score = rouge.evaluate([pred], [[true]])
            rouge1=score['rouge-1']['f']
            rouge2=score['rouge-2']['f']
            if rouge1>rouge_1_max:
                rouge_1_max_ = score['rouge-1']
                rouge_1_max=rouge1
            if rouge2 > rouge_2_max:
                rouge_2_max_ = score['rouge-2']
                rouge_2_max = rouge2
        rouge_1_max_list.append(rouge_1_max_)
        rouge_2_max_list.append(rouge_2_max_)
    def _get_mean(_list, _type):
        return mean([x[_type] for x in _list])
    p=_get_mean(rouge_1_max_list,'p')
    r=_get_mean(rouge_1_max_list,'r')
    f=_get_mean(rouge_1_max_list,'f')
    rouge_1_max_={'p':p,'r':r,'f':f}
    p = _get_mean(rouge_2_max_list, 'p')
    r = _get_mean(rouge_2_max_list, 'r')
    f = _get_mean(rouge_2_max_list, 'f')
    rouge_2_max_ = {'p': p, 'r': r, 'f': f}
    scores=rouge.evaluate(pred_lines, true_lines)
    scores['rouge-1-max']=rouge_1_max_
    scores['rouge-2-max']=rouge_2_max_

    return scores

def calc_rouge2(pred_lines, true_lines, is_single_answer=True):
    """

    :param pred_lines: [[x,x,x],[x,x,x]]
    :param true_lines:[[x,x,x],[x,x,x]]
    :return:{'rouge-1': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-2': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-4': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-l': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-s4': {'r': 1.0, 'p': 1.0, 'f': 1.0}, 'rouge-su4': {'r': 1.0, 'p': 1.0, 'f': 1.0}}
    https://pypi.org/project/rouge-metric/
    """
    # rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_s=True, rouge_su=True, skip_gap=4)
    rouge = PyRouge(rouge_n=(1, 2), rouge_su=True, skip_gap=4)

    if is_single_answer:
        true_lines = [[x] for x in true_lines]
    scores = rouge.evaluate_tokenized(pred_lines, true_lines) #已经切过词
    # scores = rouge.evaluate(pred_lines, true_lines)
    return scores

if __name__ == '__main__':
    pred_lines = [['Bacteria', 'such', 'as', 'A.', 'actinomycetemcomitans,', 'P.', 'gingivalis,', 'T.', 'forsythensis,', 'T.', 'denticola,', 'P.', 'intermedia', 'and', 'F.', 'nucleatum', 'are', 'associated', 'with', 'the', 'progression', 'of', 'peri-implantitis.']]
    true_lines = [['Bacteria', 'such', 'as', 'A.', 'actinomycetemcomitans,', 'P.', 'gingivalis,', 'T.', 'forsythensis,', 'T.', 'denticola,', 'P.', 'intermedia', 'and', 'F.', 'nucleatum', 'are', 'associated', 'with', 'the', 'progression', 'of', 'peri-implantitis.']]
    # rouge = calc_rouge(pred_lines, true_lines)
    # print(rouge)
    #
    # pred_lines = [
    #     ['1', '2', '3']]
    # true_lines = [
    #     ['1', '2', '3','2','4']]
    # rouge = calc_rouge(pred_lines, true_lines)
    # print(rouge)

    pred_lines = [
        ['how are'.split()],  # document 1: hypothesis
        ['it is fine today'.split()],  # document 2: hypothesis
    ]
    true_lines = [
        [['how are you'.split()],['how are'.split()]],  # document 1: hypothesis
        [['it is fine today'.split()], ['football game'.split()]],  # document 2: hypothesis
    ]

    hypotheses = [
        'how are you',
        'it is fine today\nwe won the football game',  # document 2: hypothesis
    ]
    references = [[
        'how are you\ni am fine',  # document 1: reference 1
        'how old are you\ni am three',  # document 1: reference 2
    ], [
        'it is sunny today\nlet us go for a walk',  # document 2: reference 1
        'it is fine today\nwe won the football game',  # document 2: reference 2
    ]]

    hypotheses = [
        'The gene product ZmIPT2 in Maize is an isopentenyl transferase involved in cytokinin biosynthesis, which likely promotes endosperm cell proliferation and thereby contributes to seed size, as indicated by references [57, 60].',
        # document 1: hypothesis
    ]
    references = [[
        'ZmIPT2 (Isopentenyl transferase) in Maize contributes to seed size by mediating cytokinin biosynthesis, boosting cell proliferation in the developing endosperm. The elevated cytokinin levels during early endosperm development enhance storage capacity and kernel size, making ZmIPT2 crucial for controlling yield-related traits in Maize.',  # document 1: reference 1
    ]]

    # rouge = PyRouge(rouge_n=(1, 2, 4), rouge_l=True, rouge_w=True,
    #                 rouge_w_weight=1.2, rouge_s=True, rouge_su=True, skip_gap=4)

    # scores = rouge.evaluate(hypotheses, references)
    # print(scores)

    rouge = calc_rouge(hypotheses, references, False)
    #
    print(rouge)