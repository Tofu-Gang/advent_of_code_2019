__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import List, Tuple

################################################################################

class IntcodeComputer(object):
    OPCODE_ADD = 1
    OPCODE_MULTIPLY = 2
    OPCODE_SAVE_INPUT = 3
    OPCODE_WRITE_OUTPUT = 4
    OPCODE_JUMP_IF_TRUE = 5
    OPCODE_JUMP_IF_FALSE = 6
    OPCODE_LESS_THAN = 7
    OPCODE_EQUALS = 8
    OPCODE_EXIT = 99

    KEY_INPUT_PARAMS_COUNT = "input_params_count"
    KEY_OUTPUT_PARAMS_COUNT = "output_params_count"
    KEY_RUN_FUNCTION = "run_function"

    MODE_POSITION = '0'
    MODE_IMMEDIATE = '1'

################################################################################

    def __init__(self):
        """
        Creates the intcode computer instance with undefined memory, instruction
        pointer, input/output memories and jump/exit flag. Maps the correct
        methods to given opcodes.
        """

        self._instructions = {
            self.OPCODE_ADD: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 1,
                self.KEY_RUN_FUNCTION: self._add
            },
            self.OPCODE_MULTIPLY: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 1,
                self.KEY_RUN_FUNCTION: self._multiply
            },
            self.OPCODE_SAVE_INPUT: {
                self.KEY_INPUT_PARAMS_COUNT: 0,
                self.KEY_OUTPUT_PARAMS_COUNT: 1,
                self.KEY_RUN_FUNCTION: self._save_input
            },
            self.OPCODE_WRITE_OUTPUT: {
                self.KEY_INPUT_PARAMS_COUNT: 1,
                self.KEY_OUTPUT_PARAMS_COUNT: 0,
                self.KEY_RUN_FUNCTION: self._write_output
            },
            self.OPCODE_JUMP_IF_TRUE: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 0,
                self.KEY_RUN_FUNCTION: self._jump_if_true
            },
            self.OPCODE_JUMP_IF_FALSE: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 0,
                self.KEY_RUN_FUNCTION: self._jump_if_false
            },
            self.OPCODE_LESS_THAN: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 1,
                self.KEY_RUN_FUNCTION: self._less_than
            },
            self.OPCODE_EQUALS: {
                self.KEY_INPUT_PARAMS_COUNT: 2,
                self.KEY_OUTPUT_PARAMS_COUNT: 1,
                self.KEY_RUN_FUNCTION: self._equals
            },
            self.OPCODE_EXIT: {
                self.KEY_INPUT_PARAMS_COUNT: 0,
                self.KEY_OUTPUT_PARAMS_COUNT: 0,
                self.KEY_RUN_FUNCTION: self._exit
            }
        }

        self._memory = None
        self._input_values = None
        self._output_values = None
        self._instruction_pointer = None
        self._exit_flag = None
        self._auto_jump_flag = None

################################################################################

    def load_program(self, program: Tuple[int]) -> None:
        """
        Loads the given program in the memory. The program is then ready to run.

        :param program: tuple of integers
        """

        self._memory = list(program)
        self._instruction_pointer = 0
        self._exit_flag = False
        self._auto_jump_flag = True
        self._input_values = []
        self._output_values = []

################################################################################

    def load_input(self, input_value: int) -> None:
        """
        Loads an input value and saves it for later to be used by the program.

        :param input_value: input value
        """

        self._input_values.append(input_value)

################################################################################

    def run_program(self) -> None:
        """
        Runs the program loaded in the computer.
        """

        while not self._exit_flag:
            opcode = int(str(self._memory[self._instruction_pointer])[-2:])
            instruction = self._instructions[opcode]
            instruction[self.KEY_RUN_FUNCTION]()
            if self._auto_jump_flag:
                jump = instruction[self.KEY_INPUT_PARAMS_COUNT] \
                       + instruction[self.KEY_OUTPUT_PARAMS_COUNT] \
                       + 1
                self._instruction_pointer += jump
            else:
                self._auto_jump_flag = True

################################################################################

    def get_data(self, address: int) -> int:
        """
        Returns data on the given address.

        :param address: desired address
        :return: data on the given address
        """

        return self._memory[address]

