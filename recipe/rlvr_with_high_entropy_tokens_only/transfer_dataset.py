from argparse import ArgumentParser

import pandas as pd
from tqdm import trange

parser = ArgumentParser()
parser.add_argument('--original_file_path', type=str, required=True)
parser.add_argument('--save_file_path', type=str, required=True)
args = parser.parse_args()

parquest_data = pd.read_parquet(args.original_file_path)
original_suffix = "Please output the final answer within \\boxed{}."

new_prefix = "Solve the following math problem step by step. The last line of your response should be of the form Answer: $Answer (without quotes) where $Answer is the answer to the problem.\n\n"
new_suffix = '\n\nRemember to put your answer on its own line after "Answer:".'

for i in trange(len(parquest_data), desc="Transferring dataset"):
    cur_original_prompt = parquest_data['prompt'][i][0]['content']
    assert cur_original_prompt.endswith(original_suffix)
    cur_prompt = cur_original_prompt[:-len(original_suffix)]
    cur_prompt = cur_prompt.strip()
    cur_prompt = new_prefix + cur_prompt + new_suffix
    parquest_data.loc[i, 'prompt'] = [{'role': 'user', 'content': cur_prompt}]
    
parquest_data.to_parquet(args.save_file_path, index=False)

