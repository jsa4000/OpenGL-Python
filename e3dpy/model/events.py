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

    Example: 

        actions = { 
            "orbit" : { "events": [ 
                                { "type" : "DeviceEvent.MOUSEMOTION", 
                                    "parameters": [ "MouseButton.LEFT", 
                                                    "MouseButton.LEFT" ]},
                                { "type" : "DeviceEvent.MOUSEMOTION", 
                                    "parameters": [ "MouseButton.RIGHT" ] }
                                ],
                        "script": "entity.camera.orbit(event.rel[0],event.rel[1])"
                    },
            "pan" :   { "events": { "type":"DeviceEvent.KEYUP", 
                                    "buttons": ["Key.K_a"]},
                        "script": "entity.camera.pan(event.rel[0],event.rel[1])"}}

    """

    def __init__(self, actions):
        """ Initialize the class

        This functiona will parse the actions

        """
        # List that will store all the input-action for this instance
        for action in actions:
            # Create the key, value for the current action
            self[action] = dict()
            # Loop over the elements events
            events = actions[action]["events"] 
            if not is_collection(events):
                events = [actions[action]["events"]]
            self[action]["events"] = list()
            for event in events:
                # Eval the event paramters if possible
                event_eval = dict()
                for parameter in event:
                    if parameter == "type":
                        # Extract the type
                        event_eval["type"] = eval(event["type"])
                    else:
                        #Extract the parameters
                        if not is_collection(event[parameter]):
                            #event[parameter] = [event[parameter]]
                            try:
                                event[parameter] = eval(event[parameter])
                            except:
                                event[parameter] = event[parameter]
                        elif len(event[parameter]) == 1:
                            event[parameter] = eval(event[parameter][0])
                        else:
                            event_eval[parameter] = list()
                            for value in event[parameter]:
                                event_eval[parameter].append(eval(value))
                #Finally attach current evaluated item to the list
                self[action]["events"].append(event_eval)
            # Store the script
            self[action]["script"] = actions[action]["script"] 

    def check(self, action, events):
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
        # Return if all actions have been found
        return all(coincidences)