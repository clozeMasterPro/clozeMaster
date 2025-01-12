# ClozeMaster
Artifacts for "ClozeMaster: Fuzzing Rust Compiler by Harnessing LLMs for Infilling Masked Real Programs".
## Introduction
ClozeMaster is a novel fuzzing tool that leverages large language models (LLMs) to generate effective test cases for Rust compilers. The key idea behind ClozeMaster is to identify the bracket structure of given code and use it to guide the generation of new test cases through masked token completion. 
<br>This approach is very simple and easy to implement, and has achieved good practical application results in detecting defects in compilers of complex programming languages with limited training data (such as Rust). It is also easily transferable to the compilers of other relatively mature languages (such as C/C++).
## Install

Before using this tool, please ensure that the following development tools are installed on your computer:

- python>=3.8
- rustc (nightly)

You have to install all the libraries listed in `requirements.txt`

```sh
pip install -r requirements.txt
```

Additionally, ClozeMaster utilizes the [Incoder-1B](https://huggingface.co/facebook/incoder-1B), so please make sure your computer has sufficient memory and GPU resources to run the local inference of the LLM.


## Usage

```sh
python main.py --model_path your_model_path \
--tokenizer_path your_tokenizer_path \
--rs_files your_rust_files_path \
--csv_file path_which_you_want_to_log_the_bug_information \
--log_file path_which_you_want_to_log_the_fuzzing_progress
```

## Bug found by our tool
### Rust
#### rustc
[117696](https://github.com/rust-lang/rust/issues/117696)  
[117634](https://github.com/rust-lang/rust/issues/117634)  
[117443](https://github.com/rust-lang/rust/issues/117443)  
[117275](https://github.com/rust-lang/rust/issues/117275)  
[117275](https://github.com/rust-lang/rust/issues/117275)  
[117261](https://github.com/rust-lang/rust/issues/117261)  
[117257](https://github.com/rust-lang/rust/issues/117257)  
[116687](https://github.com/rust-lang/rust/issues/116687)  
[116681](https://github.com/rust-lang/rust/issues/116681)  
[116647](https://github.com/rust-lang/rust/issues/116647)  
[116624](https://github.com/rust-lang/rust/issues/116624)  
[116519](https://github.com/rust-lang/rust/issues/116519)  
[116287](https://github.com/rust-lang/rust/issues/116287)  
[115555](https://github.com/rust-lang/rust/issues/115555)  
[115435](https://github.com/rust-lang/rust/issues/115435)  
[115433](https://github.com/rust-lang/rust/issues/115433)  
[115407](https://github.com/rust-lang/rust/issues/115407)  
[115314](https://github.com/rust-lang/rust/issues/115314)  
[114464](https://github.com/rust-lang/rust/issues/114464)  
[114463](https://github.com/rust-lang/rust/issues/114463)  
[114317](https://github.com/rust-lang/rust/issues/114317)  
[118285](https://github.com/rust-lang/rust/issues/118285)  
[117657](https://github.com/rust-lang/rust/issues/117657)  
[117151](https://github.com/rust-lang/rust/issues/117151)  
[117080](https://github.com/rust-lang/rust/issues/117080)  
[116784](https://github.com/rust-lang/rust/issues/116784)  
[116783](https://github.com/rust-lang/rust/issues/116783)  
[116780](https://github.com/rust-lang/rust/issues/116780)  
[116554](https://github.com/rust-lang/rust/issues/116554)  
[115842](https://github.com/rust-lang/rust/issues/115842)  
[115599](https://github.com/rust-lang/rust/issues/115599)  
[114327](https://github.com/rust-lang/rust/issues/114327)  
[114324](https://github.com/rust-lang/rust/issues/114324)  
#### mrust
[322](https://github.com/thepowersgang/mrustc/issues/322)  
[321](https://github.com/thepowersgang/mrustc/issues/321)  
[320](https://github.com/thepowersgang/mrustc/issues/320)  
[318](https://github.com/thepowersgang/mrustc/issues/318)  
<!--
### C
#### LLVM
[87957](https://github.com/llvm/llvm-project/issues/87957)  
[89493](https://github.com/llvm/llvm-project/issues/89493)  
[90330](https://github.com/llvm/llvm-project/issues/90330)  

#### GCC
[114634](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=114634)  
[114638](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=114638)  
[114858](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=114858)  
[115173](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=115173)  
-->

## Docker Image
You can download our Docker image tarball at [link](https://drive.google.com/drive/folders/1LQtEQmF2OaM1oU8fuqW9Fetv2nKDJ_Uv?usp=sharing). Our bug data is located in the `/home/cloze` folder. You can run the bug_analysis.py script to reproduce the experimental results.

