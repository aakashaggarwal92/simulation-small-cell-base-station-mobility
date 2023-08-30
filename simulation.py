import numpy as np
import random
import time
import RSL


user_stats = np.full((7, 1000), 0, dtype=int)
'''
[summary]

An array to hold user statistics for all users.

[description]

# Zeroth Row holds the whether the user is on call or not (1: Active Call, 0: Not Active)
# First Row holds the direction of movement for the user (1: East towards Small Cell, 0: West towards Base Station)
# Second Row updates call duration timer for each user
# Third Row stores updated location of the user
# Fourth Row stores serving cell name (0:BS or 1:SC)
# Fifth Row stores the RSL value of BS
# Sixth Row stores the RSL value of SC

'''
network_stats = np.full((2, 9), 0, dtype=int)
'''
[summary]

An array to hold network statics for both Small Cell and Base Station.

[description]

# Zero Column holds total number of active calls
# First Column holds successful call attempts
# Second Column holds successful completed calls
# Third Column holds successful handoff count
# Fourth Column holds handoff failure count
# Fifth Column holds call drops
# Sixth Column holds blocked calls due to capacity
# Seventh Column holds blocked calls due to signal power
# Eighth Column holds Handoff Attempts
'''
n = int(input("Enter Total Simulation Time (in hours): "))
x = int(input("Enter the distance between Base Station and Small Cell (in meters): "))
RSL.create_shadowloss(x)
power_bs = int(input("Enter the Base Station EIRP (in dBm): "))
power_sc = int(input("Enter the Small Cell EIRP (in dBm): "))
height_bs = 50
height_sc = 10
height_user = 1.7
N_bs = int(input("Enter the Channels at Base Station: "))
N_sc = int(input("Enter the Channels at Small Cell: "))
RSL_threshold = -102
frequency = 1000


def user_location():
    '''
    [summary]

    The function generates user location, direction of movement and the initial serving cell

    Returns:
        [loc] -- [location of user (float)]
        [dir] -- [direction of user (int)] 
        [node] -- [serving node of user (int)] int for boolean manipulation (flipping bit) when handing off
    '''
    prob_loc = random.random(
    )  # random location generation to get either the road, mall or parking lot
    if prob_loc <= 0.2:
        # 1/(total distance - 300) to get at least 1 meter off the base station
        loc = float(random.uniform(1 / (x - 300), 1) * (x - 300))
    elif 0.2 < (prob_loc) <= 0.5:
        loc = float((random.uniform(0, 1) * 100) + (x - 300))
    else:
        loc = float((random.uniform(0, (1 - (1 / x))) * 200) + (x - 200))

    if loc < (x - 200):
        udir = 1
    else:
        udir = 0

    if loc <= (x - 200):
        node = 0
    else:
        node = 1
    return loc, udir, node


def reset_user_stats(user):
    user_stats[0][user] = 0
    user_stats[1][user] = 0
    user_stats[2][user] = 0
    user_stats[3][user] = 0
    user_stats[4][user] = 0
    user_stats[5][user] = 0
    user_stats[6][user] = 0


def init_user(user, node, udir, loc, RSL_bs, RSL_sc):
    '''[summary]

    [Function Updates the Active call list and call timer]

    Arguments:
            user {[Integer]} -- [User #]
            node {[String]} -- [0: Base Station, 1: Small Cell]
            udir {[Integer]} -- [0: East, 1: West]
            loc {[float]} -- [Current Location of USer]
            rsl {[float]} -- [RSL value at current location for bs/sc]
    '''
    user_stats[0][user] = 1
    user_stats[1][user] = udir
    user_stats[3][user] = loc
    user_stats[4][user] = node
    user_stats[5][user] = RSL_bs
    user_stats[6][user] = RSL_sc


def call_start(user, node):
    network_stats[node][0] += 1  # Connected calls on node
    network_stats[node][1] += 1  # Successful call attempts
    # initiliazes the call timer
    user_stats[2][user] = int(np.random.exponential(180))


def call_setup(user, node, RSL_bs, RSL_sc):
    if node == 0:  # Base Station
        if RSL_bs >= RSL_threshold:  # checks RSL
            if network_stats[node][0] < N_bs:  # Checks Channels
                call_start(user, node)
            else:
                # blocked call due too capacity increment
                network_stats[node][6] += 1
                reset_user_stats(user)
        elif RSL_sc >= RSL_threshold:
            if network_stats[1][0] < N_sc:
                node = 1  # re assignment of node
                user_stats[4][user] = node
                call_start(user, node)
            else:
                network_stats[node][7] += 1  # blocked call due to power
                reset_user_stats(user)
        else:
            # blocked call due to power on initial node
            network_stats[node][7] += 1
            reset_user_stats(user)

    else:  # Small Cell
        if RSL_sc >= RSL_threshold:
            if network_stats[node][0] < N_sc:
                call_start(user, node)
            else:
                network_stats[node][6] += 1
                reset_user_stats(user)
        elif RSL_bs >= RSL_threshold:
            if network_stats[0][0] < N_bs:
                node = 0
                user_stats[4][user] = node
                call_start(user, node)
            else:
                network_stats[node][7] += 1
                reset_user_stats(user)
        else:
            network_stats[node][7] += 1
            reset_user_stats(user)


