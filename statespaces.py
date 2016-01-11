def discrete_bin(value, minimum, maximum, nbins):
    """
    Given a range from minimum to maximum (inclusive) divided into nbins bins, returns
    the bin that "value" belongs in.
    """
    # Make the maximum "exclusive".
    maximum += 0.001
    binsz = (maximum - minimum)*1.0/nbins
    # Bins are 0 to (nbins - 1). If values lie outside of min/max range, they just go in the first/last bin.
    return max(0,min(int((value - minimum)/binsz), nbins-1))

class RawDataStateSpace():
    def __init__(self):
        pass

    def transform(self, state):
        monkey_top = discrete_bin(state["monkey"]["top"], -200,200,20)
        monkey_bot = discrete_bin(state["monkey"]["bot"], -200, 200, 20)
        tree_top = discrete_bin(state["tree"]["top"], -200, 200, 20)
        tree_bot = discrete_bin(state["tree"]["bot"], -200, 200, 20)
        return (monkey_top, monkey_bot, tree_top, tree_bot)

class YDistFromGapStateSpace():
    def __init__(self):
        pass

    def transform(self, state):
        """
        Transforms the state from a dictionary to a tuple contianing some information.
        {
        'score': <current score>,
        'tree': { 'dist': <pixels to next tree trunk>,
            'top': <height of top of tree trunk gap>,
            'bot': <height of bottom of tree trunk gap> },
        'monkey': { 'vel': <current monkey y-axis speed>,
            'top': <height of top of monkey>,
            'bot': <height of bottom of monkey> }
        }
        """
        monkey_pos = state['monkey']['bot'] + (state['monkey']['top'] - state['monkey']['bot']) / 2.0
        gap_center = state['tree']['bot'] + (state['tree']['top'] - state['tree']['bot']) / 2.0

        diff = (monkey_pos - gap_center)
        discrete_diff = discrete_bin(diff, -250,250,20)
        state = (discrete_diff,)
        return state

class YDistFromGapAndVelStateSpace():

    def __init__(self):
        pass

    def transform(self, state):
        """
        Transforms the state from a dictionary to a tuple contianing some information.
        {
        'score': <current score>,
        'tree': { 'dist': <pixels to next tree trunk>,
            'top': <height of top of tree trunk gap>,
            'bot': <height of bottom of tree trunk gap> },
        'monkey': { 'vel': <current monkey y-axis speed>,
            'top': <height of top of monkey>,
            'bot': <height of bottom of monkey> }
        }
        """
        monkey_pos = state['monkey']['bot'] + (state['monkey']['top'] - state['monkey']['bot']) / 2.0
        gap_center = state['tree']['bot'] + (state['tree']['top'] - state['tree']['bot']) / 2.0
        vel = state['monkey']['vel']

        diff = (monkey_pos - gap_center)
        discrete_diff = discrete_bin(diff, -200,200,20)
        discrete_vel = discrete_bin(vel, -20, 20, 10)
        print vel, discrete_vel
        #print vel
        state = (discrete_diff,discrete_vel)
        return state

class XYDistFromGapStateSpace():

    def __init__(self):
        pass

    def transform(self, state):
        """
        Transforms the state from a dictionary to a tuple contianing some information.
        {
        'score': <current score>,
        'tree': { 'dist': <pixels to next tree trunk>,
            'top': <height of top of tree trunk gap>,
            'bot': <height of bottom of tree trunk gap> },
        'monkey': { 'vel': <current monkey y-axis speed>,
            'top': <height of top of monkey>,
            'bot': <height of bottom of monkey> }
        }
        """
        monkey_pos = state['monkey']['bot'] + (state['monkey']['top'] - state['monkey']['bot']) / 2.0
        gap_center = state['tree']['bot'] + (state['tree']['top'] - state['tree']['bot']) / 2.0
        vel = state['monkey']['vel']
        dist = state['tree']['dist']

        diff = (monkey_pos - gap_center)
        discrete_diff = discrete_bin(diff, -200,200,20)
        discrete_vel = int( (vel < 0) )
        discrete_dist = discrete_bin(dist, 0, 50, 5)
        #print vel
        state = (discrete_diff,discrete_vel,discrete_dist)
        return state

class CanClearGapStateSpace():
    def __init__(self):
        pass

    def transform(self, state):
        # Want a 20 pixel cushion from bottom and top of gap
        cushion = 20
        # Negative if monkey below
        distfrombot = state["monkey"]["bot"] - (state["tree"]["bot"] + cushion)
        # Positive if monkey above
        distfromtop = state["monkey"]["top"] - (state["tree"]["top"] - cushion)
        distfrombot = min(0, distfrombot)
        distfromtop = max(0, distfromtop)

        # Special case if can go into gap
        if distfrombot == 0 and distfromtop == 0:
            state = "SPECIAL!"
        elif distfrombot == 0:
            state = discrete_bin(distfromtop, 0, 200,10)
        elif distfromtop == 0:
            state = -discrete_bin(distfrombot, -200, 0, 10)

        return state