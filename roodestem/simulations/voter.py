'''
Created on Jul 25, 2016

@author: Thomas Adriaan Hellinger
'''
from abc import ABCMeta, abstractmethod
from math import sqrt, pow


class Voter(object):
    """Basic entity in simulation, represents an individual.
    
    Args:
        metric (:obj:`VotingMetric`): Determines the voter's relative opinion
            of a  candidate proposal or individual, based on a distance 
            measurement between the voter position on the 
            :obj:`VotingMetric`'s spectrum, measured against the candidate on
            the same spectrum.
        name (:obj:`str`): The name of the candidate proposal or individual.
     
     Raises:
         :py:exec:`AttributeError`: If metric is deleted.
    """
    def __init__(self, voting_metric, name=None):
        self._metric = voting_metric
        self._name = name

    def determine_opinion_on(self, vm, rng=(0,10)):
        """Indicates the strength of the voters opinion on a candidate.
        
        Args:
            vm (:obj:`VotingMetric` or :obj:`Voter`): The metric (or the voter
                in which the metric resides) which measures where the candidate
                proposal or individual resides on an ideological scale. MUST BE 
                the same metric this voter uses.
            rng (:obj:`2-tuple` of :obj:`int`): The lowest and highest scores,
                respectively, that the user can assign to the candidate
                proposal.
        
        Raises:
            :py:exec:`TypeError`: If rng[0], the lower bound is greater than,
                or equal to, rng[1], the higher bound.
        """
        err_msg = 'Candidate "{0}" uses "{1}" metric, '
        err_msg += 'but "{2}" uses "{3}" metric.'
        if type(vm is Voter):
            if type(vm.metric) != type(self.metric):
                raise TypeError(err_msg.format(vm.name,
                                               str(type(vm.metric)),
                                               self.name,
                                               str(type(self.metric))))
            return self.metric.determine_distance_from(vm.metric, rng)
        else:
            if type(vm) != type(self.metric):
                raise TypeError(err_msg.format(str(type(vm)), 
                                               str(type(vm)),
                                               self.name,
                                               str(type(self.metric))))
            return self.metric.determine_distance_from(vm, rng)
    
    @property
    def name(self):
        return self._name
    
    @property
    def metric(self):
        return self._metric
    
    @metric.setter
    def metric(self, val):
        self._metric = val
    
    @metric.deleter
    def metric(self):
        raise AttributeError("Cannot delete a Voter's VotingMetric.")
    
    def __repr__(self):
        return "<Voter: {0}>".format(self.name)

class VotingMetric(object, metaclass=ABCMeta):
    """System for determining position on an n-dimensional ideological space
    
    Args:
        dimensions (:obj:`dict` of :obj:`str` to :obj:`float`): Each dimension
            is labeled by the name of the dimension with the value being the
            ideological position. The position is -1 on one end of the spectrum 
            to 1 on the other, with 0 representing a perfect balance between
            both poles.
        cardinality (:obj:`const int`): A constant indicating the number of
            ideological dimensions on the specrtum.  
    """
    @abstractmethod
    def __init__(self, **kwargs):
        pass
    
    @property
    def dimensions(self):
        return self._dimensions
    
    def get_axis_labels(self):
        return self._dimensions.keys()
    
    @property
    def cardinality(self):
        return self._cardinality
    
    @cardinality.setter
    def cardinality(self, _):
        raise AttributeError("Cannot set or delete VotingMetric cardinality.")
    
    @cardinality.deleter
    def cardinality(self):
        raise AttributeError("Cannot set or delete VotingMetric cardinality.")
    
    @abstractmethod
    def determine_distance_from(self, dim):
        pass


