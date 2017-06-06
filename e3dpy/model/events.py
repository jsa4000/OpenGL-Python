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

    def print_events(events):
        """
        """
        result = [str(event) for event in events]
        print("\n".join(result))

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

    SCRIPT_LABEL = "script"
    CONDITION_LABEL = "condition"
    TYPE_LABEL = "type"

    @property
    def condition(self):
        """ Check if the current Action has a condition to evaluate
        """
        if Action.CONDITION_LABEL in self:
            return True
        return False

    def __init__(self, action):
        """ Constructor for Action Class

        This will parse the actions in parameters in it will create
        the class Action to manage the actions, check of events that
        satisfy the action and it will launch the scripts.

         [actions: action1 {  [ event ]     [ event ]  [ script ] }
                   action2 {  [ event ]                [ script ] }
                   action3 {  [ condition ]            [ script ] } ]
                   action4 {  [ condition ] [ event ]  [ script ] } ]

        """
        # Parse the current action
        self.update(self._parse_action(action))   

    def _eval(self, value):
        """ Evaluate the current value
        """
        try:
            value = eval(value)    
        except:
            pass
        return value

    def _get_attr(self, object, attrib):
        """
        """
        value = getattr(object,attrib)
        if isinstance(value,(list)):
            if len(value) == 1:
                return value[0]
            else:
                return sorted(value)
        else:
            return value

    def _parse_event(self, event):
        """ Parse the event passed by parameters

        Each event will be composed on a type and different
        parameters depending on the event type

            type            parameters
            ---------------------------------
            QUIT	        None
            ACTIVEEVENT	    gain, state
            KEYDOWN	        key, mod
            KEYUP	        key, mod
            MOUSEMOTION	    pos, rel, buttons
            MOUSEBUTTONUP	pos, button
            MOUSEBUTTONDOWN	pos, button
            JOYAXISMOTION	joy, axis, value
            JOYBALLMOTION	joy, ball, rel

        """
        result = dict()
        for parameter in event:
            if parameter == Action.TYPE_LABEL:
                # Extract the type
                result[parameter] = self._eval(event[parameter])
            else:
                # Check whther the parameters is a list, scalar, etc,,
                if not isinstance(event[parameter], (list)):
                    # Parameters it's a scalar value, not a list
                    result[parameter] = self._eval(event[parameter])
                elif len(event[parameter]) == 1:
                    # Parameter is a list, but only one value in it
                    result[parameter] = self._eval(event[parameter][0])
                else:
                    #Parameter is a list, consider the value as a list
                    result[parameter] = list()
                    for value in event[parameter]:
                        result[parameter].append(self._eval(value))
                    # Sort current values
                    result[parameter] = sorted(result[parameter])
        return result

    def _parse_action(self, action):
        """ Parse the action passed by parameters
  
        Following are some possible cases of actions. Each action could
        be composed of events, condition and finally the script that
        will be executed.

        [actions: action1 {  [ event ]     [ event ]  [ script ] }
                  action2 {  [ event ]                [ script ] }
                  action3 {  [ condition ]            [ script ] } ]
                  action4 {  [ condition ] [ event ]  [ script ] } ]
        """
        result = dict()
        for element in action:
            # Search for events, conditions and script
            if element in [Action.SCRIPT_LABEL, Action.CONDITION_LABEL]:
                result[element] = action[element]
            else:
                # Create current element
                event = action[element]
                if not isinstance(event, (list)):
                    # Create a soingle event
                    result[element] = self._parse_event(action[element])
                else:
                    # Crete a list of events and
                    result[element]=list()
                    for subevent in event:
                        # Check whether it's a multiple condition or not
                        result[element].append(self._parse_event(subevent))
        return result

    @property
    def events(self):
        """ Return the current events for the action
        """
        return [element for element in self if element not in [Action.CONDITION_LABEL, Action.SCRIPT_LABEL]]

    def isin(self, events):
        """ Check if the action is present in the events

        An action could be represented as a sequence of action. However
        we will only consider the events that belong to the same frame.
        """
        # Get the current events from the action to check
        action_events = self.events
        if empty(action_events): return False
        # Look through all the events-action and current events.
        for action_event in action_events:
            #Check if the condition is aggrefation
            if isinstance(self[action_event],(list)):
                series_event = self[action_event]
                # Initialize the coincidences between action-events and events
                coincidences = [0] * len(series_event)
                # Loop through all the series events
                for index, serie in enumerate(series_event):
                    # Check if the action-events are currently in the events
                    for event in events:
                        # Check the current event
                        for parameter in serie:
                            try:
                               # For the comparation the list are sortened previously
                                if serie[parameter] != self._get_attr(event,parameter):
                                    break
                            except:
                                pass
                        else:
                            # If elements are not different the continue
                            coincidences[index] = 1
                # Return the number of coincidences.
                if all(coincidences):
                    return True
            else:
                #Single events that must be satisfied
                coincidences = False
                # Check if the action-events are currently in the events
                for event in events:
                    # Check the current event
                    for parameter in self[action_event]:
                        try:
                            # For the comparation the list are sortened previously
                            if self[action_event][parameter] != self._get_attr(event,parameter):
                                break
                        except:
                            pass
                    else:
                        # If elements are not different the continue
                        coincidences = True
                # Return the number of coincidences.
                if coincidences:
                    return True
        # By default return false
        return False
      
    def print_resume(action, events):
        """
        """
        # Return all actions have been found
        print("************************************")
        if action:
            print("Current Action:")
            print(action)
        print("------------------------------------")
        if events:
            print("Current Events:")
            Event.print_events(events)

    def __str__(self):
        """
        """
        # <Event: {}>".format(self.__dict__
        result = ["<{}: {}>".format(element, self[element]) for element in self]
        return "\n".join(result)

    def evaluate(self, event):
        """ Check if condition in action to evaulate it
        """
        if not self.condition: return False

        try:
            exec(self[Action.CONDITION_LABEL])
        except:
            return False
        return True

    def execute(self, **kwargs):
        """ Execute the current script associated with the current action.
        """
        for key in kwargs:
            exec("{} = kwargs['{}']".format(key, key))
        try:
            exec(self[Action.SCRIPT_LABEL])
        except:
            print("Error: {}".format(self[Action.SCRIPT_LABEL]))
            return False
        return True

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

    