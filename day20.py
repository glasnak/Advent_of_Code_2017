#!/usr/bin/env python3

"""
--- Day 20: Particle Swarm ---
"""

from collections import namedtuple

Particle = namedtuple('Particle', 'p v a')
INPUT_FILE = 'input_day20.txt'


def get_input():
    """ Read the input lines. """
    with open(INPUT_FILE) as f:
        return f.readlines()


def parse_input(lines):
    """ return lines parsed into the Particle structure.
    input line example:
    p=<-671,1794,-1062>, v=<46,87,41>, a=<-1,-17,1>
    """
    particles = []
    for i, line in enumerate(lines):
        pva = [x[3:-1] for x in line.strip().split(', ')]
        xyz = []
        for x in pva:
            xyz.append([int(n) for n in x.split(',')])
        particles.append(Particle(*xyz))

    return particles


def distance(xyz):
    """ return manhattan distance from zero """
    return sum(abs(n) for n in xyz)


def solve(particles):
    """ solve the puzzle part 1, the closest particle. """
    for _ in range(500):
        update(particles)
    closest = 0
    min_distance = distance(particles[0].p)

    for i, particle in enumerate(particles):
        d = distance(particle.p)
        if d < min_distance:
            closest = i
            min_distance = d

    return closest, min_distance


def update(particles):
    """ one step of all the particles: v+=a; p+=v; """
    for particle in particles:
        for i in range(3):
            particle.v[i] += particle.a[i]
            particle.p[i] += particle.v[i]


def collide(particles):
    """
    Find the closest particle in the long-term.
    100 guaranteed to be 'long-term'.
    """

    for _ in range(100):
        update(particles)
        # get current positions:
        positions = [particle.p for particle in particles]
        # find where they collide by checking for positions up to this Nth particle
        collision_positions = [particle.p for i, particle in enumerate(particles) if particle.p in positions[:i]]
        # finally, remove the ones that have collided
        particles = [particle for particle in particles if particle.p not in collision_positions]

    return len(particles)


def main():
    """ Collide particles """
    particles = parse_input(get_input())
    closest = solve(particles)
    print("Closest particle - distance pair is {}".format(closest))

    particles = parse_input(get_input())
    remaining = collide(particles)
    print("{} particles are left after collisions.".format(remaining))

    return


if __name__ == '__main__':
    main()
