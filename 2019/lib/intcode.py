"""
Multiple puzzles this year use "intcode" this library will be used to work with those codes
"""

"""
define possible operation codes, and corresponding operations -
note: writing the dictionary out would have been clearer actually
"""

# TODO: figure out how to do this




class fixed_input:
    def __init__(self, data):
        self.data = data
        self.pointer = 0
    def next(self):
        entry = self.data[self.pointer]
        self.pointer += 1
        if self.pointer >= len(self.data):
            self.pointer = 0
        return entry








class int_computer():
    """
    operates on intcodes per Advent of Code 2019 - Day 2
    """
    def __init__(self, init_code,
                 input_stream=None, output_stream=print,
                 debug=False):
        """
        Initialize with some intcode
        """
        self.output_stream=output_stream
        self.debug = debug

        self.input_stream=input_stream
        self.code = init_code
        self.pointer = 0
        self.OP_DICT = {
            1: self.intcode_add,
            2: self.intcode_mult,
            3: self.intcode_get_input,
            4: self.intcode_get_output,
            88: self.intcode_diagnostic,
            99: self.intcode_quit
        }

    def intcode_diagnostic(self, args):
        STEP_SIZE = 1
        if args == None:
            args = []
        while len(args) < 3:
            args.append(0)
        print(args)
        self.pointer += STEP_SIZE
        return 1

    def intcode_add(self, args=[0]):
        """
        moves pointer 4 positions forward, adds positions 1 and 2,
        outputs position 3
        """
        STEP_SIZE = 4
        if args == None:
            args = []
        while len(args) < STEP_SIZE-1:
            args.append(0)

        # input is the value at position 1 and 2
        # this is the behavior with arg=1
        in1 = int(self.code[self.pointer+1])
        in2 = int(self.code[self.pointer+2])
        # arg == 0
        # input is the value at the location specified
        if not args[0] == 1:
            in1 = int(self.code[in1])
        if not args[1] == 1:
            in2 = int(self.code[in2])
        result = in1 + in2
        if not args[2] == 1:
            out1 = int(self.code[self.pointer+2])
            self.code[out1] = str(result)
        else:
            self.code[self.pointer+2] = str(result)
        self.pointer += STEP_SIZE
        return 1

    def intcode_mult(self, args=[0]):
        """
        moves pointer 4 positions forward, multiplies positions 1 and 2,
        outputs position 3
        """
        STEP_SIZE = 4
        if args == None:
            args = []
        while len(args) < STEP_SIZE-1:
            args.append(0)
        in1 = int(self.code[self.pointer+1])
        in2 = int(self.code[self.pointer+2])
        if not args[0] == 1:
            in1 = int(self.code[in1])
        if not args[1] == 1:
            in2 = int(self.code[in2])
        result = in1 * in2
        if not args[2] == 1:
            out1 = int(self.code[self.pointer+2])
            self.code[out1] = str(result)
        else:
            self.code[self.pointer+2] = str(result)
        self.pointer += STEP_SIZE
        return 1

    def intcode_get_input(self, args=[0]):
        STEP_SIZE = 2
        if args == None:
            args = []
        while len(args) < STEP_SIZE-1:
            args.append(0)
        status = 1
        # loc is value of code at position pointer
        loc = int(self.code[self.pointer+1])
        # args == 1
        if args[0] == 1:
            # location is pointer + 1
            loc = self.pointer+1
        in1 = self.input_stream.next()
        self.code[loc] = in1
        self.pointer += STEP_SIZE
        return status

    def intcode_get_output(self, args=[0]):
        STEP_SIZE = 2
        if args == None:
            args = []
        while len(args) < STEP_SIZE-1:
            args.append(0)
        status = 1
        loc = int(self.code[self.pointer+1])
        if args[0] == 1:
            loc = self.pointer+1
        print(self.pointer, loc)
        self.output_stream(self.code[loc])
        self.diagCode = self.code[loc]
        self.pointer += STEP_SIZE
        return status

    def intcode_quit(self, args):
        return 0

    def run_step(self):
        """
        perform one operation,
        """
        instruction_str = self.code[self.pointer]
        opcode = instruction_str[-2:]
        # define args here
        # default
        argstring = instruction_str[:-2]
        arglist = list(argstring)
        args = [int(x) for x in arglist]
        args.reverse()
        try:
            status = self.OP_DICT[int(opcode)](args)
        except KeyError:
            return self.pointer, self.code[self.pointer]
        return status

    def run_code(self):
        """
        run through intcode, if no code is provided use the code provided when class was created
        returns 0 if 99 was reached, 2 if some unexpected op-code encountered
        """
        retVal = 1
        while(retVal == 1):
            retVal = self.run_step()
        return retVal

    def run_code_d2(self):
        """
        run through intcode, if no code is provided use the code provided when class was created
        returns 0 if 99 was reached, 2 if some unexpected op-code encountered
        """
        retVal = 1
        try:
            while(retVal == 1):
                retVal = self.run_step()
        except IndexError:
            return(self.pointer, self.code[self.pointer])
        return retVal
    def run_diag(self):
        retVal = 1
        self.diagCode = '0'
        while((retVal == 1) and (self.diagCode == '0')):
            retVal = self.run_step()
        print("Current Position: ", self.pointer)

    def get_code(self):
        return self.code


if __name__ == "__main__":
    testCase2 = int_computer(
        ["1", '9', '10', '3', '2', '3', '11', '0', '99', '30', '40', '50'])
    testCase1 = int_computer(["1", "1", "1", "1", "99"])
    testCase3 = int_computer(["3", "1", "4", "1", "99"], fixed_input('9'))
    testCase4 = int_computer(['11188', '1188', '188', '88', '1088',
                              '10088', '10188', '99'])
    print(testCase4.get_code())
    print(testCase4.run_code())
    print(testCase4.get_code())
    #testCase.run_step()
