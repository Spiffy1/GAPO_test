# program description: 
# Công ty cần xây dựng một hệ thống tính toán báo cáo động dựa trên dữ liệu thu thập được.
# Các số liệu của báo cáo được tính toán dựa trên công thức do người dùng chủ động nhập vào theo cú pháp có sẵn.
# Bạn cần implement hàm tính toán cho báo cáo dựa trên dữ liệu của công ty và công thức từ người dùng.
# Công thức chỉ cần hỗ trợ 4 phép tính cơ bản là cộng trừ nhân chia (và dấu ngoặc, optional)

# Input:
# - String công thức tính từ người dùng
# - Data để tính

# Output:
# - Kết quả số liệu cần tính toán

# Có hỗ trợ dấu ngoặc
# Có hỗ trợ power

# TODO:
#   Write unit test

class Calculator(object):
    """ Example input:
        expression: (12+4)*2^4-(10-3**(15/5))
        steps:
        1) convert key string to number
        2) compile input equation to a list of operators and numbers: [ [14,+,2],*,2,^,2,-,[20,-,3,*,[25,/,5]] ]
        3) calculate starting with the highest priority first:

        [ [14, +, 2], *, 4, -, [20,-,3,*,[25,/,5]] ]
        [ 19, *, 4, -, [20,-,3,*,5] ]
        [ 19, *, 4, -, [20-15] ]
        [ 19, *, 16, -, 5]
        [ 304, -, 5 ]
        [ 299 ]


    """
    _stack = []

    # Flag that signfies if it's the first character in the expression
    INITIAL = True

    # exit perenthesis
    EXIST_PARENS = False
    # in number
    IN_NUM = False
    # in operator
    IN_OPERATOR = False

    # in decimal
    ADD_DECIMAL = False

    OPERATORS = {
        '+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '^': lambda x,y: x**y
    }

    OPS_ORDER = (('^',), ('*', '/'), ('+', '-'))

    class ErrorInvalidExpression(Exception):
        pass


    def compile(self, input_eq, data):
        """
        Compile the expression to a python representation
        of a list of numbers, operators and lists (parentheses)
        """
        input_eq = calc.mod_input_eq(input_eq, data)
        print("input_eq: ", input_eq)
        i = 0
        for c in input_eq:
            try:

                # check if its a number
                current = int(c)

                # Adding floating point number to stack
                if self.ADD_DECIMAL:
                    last_pos = self._get_last_position()[-1]
                    if not isinstance(last_pos, float):
                        dec_count = 1
                        new_num = float(str(last_pos)+'.'+str(c))
                        self._get_last_position()[-1] = new_num
                        dec_count +=1
                    else:
                    # Solution 1  - Fail when add zero after the decimal point
                    # convert to string & append it to the end of the number rather than adding it
                        # new_num = str(last_pos) + str(c)
                        # self._get_last_position()[-1] = float(new_num)
                        
                    # Solution 2
                    # add new decimal place using power operator
                        new_num = last_pos + float(c)*(0.1**dec_count)
                        self._get_last_position()[-1] = new_num
                        dec_count +=1
                    
            except ValueError:
                
                # it's a decimal number
                if c == '.':
                    # self.IN_NUM = True
                    self.ADD_DECIMAL = True

                else:
                    # its not a number 
                    self.IN_NUM = False
                    self.ADD_DECIMAL = False
                    # if it's an operator 
                    if c in self.OPERATORS.keys():
                        if not self._stack:
                            raise ErrorInvalidExpression("You can't start an expression with an operator")

                        if self.IN_OPERATOR:
                            raise ErrorInValidExpression("More than one operator in a sequance")
                        else:
                            self._append_element(c)
                            self.IN_OPERATOR = True        
                    elif c == '(':
                        self._add_new_parentheses()
                        self.EXITS_PARENS = False
                    elif c == ')':
                        self.EXIST_PARENS = True

                    else:
                        raise ErrorInvalidExpression("Syntax Error")
                    continue
            
            # runs when its a number
            self.IN_OPERATOR = False

            # add the number to the stack
            if not self.ADD_DECIMAL:
                self._add_new_num(current)

            # if its a new number
            if not self.IN_NUM:
                self.IN_NUM = True

            if self.INITIAL:
                self.INITIAL = False
            i+=1
            list_ref = self._stack

    def mod_input_eq(self, input_eq, data):
        # This function replace all fields with their respective value
        import re

        splitter = re.split('\W', input_eq)
        new_list = []
        for i in splitter:
            if i != "":
                new_list.append(i)
                
        # remove all integer
        no_integers = [elem for elem in new_list if not (elem.isdigit() 
                                                or elem[0] == '-' and elem[1:].isdigit())]

        for key in no_integers:
            try: # ignore integer in the buffer list
                check_int = int(key)
            except ValueError:
                # replace original input_eq string with number
                try :
                    new_num=data[key]
                    input_eq = re.sub(key, str(new_num), input_eq)
                except KeyError:
                    raise ErrorInvalidExpression("Field name does not exist, please try again")
        return input_eq

    def _get_last_position(self):
        """ Returns the last inner most list in the stack """

        list_ref = list_prev = self._stack
        try:
            # While there's a list
            while list_ref[-1] or list_ref[-1] == []:
                if isinstance(list_ref[-1], list):
                    # make a reference to the list
                    list_prev = list_ref
                    list_ref = list_ref[-1]
                else:
                    break
        except IndexError:
            pass

        if self.EXIST_PARENS == True:
            self.EXIST_PARENS = False
            return list_prev
        else:
            return list_ref

    def _append_element(self, el):
        last_pos = self._get_last_position()
        last_pos.append(el)

    def _add_new_num(self, num):
        # if its the first character in an expression
        if not self._stack or self._get_last_position() == []:
            self._append_element(num)
        else:
            prev_c = self._get_last_position()[-1]
            # check if previous char is a number
            is_int = isinstance(prev_c, int)

            if is_int:
                self._add_to_previous_num(num, self._stack)
            elif prev_c in self.OPERATORS.keys():
                self._append_element(num)
            else:
                is_list = isinstance(self._stack[-1], list)
                # if it's a list search the last element in the list's children
                if is_list:
                    list_ref = self._get_last_position()
                    self._add_to_previous_num(num, list_ref)
                else:
                    # this should never happen
                    raise Exception("A fatal error has occured")

    def _add_to_previous_num(self, num, stack):
        try:
            last_pos = self._get_last_position()
            last_pos[-1] = last_pos[-1]*10+num
        except IndexError:
            last_pos.append(num)

    def _add_new_parentheses(self):
        last_pos = self._get_last_position()
        last_pos.append([])

    def calculate(self, expr, data):
        self.compile(''.join(expr.split()), data)
        # do the actual calculation
        result = self._rec_calc(self._stack)

        # initialize the stack
        self._stack = []
        self.ADD_DECIMAL = False
        print(result)
        return result

    def _rec_calc(self, stack):
        while len(stack) > 1:
            # print("stack size", self._stack) # Uncomment this to check stack progress

            for ops in self.OPS_ORDER:
                for el in range(len(stack)):
                    try:
                        if isinstance(stack[el], list):
                            result = self._rec_calc(stack[el])
                            del stack[el]
                            stack.insert(el, result)
                        elif stack[el] in ops:
                            result = self._calc_binary(stack, el)
                            # delete all three elements that were used in the binary operation
                            del stack[el-1]
                            del stack[el-1]
                            del stack[el-1]
                            stack.insert(el-1, result)
                    except IndexError:
                        break
                else:
                    continue
                break

        return stack[0]

    def _calc_binary(self, stack, index):
        op = stack[index]
        prev = stack[index-1]
        next = stack[index+1]

        for symbol, action in self.OPERATORS.items():
            if symbol == op:
                return action(prev, next)

