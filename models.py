class Node:
    def __init__(self):
        self._neighbours = []
    
    def connect(self, node):
        self._neighbours.append(node)
    
class FunctionBlock(Node):
    def __init__(self, block, arguments = []):
        super().__init__()
        self._function_body = block
        self._arguments = arguments

    def getBody(self):
        return self._function_body
    
    def getArguments(self):
        return self._arguments

class ConditionalBlock(Node):
    def __init__(self, condition, block):
        super().__init__()
        self._condition = condition
        self._block = block
    
    def getBody(self):
        return self._block
    
    def __repr__(self):
        return "\n\nexpr: {0}\ntype: {1}\n\n".format(" and ".join(map(lambda x: x.getExpression(), self._condition)), "".join(self._block.getCode()))

class GlobalBlock(Node):
    def __init__(self, block):
        super().__init__()
        self._block = block

    def getBody(self):
        return self._block


class Block:
    def __init__(self, code):
        self._code = code
    
    def getCode(self):
        return self._code   
 
class Condition:
    id = 0
    def __init__(self, expression, negated = False):
        self._expression = expression
        self._negated = negated
        self.id += 1 
        self._id = self.id   
    def getExpression(self):
        return ("not " if self._negated else "") + self._expression
    
    def negate(self):
        return Condition(self._expression, negated = True)

    def getId(self):
        return self._id
        
    def __str__(self):
        return self.getExpression()
    
    def __repr__(self):
        return self.getExpression()