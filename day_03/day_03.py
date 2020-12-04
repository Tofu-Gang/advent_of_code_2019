__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import Tuple, List, Union, Dict
from itertools import combinations

"""
--- Day 3: Crossed Wires ---
The gravity assist was successful, and you're well on your way to the Venus 
refuelling station. During the rush back on Earth, the fuel management system 
wasn't completely installed, so that's next on the priority list.
"""

################################################################################

UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'

INDEX_X = 0
INDEX_Y = 1
DIRECTION_INDEX = 0
DISTANCE_INDEX = 1

DIRECTIONS = {
    UP: (0, 1),
    DOWN: (0, -1),
    LEFT: (-1, 0),
    RIGHT: (1, 0)
}

KEY_FROM = "FROM"
KEY_TO = "TO"
KEY_FIXED_COORDINATE = "FIXED_COORDINATE"
KEY_VARIABLE_COORDINATE = "VARIABLE_COORDINATE"
KEY_WIRE_LENGTH = "WIRE_LENGTH"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Opening the front panel reveals a jumble of wires. Specifically, two wires
    are connected to a central port and extend outward on a grid. You trace the
    path each wire takes as it leaves the central port, one wire per line of
    text (your puzzle input).

    The wires twist and turn, but the two wires occasionally cross paths. To fix
    the circuit, you need to find the intersection point closest to the central
    port. Because the wires are on a grid, use the Manhattan distance for this
    measurement. While the wires do technically cross right at the central port
    where they both start, this point does not count, nor does a wire count as
    crossing with itself.

    For example, if the first wire's path is R8,U5,L5,D3, then starting from the
    central port (o), it goes right 8, up 5, left 5, and finally down 3:

    ...........
    ...........
    ...........
    ....+----+.
    ....|....|.
    ....|....|.
    ....|....|.
    .........|.
    .o-------+.
    ...........

    Then, if the second wire's path is U7,R6,D4,L4, it goes up 7, right 6, down
    4, and left 4:

    ...........
    .+-----+...
    .|.....|...
    .|..+--X-+.
    .|..|..|.|.
    .|.-X--+.|.
    .|..|....|.
    .|.......|.
    .o-------+.
    ...........

    These wires cross at two locations (marked X), but the lower-left one is
    closer to the central port: its distance is 3 + 3 = 6.

    Here are a few more examples:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = distance 159
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = distance 135

    What is the Manhattan distance from the central port to the closest
    intersection?

    The answer should be 870.
    """

    with open("day_03/input.txt", 'r') as f:
        wire_1 = _make_wire_vectors(f.readline())
        wire_2 = _make_wire_vectors(f.readline())

        print(min([abs(_get_intersection(vector_1, vector_2)[0])
                   + abs(_get_intersection(vector_1, vector_2)[1])
                   for vector_1 in wire_1
                   for vector_2 in wire_2
                   if _get_intersection(vector_1, vector_2) is not None]))

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    It turns out that this circuit is very timing-sensitive; you actually need
    to minimize the signal delay.

    To do this, calculate the number of steps each wire takes to reach each
    intersection; choose the intersection where the sum of both wires' steps is
    lowest. If a wire visits a position on the grid multiple times, use the
    steps value from the first time it visits that position when calculating the
    total value of a specific intersection.

    The number of steps a wire takes is the total number of grid squares the
    wire has entered to get to that location, including the intersection being
    considered. Again consider the example from above:

    ...........
    .+-----+...
    .|.....|...
    .|..+--X-+.
    .|..|..|.|.
    .|.-X--+.|.
    .|..|....|.
    .|.......|.
    .o-------+.
    ...........

    In the above example, the intersection closest to the central port is
    reached after 8+5+5+2 = 20 steps by the first wire and 7+6+4+3 = 20 steps by
    the second wire for a total of 20+20 = 40 steps.

    However, the top-right intersection is better: the first wire takes only
    8+5+2 = 15 and the second wire takes only 7+6+2 = 15, a total of 15+15 = 30
    steps.

    Here are the best steps for the extra examples from above:

    R75,D30,R83,U83,L12,D49,R71,U7,L72
    U62,R66,U55,R34,D71,R55,D58,R83 = 610 steps
    R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
    U98,R91,D20,R16,D67,R40,U7,R15,U6,R7 = 410 steps

    What is the fewest combined steps the wires must take to reach an
    intersection?

    The answer should be 13698.
    """

    with open("day_03/input.txt", 'r') as f:
        wire_1 = _make_wire_vectors(f.readline())
        wire_2 = _make_wire_vectors(f.readline())

        print(min([vector_1[KEY_WIRE_LENGTH]
                   - abs(vector_1[KEY_TO][vector_1[KEY_VARIABLE_COORDINATE]]
                         - _get_intersection(vector_1, vector_2)
                         [vector_1[KEY_VARIABLE_COORDINATE]])
                   + vector_2[KEY_WIRE_LENGTH]
                   - abs(vector_2[KEY_TO][vector_2[KEY_VARIABLE_COORDINATE]]
                         - _get_intersection(vector_1, vector_2)
                         [vector_2[KEY_VARIABLE_COORDINATE]])
                   for vector_1 in wire_1
                   for vector_2 in wire_2
                   if _get_intersection(vector_1, vector_2) is not None]))