def user_location_update(user, loc, udir):
    if 1 < loc <= (x - 300):
        if udir:
            loc += 15
        else:
            loc -= 15
    else:
        if udir:
            loc += 1
        else:
            loc -= 1
    user_stats[3][user] = loc  # updated location of user at next second
    return loc


def call_success_update(user, node):
    network_stats[node][2] += 1  # Increment Completed Calls
    network_stats[node][0] -= 1  # Active Calls on Node
    reset_user_stats(user)  # Set user to Idle


def handoff(user, node):
    node = 1 if node == 0 else 0  # node flipped
    N = N_sc if node == 1 else N_bs  # channel check
    if network_stats[node][0] < N:
        user_stats[4][user] = node
        network_stats[node][0] += 1  # Connected calls on node
        # Connected calls on prev node
        network_stats[1 if node == 0 else 0][0] -= 1
        # Successful call handoffs from prev node
        network_stats[1 if node == 0 else 0][3] += 1
    else:
        # Failed call handoffs from prev node
        network_stats[1 if node == 0 else 0][4] += 1
        network_stats[node][6] += 1  # Failed due to capacity


def drop_call_update(user, node):
    network_stats[node][0] -= 1  # Decrement connected calls
    network_stats[node][5] += 1  # Dropped call
    reset_user_stats(user)  # Set user to Idle


