__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

################################################################################

class IntcodeComputer(object):
    OPCODE_ADD = 1
    OPCODE_MULTIPLY = 2
    OPCODE_EXIT = 99

    KEY_PARAMS_COUNT = "params_count"
    KEY_RUN_FUNCTION = "run_function"

################################################################################

    def __init__(self):
        """
        Creates the intcode computer instance with undefined memory, instruction
        pointer and exit flag. Maps the correct methods to given opcodes.
        """

        self._instructions = {
            self.OPCODE_ADD: {
                self.KEY_PARAMS_COUNT: 3,
                self.KEY_RUN_FUNCTION: self._add
            },
            self.OPCODE_MULTIPLY: {
                self.KEY_PARAMS_COUNT: 3,
                self.KEY_RUN_FUNCTION: self._multiply
            },
            self.OPCODE_EXIT: {
                self.KEY_PARAMS_COUNT: 0,
                self.KEY_RUN_FUNCTION: self._exit
            }
        }

        self._memory = None
        self._instruction_pointer = None
        self._exit_flag = None

################################################################################

    def load_program(self, file_path: str) -> None:
        """
        Loads the given program in the memory, sets the instruction pointer at
        the beginning of the memory and clears the exit flag.

        :param file_path: path to the file with the program
        """

        with open(file_path, 'r') as f:
            self._memory = [int(data.strip())
                            for data in f.read().strip().split(',')]
            self._instruction_pointer = 0
            self._exit_flag = False

################################################################################

    def run_program(self) -> None:
        """
        Runs the program loaded in the computer.
        """

        while not self._exit_flag:
            opcode = self._memory[self._instruction_pointer]
            self._instructions[opcode][self.KEY_RUN_FUNCTION]()
            self._instruction_pointer += self._instructions[opcode][self.KEY_PARAMS_COUNT] + 1

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

    def _add(self) -> None:
        """
        Opcode 1 adds together numbers read from two positions and stores the
        result in a third position. The three integers immediately after the
        opcode tell you these three positions - the first two indicate the
        positions from which you should read the input values, and the third
        indicates the position at which the output should be stored.
        """

        param_1 = self._memory[self._instruction_pointer + 1]
        param_2 = self._memory[self._instruction_pointer + 2]
        output = self._memory[self._instruction_pointer + 3]
        self._memory[output] = self._memory[param_1] + self._memory[param_2]

################################################################################

    def _multiply(self) -> None:
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two
        inputs instead of adding them. Again, the three integers after the
        opcode indicate where the inputs and outputs are, not their values.
        """

        param_1 = self._memory[self._instruction_pointer + 1]
        param_2 = self._memory[self._instruction_pointer + 2]
        output = self._memory[self._instruction_pointer + 3]
        self._memory[output] = self._memory[param_1] * self._memory[param_2]

################################################################################

    def _exit(self) -> None:
        """
        Opcode 99 means that the program is finished and should immediately
        halt.
        """

        self._exit_flag = True

################################################################################