################################################################################

def _make_wire_vectors(line: str) -> List[Dict]:
    """
    Creates list of wire segments.

    :param line: wire instructions
    :return: list of wire segments
    """

    instructions = [(instruction.strip()[0], int(instruction.strip()[1:]))
                    for instruction in line.strip().split(',')]
    vectors = []

    for i in range(len(instructions)):
        instruction = instructions[i]
        direction = instruction[DIRECTION_INDEX]
        distance = instruction[DISTANCE_INDEX]
        fixed_coordinate = DIRECTIONS[direction].index(0)
        variable_coordinate = (fixed_coordinate + 1) % 2

        try:
            point_from = vectors[i - 1][KEY_TO]
            wire_length = vectors[i - 1][KEY_WIRE_LENGTH] + distance
        except IndexError:
            point_from = (0, 0)
            wire_length = distance

        point_to_x = point_from[INDEX_X] \
                     + DIRECTIONS[direction][INDEX_X] \
                     * distance
        point_to_y = point_from[INDEX_Y] \
                     + DIRECTIONS[direction][INDEX_Y] \
                     * distance

        vectors.append({
            KEY_FROM: point_from,
            KEY_TO: (point_to_x, point_to_y),
            KEY_FIXED_COORDINATE: fixed_coordinate,
            KEY_VARIABLE_COORDINATE: variable_coordinate,
            KEY_WIRE_LENGTH: wire_length
        })

    return vectors

################################################################################

def _get_intersection(vector_1: Dict, vector_2: Dict) \
        -> Union[Tuple[int, int], None]:
    """
    Determines whether vectors from the parameters intersect or not. If so,
    the intersection point is returned.

    :param vector_1: vector 1
    :param vector_2: vector 2
    :return: intersection point or None (if vectors do not intersect)
    """

    fixed_coordinate_1 = vector_1[KEY_FIXED_COORDINATE]
    fixed_coordinate_2 = vector_2[KEY_FIXED_COORDINATE]
    variable_coordinate_1 = vector_1[KEY_VARIABLE_COORDINATE]
    variable_coordinate_2 = vector_2[KEY_VARIABLE_COORDINATE]

    limit_1_from = min(vector_1[KEY_FROM][variable_coordinate_1],
                       vector_1[KEY_TO][variable_coordinate_1])
    limit_1_to = max(vector_1[KEY_FROM][variable_coordinate_1],
                     vector_1[KEY_TO][variable_coordinate_1])
    limit_2_from = min(vector_2[KEY_FROM][variable_coordinate_2],
                       vector_2[KEY_TO][variable_coordinate_2])
    limit_2_to = max(vector_2[KEY_FROM][variable_coordinate_2],
                     vector_2[KEY_TO][variable_coordinate_2])

    if fixed_coordinate_1 == fixed_coordinate_2:
        return None
    elif limit_1_from \
            <= vector_2[KEY_FROM][fixed_coordinate_2] \
            <= limit_1_to \
            and limit_2_from \
            <= vector_1[KEY_FROM][fixed_coordinate_1] \
            <= limit_2_to:
        # determine which is x coordinate and which is y coordinate
        if fixed_coordinate_1 < fixed_coordinate_2:
            return (vector_1[KEY_FROM][fixed_coordinate_1],
                    vector_2[KEY_FROM][fixed_coordinate_2])
        else:
            return (vector_2[KEY_FROM][fixed_coordinate_2],
                    vector_1[KEY_FROM][fixed_coordinate_1])
    else:
        return None

################################################################################
