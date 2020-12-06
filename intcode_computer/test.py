__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from unittest import TestCase, main
from intcode_computer.computer import IntcodeComputer
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

################################################################################

    def test_whole_memory(self):
        computer = IntcodeComputer()
        for test in self.TESTS_WHOLE_MEMORY:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([int(data.strip())
                                 for data in f.read().strip().split(',')])
                computer.load_program(program)
                computer.run_program()
                self.assertEqual(computer._memory,
                                 test[self.KEY_EXPECTED_RESULT])

################################################################################

    def test_output(self):
        computer = IntcodeComputer()
        for test in self.TESTS_OUTPUT:
            with open(test[self.KEY_FILE_PATH], 'r') as f:
                program = tuple([int(data.strip())
                                 for data in f.read().strip().split(',')])
                computer.load_program(program)
                [computer.load_input(value) for value in test[self.KEY_INPUT]]
                computer.run_program()
                self.assertTrue(
                    len(test[self.KEY_OUTPUT]) == len(computer.get_output()))
                self.assertTrue(
                    all([computer.get_output()[i] == test[self.KEY_OUTPUT][i]
                         for i in range(len(computer.get_output()))]))

################################################################################

    def test_day_02_puzzle_1(self):
        with open("../day_02/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            computer = IntcodeComputer()
            self.assertEqual(_set_and_run(computer, program, NOUN, VERB),
                             3654868)

################################################################################

    def test_day_02_puzzle_2(self):
        with open("../day_02/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            computer = IntcodeComputer()
            combination = [
                (noun, verb)
                for noun in range(NOUN_RANGE)
                for verb in range(VERB_RANGE)
                if _set_and_run(computer, program, noun, verb)
                   == GRAVITY_ASSIST_GOAL][0]
            self.assertEqual(100 * combination[0] + combination[1], 7014)

################################################################################

    def test_day_05_puzzle_1(self):
        with open("../day_05/input.txt", 'r') as f:
            program = tuple([int(data.strip())
                             for data in f.read().strip().split(',')])
            computer = IntcodeComputer()
            computer.load_program(program)
            computer.load_input(1)
            computer.run_program()
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
            computer.run_program()
            self.assertEqual(computer.get_output()[0], 4655956)

################################################################################

if __name__ == '__main__':
    main()

################################################################################
