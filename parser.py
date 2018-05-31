import re
from models import Condition, ConditionalBlock, Block, FunctionBlock, Node, GlobalBlock

graph = Node()
sample = "sample_inputs/sample.py"

no_of_tabs = 0
identation_expression = r"^( +)?"
conditional_expression = r"^(if|while|elif)[ ]?\(?(True|False|.+)?\)?:"
else_expression = r"^(else)"
block_buffer = []
condition_stack = []
for_else = []
if_pos = 0

condition_lookup = {

}

def main():
    global no_of_tabs, block_buffer, condition_stack, for_else, isOnElse, if_pos, condition_lookup
    print("opening: {0}".format(sample))
    with open(sample) as file:
        lines = file.readlines()
        for eachline in lines:
            matched = re.match(identation_expression, eachline).groups()
            if matched[0] is not None:
                tabs = len(matched[0])
            else:
                tabs = 0
            if tabs > no_of_tabs:
                block_buffer = [eachline]
            elif tabs < no_of_tabs:
                print(condition_stack)
                conditional_block = ConditionalBlock(condition_stack, Block(block_buffer))
                graph.connect(conditional_block)

                try:
                    condition_stack.pop()
                except: pass
                conditional_block = ConditionalBlock(condition_stack, Block(block_buffer))
                graph.connect(conditional_block)
                
            else:
                block_buffer.append(eachline)

            eachline = eachline.strip()
            is_conditional_statement = re.match(conditional_expression, eachline.strip())
            is_else_conditional_statement = re.match(else_expression, eachline.strip())
            if is_conditional_statement is not None:                
                if eachline.startswith('elif'):
                    condition_stack.pop()
                temp_cond = Condition(is_conditional_statement.groups()[1])
                condition_lookup[is_conditional_statement.groups()[1]] = temp_cond
                condition_stack.append(temp_cond)
                for_else.append(temp_cond.negate())
                no_of_tabs -= 4
 
            elif is_else_conditional_statement is not None:
                condition_stack.extend(for_else[if_pos*-1:-1])
                no_of_tabs -= 4
                for_else = []
                try:
                    condition_stack.pop()
                except: pass


            no_of_tabs = tabs
            print("inside :", " AND ".join(map(lambda x: "'{0}'".format(x), condition_stack if len(condition_stack) > 0 else ["global"]))," ------------->  ", eachline.strip()) 
           
if __name__ == '__main__':
    main()
    print(graph._neighbours)