if __name__ == "__main__":
    start = time.time()
    file = open("Stats.txt", "w+")
    file1 = open("Drop Locations.txt", "w+")
    file1.write("Dropped Calls at: \n")
    file.write(
        '--------------------------------------------------------------------------------------\n')
    file.write(
        'Carrier Frequency                   : {} Mhz\n'.format(frequency))
    file.write(
        'Height of Base Station              : {} Meters\n'.format(height_bs))
    file.write(
        'Height of Small Cell                : {} Meters\n'.format(height_sc))
    file.write(
        'Height of User                      : {} Meters\n'.format(height_user))
    file.write(
        'Base Station Power                  : {} dBm\n'.format(power_bs))
    file.write(
        'Small Cell Power                    : {} dBm\n'.format(power_sc))
    file.write('Maximum Channels in Base Station    : {}\n'.format(N_bs))
    file.write('Maximum Channels in Small Cell      : {}\n'.format(N_sc))
    file.write(
        '--------------------------------------------------------------------------------------\n')
    for hours in range(0, n):
        for seconds in range(1, 3600):
            for user in range(1, 1000):
                if user_stats[0][user] == 0:  # checking if user is on active call or not
                    prob_Call = random.random()  # generating random flot for call probability
                    if prob_Call <= (1 / 3600):
                        loc, udir, node = user_location()
                        RSL_bs, RSL_sc = RSL.RSL(
                            frequency, x, loc, height_bs, height_sc, height_user, power_bs, power_sc)
                        init_user(user, node, udir, loc, RSL_bs, RSL_sc)
                        call_setup(user, node, RSL_bs, RSL_sc)
                else:  # if not on active call
                    loc, udir, node = user_stats[3][user], user_stats[1][user], user_stats[4][user]
                    loc = user_location_update(user, loc, udir)
                    user_stats[2][user] -= 1
                    if user_stats[2][user] == 0:
                        call_success_update(user, node)
                    else:
                        if loc <= 1:
                            call_success_update(user, node)
                        elif loc >= (x - 1):
                            call_success_update(user, node)
                        else:
                            RSL_bs, RSL_sc = RSL.RSL(
                                frequency, x, loc, height_bs, height_sc, height_user, power_bs, power_sc)
                            user_stats[5][user] = RSL_bs
                            user_stats[6][user] = RSL_sc
                            if node == 0:  # Base Station
                                if RSL_bs < RSL_threshold:
                                    file1.write("Location : {}, Node: {}, RSL of serving cell: {}\n".format(
                                        loc, node, RSL_bs))
                                    drop_call_update(user, node)
                                elif RSL_bs < RSL_sc:
                                    # handoff attemp increment
                                    network_stats[1][8] += 1
                                    handoff(user, node)
                                else:
                                    continue
                            else:  # Small Cell
                                if RSL_sc < RSL_threshold:
                                    file1.write("Location : {}, Node: {}, RSL of serving: {}\n".format(
                                        loc, node, RSL_sc))
                                    drop_call_update(user, node)
                                elif RSL_sc < RSL_bs:
                                    # handoff attempt increment
                                    network_stats[0][8] += 1
                                    handoff(user, node)
                                else:
                                    continue

        # file.write('Net Stats: {}\n\n'.format(network_stats))
        file.write('Statistics for hour {}.\n\n\n'.format(hours + 1))
        file.write(
            '--------------------------------------------------------------------------------------\n')
        file.write('                   BASESTATION                  \n')
        file.write('Active Calls                         : {}\n\n'.format(
            network_stats[0][0]))
        file.write(
            '--------------Accessibility Statistics------------------------------------------------\n')
        file.write('Total Call Attempts                  : {}\n'.format(
            network_stats[0][1]))
        file.write('Successful Call Connections          : {}\n'.format(
            network_stats[0][2]))
        file.write(
            '--------------Retainability Statistics------------------------------------------------\n')
        file.write('Dropped Calls                        : {}\n'.format(
            network_stats[0][5]))
        file.write('Blocked Calls due to Capacity        : {}\n'.format(
            network_stats[0][6]))
        file.write('Blocked Calls due to Power           : {}\n'.format(
            network_stats[0][7]))
        file.write(
            '-----------------Mobility Statistics--------------------------------------------------\n')
        file.write('Handoff Attempts to Small Cell       : {}\n'.format(
            network_stats[0][8]))
        file.write('Successful Handoffs from Small Cell  : {}\n'.format(
            network_stats[0][3]))
        file.write('Failed Handoffs from Small Cell      : {}\n'.format(
            network_stats[0][4]))
        file.write(
            '--------------------------------------------------------------------------------------\n')
        file.write('                   SMALL CELL                  \n')
        file.write('Active Calls                         : {}\n'.format(
            network_stats[1][0]))
        file.write(
            '--------------Accessibility Statistics------------------------------------------------\n')
        file.write('Total Call Attempts                  : {}\n'.format(
            network_stats[1][1]))
        file.write('Successful Call Connections          : {}\n'.format(
            network_stats[1][2]))
        file.write(
            '--------------Retainability Statistics------------------------------------------------\n')
        file.write('Dropped Calls                        : {}\n'.format(
            network_stats[1][5]))
        file.write('Blocked Calls due to Capacity        : {}\n'.format(
            network_stats[1][6]))
        file.write('Blocked Calls due to Power           : {}\n'.format(
            network_stats[1][7]))
        file.write(
            '-----------------Mobility Statistics--------------------------------------------------\n')
        file.write('Handoff Attempts to Base Station     : {}\n'.format(
            network_stats[1][8]))
        file.write('Successful Handoffs from Base Station: {}\n'.format(
            network_stats[1][3]))
        file.write('Failed Handoffs from Base Station    : {}\n'.format(
            network_stats[1][4]))
        file.write(
            '--------------------------------------------------------------------------------------\n')
        file.write('                NETWORK SUMMARY                \n')
        file.write('Total Call Attempts                  : {}\n'.format(
            network_stats[0][1] + network_stats[1][1]))
        file.write('Total Successful Call Connections    : {}\n'.format(
            network_stats[0][2] + network_stats[1][2]))
        file.write('Total Dropped Calls                  : {}\n'.format(
            network_stats[0][5] + network_stats[1][5]))
        file.write('Total Blocks due to Capacity         : {}\n'.format(
            network_stats[0][6] + network_stats[1][6]))
        file.write('Total Blocks due to Power            : {}\n'.format(
            network_stats[0][7] + network_stats[1][7]))
        file.write('Total Handoff Attempts               : {}\n'.format(
            network_stats[0][8] + network_stats[1][8]))
        file.write('Total Handoff Successful             : {}\n'.format(
            network_stats[0][3] + network_stats[1][3]))
        file.write('Total Handoff Failed                 : {}\n'.format(
            network_stats[0][4] + network_stats[1][4]))
        file.write('Call Connection Success Rate         : {:0.2f}%\n'.format(
            ((network_stats[0][2] + network_stats[1][2]) / (network_stats[0][1] + network_stats[1][1]) * 100)))
        file.write('Drop Call Rate                       : {:0.2f}%\n'.format(
            ((network_stats[0][5] + network_stats[1][5]) / (network_stats[0][1] + network_stats[1][1]) * 100)))
        file.write('Handoff Success Rate                 : {:0.2f}%\n'.format(((network_stats[0][3] + network_stats[1][3]) / (
            network_stats[0][8] + network_stats[1][8]) * 100)))
        file.write('GOS for the System                   : {:0.3f}\n'.format(
            (network_stats[1][6] + network_stats[1][7] + network_stats[0][6] + network_stats[0][7]) / (network_stats[0][1] + network_stats[1][1])))
        file.write('\n\n')
    print('Simulation Runtime: {}'.format(time.time() - start))
    file.close()