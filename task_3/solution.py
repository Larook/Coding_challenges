
class GearConstruction:
    pegs_locations = []
    pegs_distances = []
    radii = []
    impossible_response = -1, -1

    def __init__(self, pegs):
        self.pegs_locations = pegs

    def get_distances_pegs(self):
        """
        calculate distances between pegs
        """
        self.pegs_distances = []
        for i in range(1, len(self.pegs_locations)):
            self.pegs_distances.append(self.pegs_locations[i] - self.pegs_locations[i - 1])
        return self.pegs_distances

    def is_data_fine(self):
        # safety checks
        if not 2 <= len(self.pegs_locations) <= 20:
            return False
        if max(self.pegs_locations) > 10000 or min(self.pegs_locations) < 1:
            return False

        # check if in ascending order
        tmp = 0
        for peg in self.pegs_locations:
            if type(peg) != int or peg <= 0:
                return False
            if peg < tmp:
                return False
            else:
                tmp = peg

        # check if distances are feasible
        for distance in self.pegs_distances:
            if distance <= 0:
                return False

        return True

    def are_radii_fine(self, radius):
        """
        Calculates all the radii and returns False if the set of radii is impossible to get
        :param radius: radius of the first cog
        :return: is_problem
        """

        self.radii = [radius]
        for i, distance in enumerate(self.pegs_distances):
            # for distance in self.pegs_distances:
            self.radii.append(distance - self.radii[i])

        for r in self.radii:
            if r < 1:
                return False

        # check if all the radii make the distance between the pegs
        len_pegs = self.pegs_locations[-1] - self.pegs_locations[0]
        len_radii = sum(self.radii) + sum(self.radii[1:-1])
        if int(round(len_pegs)) != int(round(len_radii)):
            return False

        return True


def solution(pegs):
    """
    :param pegs: list of distances between the pegs (centers of the cogs) ~variable length
    :return (rad_num, rad_denom): tuple of numerator and denominator of the radius_0 of the first cog
    """
    gears = GearConstruction(pegs)
    if not gears.is_data_fine():
        return gears.impossible_response

    distances = gears.get_distances_pegs()
    """
    sequentially add and subtract the distances between pegs to get a final form of the radius_0 -- either half or 1.5
    """
    rad_fraction = distances[0]
    for i in range(1, len(distances)):
        # start by minus
        if i % 2 == 1:
            rad_fraction -= distances[i]
        else:
            rad_fraction += distances[i]

    if rad_fraction <= 0 or int(round(rad_fraction)) != int(rad_fraction):
        return gears.impossible_response

    """
    rad_fraction is an positive integer from now on
    """
    rad_fraction = int(rad_fraction)
    if len(distances) % 2 == 1:
        # when odd number -- the rad_fraction = 1.5 radius_0
        radius_0 = rad_fraction / 1.5
        if rad_fraction % 3 == 0:
            num = rad_fraction * 2 / 3
            denom = 1
        else:
            num = rad_fraction * 2
            denom = 3
    else:
        # when even number -- the rad_fraction = 0.5 radius_0
        radius_0 = rad_fraction / 0.5
        num = rad_fraction * 2
        denom = 1

    radii_fine = gears.are_radii_fine(radius_0)
    if not radii_fine:
        return gears.impossible_response

    if num / denom < 1:
        return gears.impossible_response

    return int(round(num)), int(round(denom))


if __name__ == "__main__":
    # tmp = 52./3
    # tmp = 16./6
    tmp = 17. / 4
    tmp = 17. / 8
    tmp = 17. / 9
    tmp = 17. / 8
    # a, b = get_numerator_denominator(tmp)

    # frac = Fraction(22, 11)
    # a, b = frac.numerator, frac.denominator
    # print tmp, a, b
    # exit(0)

    # test_0 = solution([4, 30])
    print '\n------------------'
    # print solution([4, 30])
    # print solution([4, 30.12])
    # print solution([-4, 30])
    # print solution([30, 4])
    #
    # print '\n------------------'
    print solution([4, 30, 50])
    print solution([4, 17, 50])
    print solution([30, 4, 50])

    print '\n------------------'
    # print solution([1, 2, 3, 4, 5, 12])
    # print solution([4.1, 30, 50])
    # print solution([30, 4, 50])

    # print solution([4, 30, 50, 70, 100])
    print solution([4, 30, 50, 70, 91])
    # print solution([4.12, 30, 50, 70, 91])
    # print solution([44, 30, 50, 70, 91])
    #
    # test_1 = solution([4, 30, 50])
    # assert test_1 == (12, 1)
    # print test_1
    #
    # test_2 = solution([4, 17, 50])
    # assert test_2 == (-1, -1)
    # print test_2

    """
    code as it is now doesn't pass some of the hidden tests

    maybe just calculate all of the radii and throw an error when the radius is impossible to build (e.g <1)
    OK

    maybe double check if the distance made by the radii is covering the distance of pegs
    OK

    Still tests 6 and 9 are causing problems -- they are expecting sth different than [-1, -1]
    Test 6 works well with the num, denom function!  But loosing tests 4, 5, 10 then

    used library Fractions -- now only test 9 is not passing

    Problem was with a typo in is_data_fine
    """


