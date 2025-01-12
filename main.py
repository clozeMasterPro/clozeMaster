import os
import re
import random
import logging

import argparse
from tqdm import tqdm
import subprocess
import time
import csv
import pandas as pd

import torch
import tokenizers
from transformers import AutoModelForCausalLM, AutoTokenizer
import pandas as pd

from model.IncoderModel import InCoder
from utils.masking import ClozeMask


os.environ["TOKENIZERS_PARALLELISM"] = "false"


def get_rs_files(directory,suffix=['rs']):
    rs_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split('.')[-1] in suffix:
                rs_files.append(os.path.join(root, file))
    return rs_files

def compare_text(text1, text2):
    text1 = text1.replace(' ', '').replace('\n', '').replace('\t', '')
    text2 = text2.replace(' ', '').replace('\n', '').replace('\t', '')
    return text1==text2

def compile_rust(filepath,rsfile,opt):
    cmd="rustc {} -C opt-level={}  --out-dir temp".format(rsfile,opt) #--out-dir temp
    time_limit=180
    p=subprocess.Popen(cmd,cwd=filepath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,text=True)
    try:
        out, err = p.communicate(timeout=time_limit)
        returncode = p.returncode
        if "internal compiler error" in err.lower() or "compiler unexpectedly panicked" in err.lower():
            return "ice",err
        elif returncode==137:
            return "mem err",err
        elif "process didn't exit successfully" in err.lower():
            return "crash",err
        else:
            return "ok",err
    except subprocess.TimeoutExpired:
        p.terminate()
        return "timeout","" 
    
def get_err(err):
    err_info=re.findall(r"thread 'rustc' panicked at.*?\n",err,re.DOTALL)
    if len(err_info)==0:
        err_info=""
    else:
        err_info=err_info[0]
    start=err.find("query stack during panic:")
    end=err.find("end of query stack")
    stack_info=err[start:end]
    stack_info=stack_info.split("\n")
    stack_info=[info[:info.find("]")+1] for info in stack_info]
    stack_info="\n".join(stack_info)
    return err_info,stack_info

def add_csv(filename,columns,new_line_list):
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)

        if file.tell() == 0:
            writer.writerow(columns)

        writer.writerow(new_line_list)



if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default = "/path/to/your/model")#your model path
    parser.add_argument('--tokenizer_path', type=str, default="/path/to/your/model")# #your tokenizer path
    
    parser.add_argument('--rs_files', type=str, default = './dataset/')#your rust files path,default is the rust files path

    parser.add_argument('--csv_file', type=str, default = './log/bug.csv')#your csv file path
    parser.add_argument('--log_file', type=str, default = './log/demo.log')#your log file path
    args = parser.parse_args()
    

    logging.basicConfig(level=logging.INFO 
                    ,filename=args.log_file
                    ,filemode="w" 
                    ,format="%(asctime)s - %(name)s - %(levelname)-9s - %(filename)-8s : %(lineno)s line - %(message)s" 
                    
                    ,datefmt="%Y-%m-%d %H:%M:%S" 
                    )
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model_path = args.model_path
    tokenizer_path = args.tokenizer_path
    incoder = InCoder(model_path, tokenizer_path, device)
    cloze_mask = ClozeMask()

    opts=['0','1','2','3','s','z']
    csv_file = args.csv_file

    rs_files=get_rs_files(args.rs_files)
    
    
    logging.info('============================\n rs_files num:{}\n=========================\n'.format(len(rs_files)))

    for rs_file in tqdm(rs_files):
        with open(rs_file,'r',errors='ignore') as f:
            code = f.read()
        masked_codes = cloze_mask.mask_singel_code(code)
        cnt=0
        for masked_code in masked_codes:
            cnt+=1
            masked_file=rs_file.replace('dataset','target_dataset')
            filename=rs_file.split('/')[-1]
            newfilename=filename.split('.')[0]+'_'+str(cnt)+'.'+filename.split('.')[1]
            masked_file=masked_file.replace(filename,newfilename)
            if not os.path.exists(os.path.dirname(masked_file)):
                os.makedirs(os.path.dirname(masked_file))
            new_code=incoder.code_infilling(masked_code,temperature=0.2)
            with open(masked_file,'w') as f:
                f.write(new_code)

            for opt in opts:
                status,err=compile_rust(os.path.dirname(masked_file),newfilename,opt)
                err_info,stack_info=get_err(err)
                if status!="ok":
                    add_csv(csv_file,["filename","opt","status","err_info","stack_info"],[masked_file,opt,status,err_info,stack_info])
                logging.info('filename:{} opt:{} status:{} err_info:{} stack_info:{}'.format(newfilename,opt,status,err_info,stack_info))
                