################################################################################

    def set_data(self, address: int, data: int) -> None:
        """
        Manually sets data in memory.
        
        :param address: desired address 
        :param data: desired data
        """

        self._memory[address] = data

################################################################################

    def get_output(self) -> List[int]:
        """
        Returns all output values that were written by the program.

        :return: list of all output values
        """

        return self._output_values

################################################################################

    def _get_instruction_params(self) -> Tuple:
        """
        Gets instruction input param values. If the params are in immediate
        mode, the specified value is just taken. If the params are in position
        mode, the value is taken from the given address.

        :return: instruction input param values
        """

        # instruction from the memory
        heading = str(self._memory[self._instruction_pointer])
        opcode = int(heading[-2:])
        instruction = self._instructions[opcode]
        params_count = instruction[self.KEY_INPUT_PARAMS_COUNT]
        # prepend it with possible missing position modes
        heading = self.MODE_POSITION \
                  * (2 + params_count - len(heading)) + heading
        # number of modes and their order is the same as number and order of
        # input params
        modes = ''.join(reversed(heading[:-2]))
        return tuple([self._memory[
                          self._memory[self._instruction_pointer + i + 1]
                          if modes[i] == self.MODE_POSITION
                          else
                          self._instruction_pointer + i + 1]
                      for i in range(len(modes))])

################################################################################

    def _add(self) -> None:
        """
        Opcode 1 adds together numbers read from two positions and stores the
        result in a third position. The three integers immediately after the
        opcode tell you these three positions - the first two indicate the
        positions from which you should read the input values, and the third
        indicates the position at which the output should be stored.
        """

        params = self._get_instruction_params()
        output_address = self._memory[self._instruction_pointer + 3]
        self._memory[output_address] = params[0] + params[1]

################################################################################

    def _multiply(self) -> None:
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two
        inputs instead of adding them. Again, the three integers after the
        opcode indicate where the inputs and outputs are, not their values.
        """

        params = self._get_instruction_params()
        output_address = self._memory[self._instruction_pointer + 3]
        self._memory[output_address] = params[0] * params[1]

################################################################################

    def _save_input(self) -> None:
        """
        Opcode 3 takes a single integer as input and saves it to the position
        given by its only parameter.
        """

        output_address = self._memory[self._instruction_pointer + 1]
        self._memory[output_address] = self._input_values[0]
        del self._input_values[0]

################################################################################

    def _write_output(self) -> None:
        """
        Opcode 4 outputs the value of its only parameter.
        """

        param = self._get_instruction_params()[0]
        self._output_values.append(param)

################################################################################

    def _jump_if_true(self) -> None:
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero, it sets
        the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing.
        """

        params = self._get_instruction_params()

        if params[0] != 0:
            self._instruction_pointer = params[1]
            # avoid automatic instruction pointer jump to the next instruction
            self._auto_jump_flag = False

################################################################################

    def _jump_if_false(self) -> None:
        """
        Opcode 6 is jump-if-false: if the first parameter is zero, it sets the
        instruction pointer to the value from the second parameter. Otherwise,
        it does nothing.
        """

        params = self._get_instruction_params()

        if params[0] == 0:
            self._instruction_pointer = params[1]
            # avoid automatic instruction pointer jump to the next instruction
            self._auto_jump_flag = False

################################################################################

    def _less_than(self) -> None:
        """
        Opcode 7 is less than: if the first parameter is less than the second
        parameter, it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.
        """

        params = self._get_instruction_params()
        output_address = self._memory[self._instruction_pointer + 3]

        if params[0] < params[1]:
            self._memory[output_address] = 1
        else:
            self._memory[output_address] = 0

################################################################################

    def _equals(self) -> None:
        """
        Opcode 8 is equals: if the first parameter is equal to the second
        parameter, it stores 1 in the position given by the third parameter.
        Otherwise, it stores 0.
        """

        params = self._get_instruction_params()
        output_address = self._memory[self._instruction_pointer + 3]

        if params[0] == params[1]:
            self._memory[output_address] = 1
        else:
            self._memory[output_address] = 0

################################################################################

    def _exit(self) -> None:
        """
        Opcode 99 means that the program is finished and should immediately
        halt.
        """

        self._exit_flag = True

################################################################################