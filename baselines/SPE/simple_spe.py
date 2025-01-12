import re
import random
def find_and_shuffle_variables(rust_code):
    variable_pattern = re.compile(r'let\s+(\w+)\s*[=;]')
    variables = variable_pattern.findall(rust_code)
    shuffled_variables = variables[:]
    random.shuffle(shuffled_variables)
    
    for original, shuffled in zip(variables, shuffled_variables):
        rust_code = re.sub(r'\b' + re.escape(original) + r'\b', shuffled, rust_code, 1)
    
    return len(variables), rust_code