class NolanChart(VotingMetric):
    """An ideological map based on 2-dimensions
    
    The Nolan chart is an expanded version of the classic left-right political
    spectrum. The traditional left-right spectrum is represented as the
    'PRIVATE PROPERTY' spectrum, here represented as -1 for leftmost, and 1 for
    rightmost. Left represents a higher respect for communal property over
    private, with right representing the opposite.
    
    The additional axis represents the 'PUBLIC AUTHORITY' spectrum, represented
    here by 1 for the most authoritarian views, and -1 for the most libertarian
    views. This represents an individuals preference for government 
    intervention with authoritarian views leaning towards more government 
    intervention, in more arenas, and libertarian views leaning towards less
    government intervention and in less arenas.
    
    The nolan chart has five labels, with a diamond shaped region in the center
    which represents 'centrist'. All five regions are equal in area.
    
    Args:
        cardinality (:obj:`const int`): 2. Nolan chart is a two-dimensional
            political spectrum.
        position (:obj:`str`): On instantiation position is set to one of 5
            values, depending on where the coordinate falls on the ideological
            spectrum. These values are either centrist, or a combination of 
            "leftist" <=> "rightist" and "libertarian" <=> "authoritartian". In
            some cases 1 (but not both) label might be blank (eg. just 
            'leftist' or just "libertarian").
    
    Raises:
        :py:exc:`AttributeError`: If dimensions outside of [-1, 1] are passed
            to either axis. Also raised if cardinality is altered or deleted.
    """
    _MAX_DISTANCE = sqrt(8)
    def __init__(self, public_auth, pri_prop):
        self._dimensions = {"public_authority": public_auth, 
                            "private_property": pri_prop}
        for score, pos in self._dimensions.items(): 
            if pos < -1 or pos > 1:
                msg = "Voter position must be within [-1, 1]."
                msg += " Score for {0} is {1}."
                raise AttributeError(msg.format(score, pos))
        self._cardinality = 2
        self.position = self._determine_political_label()  


    def determine_distance_from(self, vm, rng=(0,10)):
        """Determines ideological distance between two points.
        
        Uses a Euclidean distance algorithm to measure the distance between
        two points on the 2d ideological spectrum. The distance is then 
        normalized from the [-1,1] range to the range specified.
        
        Args:
            vm (:obj:`NolanChart`): The other NolanChart containing the positon
              of the candidtate proposal or individual.
            rng (:obj:`2-tuple` of :obj:`int`): The lowest and highest scores,
                respectively, that range will be normalized to.
        
        Returns:
            :obj:`float`: The euclidean distance from the position in this 
                :obj:`NolanChart` to the position in the other 
                :obj:`NolanChart`.
        """
        if rng[1] <= rng[0]:
            msg = "Max rng: {0} must be GREATER THAN min rng: {1}"
            raise TypeError(msg.format(rng[1], rng[0]))
        
        sm = 0
        for k in self.get_axis_labels():
            sm += pow(self._dimensions[k] - vm.dimensions[k], 2)
        sm = sqrt(sm / pow(NolanChart._MAX_DISTANCE, 2))
        return rng[1] - rng[1]*sm 
    
    def _determine_political_label(self):
        def determine_label_onaxis(axis_name, score):
            """Assigns a label on for a point depending on where it falls on 
            it's axis. Either 'rightist', 'leftist', or '' (for 0) for the
            "private property" axis.  
            """
            if axis_name == 'private_property':
                if score > 0:
                    return 'rightist'
                elif score < 0:
                    return 'leftist'
                else:
                    return ''
            elif axis_name == 'public_authority':
                if score > 0:
                    return 'authoritarian'
                elif score < 0:
                    return 'libertarian'
                else:
                    return ''
            else:
                raise TypeError("Unknown axis")
        
                
        def determine_if_centrist(x,y,triangle_coords):
            """Uses a barycentric coordinate system to determine if the
            position falls within a centrist triangle in a particular quadrant
            of the 2d ideological spectrum.  
            """
            x1,x2,x3 = [coord[0] for coord in triangle_coords]
            y1,y2,y3 = [coord[1] for coord in triangle_coords]
            a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3))
            a /= ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
            b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) 
            b /= ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
            c = 1 - a - b
            return (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)
        
        if 0 in self._dimensions.values():
            if sum(self._dimensions.values()) < sqrt(.8) and\
            sum(self._dimensions.values()) > -1*sqrt(.8):
                return 'centrist'
            else:
                axname, score = [(x,y) for x,y in self._dimensions.items() if y != 0][0]
                return determine_label_onaxis(axname, score)
        else:
            triangle_coords = None
            lbl = None
            if self._dimensions['private_property'] > 0 and\
            self._dimensions['public_authority'] > 0:
                # Dimension I
                triangle_coords = [(0,0),(0,sqrt(.8)),(sqrt(.8), 0)]
                lbl = "authoritarian rightist"
            elif self._dimensions['private_property'] > 0 and\
            self._dimensions['public_authority'] < 0:
                # Dimension II
                triangle_coords = [(0,0),(sqrt(.8), 0),(0, -1*sqrt(.8))]
                lbl = "libertarian rightist"
            elif self._dimensions['private_property'] < 0 and\
            self._dimensions['public_authority'] < 0:
                # Dimension III
                triangle_coords = [(0,0),(-sqrt(.8), 0),(0, -1*sqrt(.8))]
                lbl = "libertarian leftist"
            else:
                # Dimension IV
                triangle_coords = [(0,0),(-sqrt(.8), 0),(0, sqrt(.8))]
                lbl = 'authoritarian leftist'
        
            if determine_if_centrist(self._dimensions['private_property'],
                                     self._dimensions['public_authority'],
                                     triangle_coords):
                return "centrist"
            else:
                return lbl
    
    def __repr__(self):
        lbl = "<Nolan Chart: {0}"
        lbl += " (private_property: {1}, public_authority: {2})>"
        return lbl.format(self.position, 
                          self._dimensions['private_property'],
                          self._dimensions['public_authority'])


# Example entities...
Thomas_Adriaan_Hellinger = Voter(NolanChart(-0.75, -0.95), 
                                 "Thomas Adriaan Hellinger")
Jill_Stein = Voter(NolanChart(-0.25, -0.25), "Jill Stein")
Gary_Johnson = Voter(NolanChart(-.15,.95),"Gary Johnson")
Hillary_Clinton = Voter(NolanChart(.5, .75), "Hillary Clinton")
Donald_Trump = Voter(NolanChart(.9,.65), "Donald Trump")
Bernie_Sanders = Voter(NolanChart(0,-.2), "Bernie Sanders")
us_presidential_candidates_2016 = [ 
    Jill_Stein,
    Hillary_Clinton,
    Gary_Johnson,
    Donald_Trump,
    Bernie_Sanders
]
