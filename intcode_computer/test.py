__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from unittest import TestCase, main
from intcode_computer.computer import IntcodeComputer, Condition
from day_02.day_02 import _set_and_run, NOUN, NOUN_RANGE, VERB, VERB_RANGE, \
    GRAVITY_ASSIST_GOAL

################################################################################

class TestStringMethods(TestCase):
    KEY_FILE_PATH = "FILE_PATH"
    KEY_EXPECTED_RESULT = "EXPECTED_RESULT"

    TESTS_WHOLE_MEMORY = [{
        KEY_FILE_PATH: "tests/test_02_01.txt",
        KEY_EXPECTED_RESULT: [1, 0, 0, 2, 99]
    }, {
        KEY_FILE_PATH: "tests/test_02_02.txt",
        KEY_EXPECTED_RESULT: [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    }, {
        KEY_FILE_PATH: "tests/test_02_03.txt",
        KEY_EXPECTED_RESULT: [2, 0, 0, 0, 99]
    }, {
        KEY_FILE_PATH: "tests/test_02_04.txt",
        KEY_EXPECTED_RESULT: [2, 3, 0, 6, 99]
    }, {
        KEY_FILE_PATH: "tests/test_02_05.txt",
        KEY_EXPECTED_RESULT: [2, 4, 4, 5, 99, 9801]
    }, {
        KEY_FILE_PATH: "tests/test_02_06.txt",
        KEY_EXPECTED_RESULT: [30, 1, 1, 4, 2, 5, 6, 0, 99]
    }, {
        KEY_FILE_PATH: "tests/test_05_02.txt",
        KEY_EXPECTED_RESULT: [1002, 4, 3, 4, 99]
    }, {
        KEY_FILE_PATH: "tests/test_05_03.txt",
        KEY_EXPECTED_RESULT: [1101, 100, -1, 4, 99]
    }]

    KEY_INPUT = "INPUT"
    KEY_OUTPUT = "OUTPUT"

    TESTS_OUTPUT = [{
        KEY_FILE_PATH: "tests/test_05_01.txt",
        KEY_INPUT: [23],
        KEY_OUTPUT: [23]
    }, {
        KEY_FILE_PATH: "tests/test_05_04.txt",
        KEY_INPUT: [8],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_04.txt",
        KEY_INPUT: [5],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_05.txt",
        KEY_INPUT: [3],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_05.txt",
        KEY_INPUT: [8],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_05.txt",
        KEY_INPUT: [19],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_06.txt",
        KEY_INPUT: [8],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_06.txt",
        KEY_INPUT: [7],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_07.txt",
        KEY_INPUT: [-5],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_07.txt",
        KEY_INPUT: [8],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_07.txt",
        KEY_INPUT: [23],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_08.txt",
        KEY_INPUT: [0],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_08.txt",
        KEY_INPUT: [89],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_09.txt",
        KEY_INPUT: [0],
        KEY_OUTPUT: [0]
    }, {
        KEY_FILE_PATH: "tests/test_05_09.txt",
        KEY_INPUT: [-42],
        KEY_OUTPUT: [1]
    }, {
        KEY_FILE_PATH: "tests/test_05_10.txt",
        KEY_INPUT: [4],
        KEY_OUTPUT: [999]
    }, {
        KEY_FILE_PATH: "tests/test_05_10.txt",
        KEY_INPUT: [8],
        KEY_OUTPUT: [1000]
    }, {
        KEY_FILE_PATH: "tests/test_05_10.txt",
        KEY_INPUT: [9],
        KEY_OUTPUT: [1001]
    }]

    KEY_PHASE_SETTINGS_SEQUENCE = "PHASE_SETTINGS_SEQUENCE"
    KEY_THRUSTER_SIGNAL = "THRUSTER_SIGNAL"

    TESTS_AMPLIFIERS = [{
        KEY_FILE_PATH: "tests/test_07_01.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [4, 3, 2, 1, 0],
        KEY_THRUSTER_SIGNAL: 43210
    }, {
        KEY_FILE_PATH: "tests/test_07_02.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [0,1,2,3,4],
        KEY_THRUSTER_SIGNAL: 54321
    }, {
        KEY_FILE_PATH: "tests/test_07_03.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [1,0,4,3,2],
        KEY_THRUSTER_SIGNAL: 65210
    }, {
        KEY_FILE_PATH: "../day_07/input.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [3,1,2,0,4],
        KEY_THRUSTER_SIGNAL: 14902
    }]

    TESTS_AMPLIFIERS_FEEDBACK_LOOP = [{
        KEY_FILE_PATH: "tests/test_07_04.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [9,8,7,6,5],
        KEY_THRUSTER_SIGNAL: 139629729
    }, {
        KEY_FILE_PATH: "tests/test_07_05.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [9,7,8,5,6],
        KEY_THRUSTER_SIGNAL: 18216
    }, {
        KEY_FILE_PATH: "../day_07/input.txt",
        KEY_INPUT: 0,
        KEY_PHASE_SETTINGS_SEQUENCE: [9,6,7,5,8],
        KEY_THRUSTER_SIGNAL: 6489132
    }]

################################################################################

    def test_whole_memory(self):
        for test in self.TESTS_WHOLE_MEMORY:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([
                    int(data.strip()) for data in f.read().strip().split(',')])
                computer = IntcodeComputer()
                computer.load_program(program)
                computer.start()
                computer.join()
                self.assertEqual(
                    computer._memory, test[self.KEY_EXPECTED_RESULT])

################################################################################

    def test_output(self):
        for test in self.TESTS_OUTPUT:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([
                    int(data.strip()) for data in f.read().strip().split(',')])
                computer = IntcodeComputer()
                computer.load_program(program)
                [computer.load_input(value) for value in test[self.KEY_INPUT]]
                computer.start()
                computer.join()
                self.assertTrue(
                    len(test[self.KEY_OUTPUT]) == len(computer.get_output()))
                self.assertTrue(
                    all([computer.get_output()[i] == test[self.KEY_OUTPUT][i]
                         for i in range(len(computer.get_output()))]))

################################################################################

    def test_amplifiers(self):
        for test in self.TESTS_AMPLIFIERS:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([
                    int(data.strip()) for data in f.read().strip().split(',')])
                input_signal = test[self.KEY_INPUT]

                for setting in test[self.KEY_PHASE_SETTINGS_SEQUENCE]:
                    computer = IntcodeComputer()
                    computer.load_program(program)
                    computer.load_input(setting)
                    computer.load_input(input_signal)
                    computer.start()
                    computer.join()
                    output_signal = computer.get_output()[-1]
                    input_signal = output_signal
                self.assertEqual(output_signal, test[self.KEY_THRUSTER_SIGNAL])

################################################################################

    def test_amplifiers_feedback_loop(self):
        for test in self.TESTS_AMPLIFIERS:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([
                    int(data.strip()) for data in f.read().strip().split(',')])
                input_signal = test[self.KEY_INPUT]
                phase_settings = test[self.KEY_PHASE_SETTINGS_SEQUENCE]
                output_condition = Condition()
                computers = [
                    IntcodeComputer(output_condition)
                    for _ in range(len(phase_settings))]
                [computer.load_program(program) for computer in computers]
                [computers[i].load_input(phase_settings[i])
                 for i in range(len(phase_settings))]
                [computer.start() for computer in computers]

                while any([computer.is_alive() for computer in computers]):
                    for computer in computers:
                        with output_condition:
                            computer.load_input(input_signal)
                            output_condition.wait()
                        input_signal = computer.get_output()[-1]

                output_signal = computers[-1].get_output()[-1]
                self.assertEqual(output_signal, test[self.KEY_THRUSTER_SIGNAL])

################################################################################

    def test_day_02_puzzle_1(self):
        with open("../day_02/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            self.assertEqual(_set_and_run(program, NOUN, VERB), 3654868)

################################################################################

    def test_day_02_puzzle_2(self):
        with open("../day_02/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            combination = [
                (noun, verb)
                for noun in range(NOUN_RANGE)
                for verb in range(VERB_RANGE)
                if _set_and_run(program, noun, verb) == GRAVITY_ASSIST_GOAL][0]
            self.assertEqual(100 * combination[0] + combination[1], 7014)

################################################################################

    def test_day_05_puzzle_1(self):
        with open("../day_05/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            computer = IntcodeComputer()
            computer.load_program(program)
            computer.load_input(1)
            computer.start()
            computer.join()
            output = computer.get_output()
            self.assertTrue(all([value == 0 for value in output[:-1]]))
            self.assertEqual(output[-1], 14522484)

################################################################################

    def test_day_05_puzzle_2(self):
        with open("../day_05/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            computer = IntcodeComputer()
            computer.load_program(program)
            computer.load_input(5)
            computer.start()
            computer.join()
            self.assertEqual(computer.get_output()[0], 4655956)

################################################################################

if __name__ == '__main__':
    main()

################################################################################
