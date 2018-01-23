#!/usr/bin/env python3

"""
--- Day 13: ---

Note: Too late did I realize this is a glorified version of Eratosthenes' Sieve
and could be implemented as such.
The brute force version was fun, but the second part was basically impossible
without discovering the rules and applying them. Oh well.

The rules can be still be simplified further if you're inpatient. I'm not.

Note that this is needlessly complicated
"""

import itertools

INPUT_FILE = 'input_day13.txt'

TEST_INPUT = """0: 3
1: 2
4: 4
6: 4"""


class Player:
    """
    The entity who moves through the Firewall, Layer by Layer.
    It gets a penalty equal to depth * scan_area every time it is caught
    by a scanner.
    """
    _depth = 0
    _penalty = 0

    def respawn(self):
        """ Restart the player into their initial state. """
        self._depth = 0
        self._penalty = 0

    def run_through(self, firewall, hard_mode=False):
        """
        RUN!
        @hard_mode = Quit running on being caught and return first penalty.
        """
        for depth in range(firewall.depth + 1):
            if firewall.catch(self._depth):
                penalty = firewall.scan_range(depth) * depth
                # print("Layer {}: Player penalty: {}.".format(depth, penalty))
                self._penalty += penalty
                if hard_mode:
                    # being caught at depth == 0 incurs 0*range penalty, so add
                    # extra penalty to avoid this situation going unpunished.
                    return self._penalty + 100
            firewall.move_scanners()
            self._depth += 1

        return self._penalty

    def play_to_win(self, firewall):
        """ Simulate running through the firewall until the packet doesn't get
        caught at all.
        EDIT: Play by the rules to speed this up and only run when you've
        calculated nobody catches you. """
        penalty = 1
        delay = 1
        rules = self.play_smart()
        num_generator = self.next_number(rules)
        while penalty:
            delay = next(num_generator)
            # This is now only for the confirmation that we got the rules right.
            # Not really needed once you self.play_smart()! ;)
            # still takes a while, though.
            self.respawn()
            firewall.restart()
            firewall.move_scanners(delay)
            penalty = self.run_through(firewall, hard_mode=True)
            # delay += 1

        return delay

    @staticmethod
    def next_number(rules):
        """ Yield the next number sieved through the rules. """
        rules = sorted(list(rules))
        for i in itertools.count(start=1):
            cont = False

            for mod, remainder in rules:
                if i % mod == remainder:
                    cont = True
                    break
            if cont:
                continue
            yield i

    @staticmethod
    def play_smart():
        """
        Find the rules to filter through the layers. Once we have all rules,
        it should be easy enough to just output the first number the generator
        gives us as the delay we have to wait before running.
        """
        rules = set()
        layers = parse_input(get_input())
        for depth, scan_range in sorted(layers.items()):
            mod = (scan_range - 1) * 2
            remain = (mod + mod - depth) % mod
            rules.add((mod, remain))
        return rules


class Firewall:
    """
    Represents a firewall with N Layers, each with a Scanner going up and down
    its range (scan area). Player then runs through this firewall while Scanners
    are detecting the Player, incurring a penalty if he's caught.
    """

    class Scanner:
        """ Security scanner, scanning the Layer range. """
        scan_range = 0
        position = 0
        rising = True

        def __init__(self, scan_range):
            self.scan_range = scan_range

        def restart(self):
            """ restart the scanner. """
            self.position = 0
            self.rising = True

        def move(self):
            """ Make one step up or down the range. """
            movement = 1 if self.rising else -1
            if 0 <= self.position + movement < self.scan_range:
                self.position += movement
            else:
                self.rising = not self.rising
                self.position += -movement

    _layers = {}

    def __init__(self, layers):
        """ initialize map of @layers into self._layers """
        for depth, scan_range in layers.items():
            scanner = self.Scanner(scan_range=scan_range)
            self._layers[depth] = scanner

    def restart(self):
        """ Restart the firewall to its initial state.
        Basically just sets all scanners to position 0 """
        for scanner in self._layers.values():
            scanner.restart()

    @property
    def depth(self):
        """ Firewall has N layers on various depths. Get the deepest one. """
        return max(self._layers.keys())

    def scan_range(self, layer):
        """ get the scan range on the specific layer. """
        if layer not in self._layers:
            return 0
        return self._layers[layer].scan_range

    def catch(self, position):
        """ Does the scanner on this layer catch the player moving through? """
        # No scanner - no collision:
        if position not in self._layers:
            return False
        # collision iff Scanner is on 0
        return self._layers[position].position == 0

    def move_scanners(self, times=1):
        """
        Every picosecond, the scanner moves up and down through its range.
        This method does 1 such step with all the scanners.
        """
        for _i in range(times):
            for scanner in self._layers.values():
                scanner.move()


def get_input():
    """
    Read the input that indicates the firewall depths and ranges.
    Looks like a lot of lines such as '2: 14'
    """
    # return TEST_INPUT.split('\n')
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """
    Parse input lines such as '2: 14' into dict.
    This example indicates firewall layer in depth 2 has range 14.
    """
    m = {}
    for line in lines:
        key, value = line.strip().split(': ')
        m[int(key)] = int(value)
    return m


def main():
    """ Calculate the distance moved in the hex grid """
    layer_ranges = parse_input(get_input())
    firewall = Firewall(layer_ranges)
    player = Player()
    penalty = player.run_through(firewall)
    print("The severity of the trip through firewall is {}".format(penalty))

    firewall.restart()
    player.respawn()
    delay = player.play_to_win(firewall)
    print("The delay we have to wait is {} picoseconds.".format(delay))

    return


if __name__ == '__main__':
    main()
