from ..core.utils import *
from ..core.constants import DeviceEvent, MouseButton, Key, KeyModifier

class Event(object):
    """ Generic Event class definition. 
    """
    def __init__(self, *args, **kwargs):
        """Constructor
        """
        try:
            for key in args:
                setattr(self, key, args[key])
        except:
            # None of not a dictionary
            pass
        for key in kwargs:
            setattr(self, key, kwargs[key])
    def __repr__(self):
        """"""
        return "<Event: {}>".format(self.__dict__)

class Action(dict):
    """ Action Class

    Following are the possible scenarios in order to create Action:

        "orbit" :
            { "event": [ 
                  {"type" : "DeviceEvent.MOUSEMOTION", 
                   "buttons": ["MouseButton.MIDDLE","MouseButton.LEFT"]},
                  {"type" : "DeviceEvent.KEYSPRESSED","keys": "Key.K_SPACE" }],
              "script": "print('Acabas de pulsar la combinación')"
            },
        "pan" :  
            { "event": { "type":"DeviceEvent.KEYUP","key":["Key.K_a"]},
              "script": "print('Acabas de pulsar la A')"
            },
        "write" :  
            { "condition": "event.type==DeviceEvent.KEYUP and  \
                            event.key==Key.K_a",
              "script": "print('Acabas de pulsar la A')"
            },
        "quit" :  
            { "event_1": { "type":"DeviceEvent.QUIT"},
              "event_2": { "type":"DeviceEvent.KEYUP","key":"Key.K_ESCAPE"},
              "script": "self._engine.stop()"
            }

    """

    def _eval(self, value):
        """
        """
        try:
            value = eval(value)    
        except:
            pass
        return value

    def _get_event(self, event):
        """ Parse the event passed by parameters
        """
        result = dict()
        for parameter in event:
            if parameter == "type":
                # Extract the type
                result[parameter] = self._eval(event[parameter])
            else:
                if not isinstance(event[parameter], (list)):
                    result[parameter] = self._eval(event[parameter])
                elif len(event[parameter]) == 1:
                    result[parameter] = self._eval(event[parameter][0])
                else:
                    result[parameter] = list()
                    for value in event[parameter]:
                        result[parameter].append(self._eval(value))
        return result

    def __init__(self, action):
        """ Constructor for Action Class

        [actions: action1 {  [ event ]     [ event ]  [ script ] }
                  action2 {  [ event ]                [ script ] }
                  action3 {  [ condition ]            [ script ] } ]
                  action4 {  [ condition ] [ event ]  [ script ] } ]

        """
        for element in action:
            # Search for events, conditions and script
            if element == "script" or element == "condition":
                self[element] = action[element]
            else:
                # Create current element
                event = action[element]
                if not isinstance(event, (list)):
                    # Current element it's a collection     
                    self[element] = self._get_event(action[element])
                else:
                    self[element]=list()
                    for subevent in event:
                        # Check whether it's a multiple condition or not
                        self[element].append(self._get_event(subevent))
                   

    def isin(self, events):
        """ Check if the action is present in the events

        An action could be represented as a sequence of action. However
        we will only consider the events that belong to the same frame.
        """
        action_events = self[action]["events"]
        coincidences = [0] * len(action_events)
        for index, action_event in enumerate(action_events):
            # Check if the action-events are currently in the events
            for event in events:
                # Check the current event
                for item in action_event:
                    try:
                        if action_event[item] != getattr(event,item):
                            break
                    except:
                        pass
                else:
                    # If elements are not different the continue
                    coincidences[index] = 1
        # Returnall actions have been found
        return all(coincidences)


class Actions(dict):
    """ Actions Class Definition

    This class will map the inputs from devices such as
    key board, clicks, etc.. to apply a certaion action.

    The idea is to have mapped all the possible inputs from
    the keyboard into actions. Actions could be from simple
    actions like invoking simple functions to be able to
    write some scripts to specify more advanced and complex actions.abs

    This input will model this configuration for files or any key, value
    structutre like dictionary

    Following are the most typical events using keyboard, mouse, etc

     Event Type	    Parameters
        -------------------------------------
        QUIT	        None
        ACTIVEEVENT	    gain, state
        KEYDOWN	        key, mod
        KEYUP	        key, mod
        MOUSEMOTION	    pos, rel, buttons
        MOUSEBUTTONUP	pos, button
        MOUSEBUTTONDOWN	pos, button
        JOYAXISMOTION	joy, axis, value
        JOYBALLMOTION	joy, ball, rel
        JOYHATMOTION	joy, hat, value
        JOYBUTTONUP	    joy, button
        JOYBUTTONDOWN	joy, button
        VIDEORESIZE	    size, w, h
        VIDEOEXPOSE	    None
        USEREVENT	    Code
        -----------------------------------
        KEYSPRESSED     Keys

    """

    def __init__(self, actions):
        """ Initialize the class

        This functiona will parse the actions.
        As comented in previouse examples the action could be composed on:

        [actions: action1 {  [ event ]     [ event ]  [ script ] }
                  action2 {  [ event ]                [ script ] }
                  action3 {  [ condition ]            [ script ] } ]

        """
        # List that will store all the input-action for this instance
        for action in actions:
            # Create the key, value for the current action to Parse
            self[action] = Action(actions[action])
            print(self[action])
             
        print(self)

    