data = {
    "price": 100,
    "amount": 50,
    "discount": 0.5,
    "unit": 1000,
    "added_tax": 50000
}


data2 = {
    "price": 200,
    "amount": 30,
    "discount": 0.205,
    "unit": 500,
    "added_tax": 10000
}


if __name__ == '__main__':
    calc = Calculator()


    calc.calculate("price * amount * discount", data) # 2500
    calc.calculate("price * amount * discount + 1000", data) # 3500
    calc.calculate("price * amount * unit", data) # 5000000
    calc.calculate("discount * 1000 + amount * price", data) # 5500
    calc.calculate("(price * amount + added_tax) * (1 - discount)", data) # 27500
    calc.calculate("(price * amount + added_tax) * (1 - discount) / unit", data) # 27,5
    calc.calculate("2*32-4+5+(1+2)+3+(1/2*3+3+(1+2))", data)
    calc.calculate("2 * (7+1) / (2 + 5 + (10-9)) ", data)
    calc.calculate("12^2-(5*(2+2)))", data)
    calc.calculate("price * (7+1) / (2 + amount + (10-9)) ", data)
    calc.calculate("price * amount", data)
    calc.calculate("price * (7+1) / (2 + 5 + (10-9)) ", data)
    calc.calculate("(12^2-5)-100*2", data)
    calc.calculate("(price * amount) * discount ", data)
    calc.calculate("price * amount * discount ", data)

    # TODO, write unit test
