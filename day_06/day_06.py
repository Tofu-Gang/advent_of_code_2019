__author__ = "Tofu Gang"
__email__ = "tofugangsw@gmail.com"

from typing import Dict, Union, List, Tuple
from sys import maxsize

"""
--- Day 6: Universal Orbit Map ---

You've landed at the Universal Orbit Map facility on Mercury. Because navigation 
in space often involves transferring between orbits, the orbit maps here are 
useful for finding efficient routes between, for example, you and Santa. You 
download a map of the local orbits (your puzzle input).
"""

################################################################################

KEY_ORBITS = "ORBITS"
KEY_VISITED = "VISITED"
KEY_DISTANCE = "DISTANCE"

CENTER_OF_MASS = "COM"
MY_ORBITER = "YOU"
SANTA_ORBITER = "SAN"

################################################################################

def puzzle_1() -> None:
    """
    --- Part One ---

    Except for the universal Center of Mass (COM), every object in space is in
    orbit around exactly one other object. An orbit looks roughly like this:

                      \
                       \
                        |
                        |
    AAA--> o            o <--BBB
                        |
                        |
                       /
                      /

    In this diagram, the object BBB is in orbit around AAA. The path that BBB
    takes around AAA (drawn with lines) is only partly shown. In the map data,
    this orbital relationship is written AAA)BBB, which means "BBB is in orbit
    around AAA".

    Before you use your map data to plot a course, you need to make sure it
    wasn't corrupted during the download. To verify maps, the Universal Orbit
    Map facility uses orbit count checksums - the total number of direct orbits
    (like the one shown above) and indirect orbits.

    Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain
    can be any number of objects long: if A orbits B, B orbits C, and C orbits
    D, then A indirectly orbits D.

    For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L

    Visually, the above map of orbits looks like this:

            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I

    In this visual representation, when two objects are connected by a line, the
    one on the right directly orbits the one on the left.

    Here, we can count the total number of orbits as follows:

    D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
    L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of
    7 orbits.
    COM orbits nothing.
    The total number of direct and indirect orbits in this example is 42.

    What is the total number of direct and indirect orbits in your map data?

    The answer should be 402879.
    """

    orbit_map = _load_orbit_map()
    count = 0

    for orbiter in orbit_map:

        while orbiter != CENTER_OF_MASS:
            orbit_center = orbit_map[orbiter][KEY_ORBITS]
            count += 1
            orbiter = orbit_center

    print(count)

################################################################################

def puzzle_2() -> None:
    """
    --- Part Two ---

    Now, you just need to figure out how many orbital transfers you (YOU) need
    to take to get to Santa (SAN).

    You start at the object YOU are orbiting; your destination is the object SAN
    is orbiting. An orbital transfer lets you move from any object to an object
    orbiting or orbited by that object.

    For example, suppose you have the following map:

    COM)B
    B)C
    C)D
    D)E
    E)F
    B)G
    G)H
    D)I
    E)J
    J)K
    K)L
    K)YOU
    I)SAN

    Visually, the above map of orbits looks like this:

                              YOU
                             /
            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN

    In this example, YOU are in orbit around K, and SAN is in orbit around I. To
    move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

    Afterward, the map of orbits looks like this:

            G - H       J - K - L
           /           /
    COM - B - C - D - E - F
                   \
                    I - SAN
                     \
                      YOU

    What is the minimum number of orbital transfers required to move from the
    object YOU are orbiting to the object SAN is orbiting? (Between the objects
    they are orbiting - not between YOU and SAN.)

    The answer should be 484.
    """

    orbit_map = _load_orbit_map()
    orbit_map[MY_ORBITER][KEY_DISTANCE] = 0
    current = MY_ORBITER

    while current != SANTA_ORBITER:
        neighbours = _get_unvisited_neighbours(current, orbit_map)

        for neighbour in neighbours:
            # set the distances
            orbit_map[neighbour][KEY_DISTANCE] \
                = min(orbit_map[current][KEY_DISTANCE] + 1,
                      orbit_map[neighbour][KEY_DISTANCE])

        try:
            # get the location with the least tentative distance
            current = sorted(
                neighbours + tuple([
                    orbiter
                    for orbiter in orbit_map
                    if orbit_map[orbiter][KEY_VISITED] is False]),
                key=lambda location: orbit_map[location][KEY_DISTANCE])[0]
            # current orbiter is visited, never process it again
            orbit_map[current][KEY_VISITED] = True
        except IndexError:
            # no unvisited locations left
            break

    # -2 because between the objects they are orbiting - not between YOU and SAN
    print(orbit_map[current][KEY_DISTANCE] - 2)

################################################################################

def _load_orbit_map() -> Dict[str, Dict[str, Union[None, str, bool, int]]]:
    """
    :return: Orbit map with data needed for both puzzles.
    """

    with open("day_06/input.txt", 'r') as f:
        data = {}
        cosmic_map = [line.strip() for line in f.readlines()]

        for orbit in cosmic_map:
            orbit_center = orbit.split(')')[0].strip()
            orbiter = orbit.split(')')[1].strip()

            data[orbiter] = {
                KEY_ORBITS: orbit_center,
                KEY_VISITED: False,
                KEY_DISTANCE: maxsize
            }

            if orbit_center not in data:
                data[orbit_center] = {
                    KEY_ORBITS: None,
                    KEY_VISITED: False,
                    KEY_DISTANCE: maxsize
                }

        return data

################################################################################

def _get_unvisited_neighbours(
        current_location: str,
        orbit_map: Dict[str, Dict[str, Union[None, str, bool, int]]]) \
        -> Tuple[str]:
    """
    Returns unvisited neighbours of the location specified in the param.

    :param current_location: location of which the unvisited neighbours are
    returned
    :param orbit_map: orbit map
    :return: unvisited neighbours of the current location
    """

    current_orbit_center = orbit_map[current_location][KEY_ORBITS]
    return tuple([
        orbiter
        for orbiter in orbit_map
        if (orbit_map[orbiter][KEY_ORBITS] == current_location
            and orbit_map[orbiter][KEY_VISITED] is False)
           or (current_orbit_center is not None
               and orbiter == current_orbit_center
               and orbit_map[current_orbit_center][KEY_VISITED] is False)])

################################################################################
