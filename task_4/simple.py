import time

def get_dist_to_bytes(pellets_now):
    # find the closest powers of 2
    for i in range(0, 1028):
        byte_low = pow(2, i)
        byte_high = pow(2, i + 1)
        if byte_low <= pellets_now <= byte_high:
            dist_low = pellets_now - byte_low
            dist_high = byte_high - pellets_now
            return dist_low, dist_high
    # print("Couldnt find bytes distance???")
    raise Warning("Couldnt find bytes distance???")



def solution(n):

    n = int(n)
    step = 0
    is_solved = False

    while not is_solved:
        dist_l, dist_h = get_dist_to_bytes(n)

        if n % 2 == 0:
            # divide if possible
            n = n/2

        else:
            # get byte distances
            if dist_h == 1:
                # add
                n += 1
            elif dist_l == 1:
                # substr
                n -= 1
            else:
                # try next values and their distances
                dist_h_l, dist_h_h = get_dist_to_bytes(n+1)
                dist_l_l, dist_l_h = get_dist_to_bytes(n-1)

                # if the next values are byte then just go for them!
                if dist_l_l == 0 or dist_l_h == 0:
                    n -= 1
                elif dist_h_l == 0 or dist_h_h == 0:
                    n += 1

                # dont select the next value if the next one is ODD
                elif (n-1)%2 == 0:
                    n -= 1

                elif (n+1)%2 == 0:
                    n += 1

                # follow to the next bytes
                elif dist_l_l == 1:
                    n -= 1
                elif dist_l_h == 1:
                    n += 1

                else:
                    n -= 1

        # print 'n', n
        step += 1
        is_solved = n==1

    # print n, 'step', step
    return step





if __name__ == "__main__":
    test_inputs = ['4', '15', '77', '135', '217', '314', '2137', '213789']
    test_outputs = [2, 5, 9, 9, 11, 11, 15, 25]
    # test_inputs = ['135']
    # test_outputs = [9]
    for ipt, opt in zip(test_inputs, test_outputs):
        # print 'ipt', ipt, 'sol', sol, 'opt', opt
        print 'ipt', ipt
        sol = solution(ipt)
        # sol = None
        print('sol', sol, 'opt', opt)
        print( '\n')
