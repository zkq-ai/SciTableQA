#nohup /root/miniforge3/envs/py312_llm/bin/python -u -m request_llm.tableqa.deepseek --lang en > logs/log-en-nohint.txt 2>&1 &
#nohup /root/miniforge3/envs/py312_llm/bin/python -u -m request_llm.tableqa.deepseek --lang en --is_hint > logs/log-en-with-hint.txt 2>&1 &

#nohup /root/miniforge3/envs/py312_llm/bin/python -u -m request_llm.tableqa.deepseek --lang en --llm_name qwen32b > logs/log-en-qwen32b-nohint.txt 2>&1 &
nohup /root/miniforge3/envs/py312_llm/bin/python -u -m request_llm.tableqa.deepseek --lang en --is_hint  --llm_name qwen32b> logs/log-en-qwen32b-with-hint.txt 2>&1 &