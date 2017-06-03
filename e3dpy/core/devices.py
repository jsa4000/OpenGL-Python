from ..core.utils import *

__all__ = ['KeyboardDevice',
           'MouseDevice',
           'UIDevice',
           'EventType',
           'MouseButton',
           'KeyModifier',
           'Key']]

class KeyboardDevice(object):
    
    def init(self):
        """ Initialize the device
        """
        return self

    def get_keys_pressed(self):
        """ Return the keys pressed with the key-code 
        The returned array for this function will be:
        [8, 13]

        # In pygame we do the following, because the position will
        give us if that key has been pressed or not
        keys = get_keyboard_input()
        if keys[pygame.K_LEFT] and keys[pygame.K_LSHIFT]:
            pass

        NOTE: To check the specific event that has been triggered
        (KEYUP, KEYDOWN ), use isntead get_events()
        When you keep pressed a button there is no event assigned,
        so we need to check it after.
        """  
        raise NotImplementedError

class MouseDevice(object):
    
    def init(self):
        """ Initialize the device
        """
        return self

    def get_events(self):
        """ This function will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == EvenType.QUIT:
            display.close()
        if event.type == EvenType.KEYUP and event.key == EvenType.K_ESCAPE:
            display.close()

        Event Type	    Parameters
        -------------------------------------
        MOUSEMOTION	    pos, rel, buttons
        MOUSEBUTTONUP	pos, button
        MOUSEBUTTONDOWN	pos, button
        """
        raise NotImplementedError

    def set_mouse_visible(self, visible):
        """ Set visible the cursor
        """
        raise NotImplementedError

    def set_mouse_position(self, x, y):
        """ Set current position
        """
        raise NotImplementedError

    def get_mouse_offset(self):
        """
        """
       raise NotImplementedError

    def get_mouse_position(self):
        """ This will return the current mouse position
        The output must be a Vector2 with x,y coordinates
        
        Example: [234,234]
        """
        raise NotImplementedError

     def get_buttons_pressed(self):
        """ Function to get the buttons currently pressed
        The function will return an array with the mouse 
        buttons pressed. 
        
        For example if the original array is [0,1,0],
        This will return [1] wher the pressed button is the
        index = 1

        Example:
            if mouse[LEFTBUTTON]:
                pass
        """
        raise NotImplementedError

class UIDevice(object):
    
    def init(self):
        """ Initialize the device
        """
        return self

    def get_events(self):
        """ This function will return an array of (type, key)
        elements with the inpus received.

        To take into consideration if a key is currently being pressed
        the you have to call get_key_pressed(). Since this events
        wont recognize the pressed action until it will be released again.

        if event.type == EvenType.QUIT:
            display.close()
        if event.type == EvenType.KEYUP and event.key == EvenType.K_ESCAPE:
            display.close()

        Event Type	    Parameters
        -------------------------------------
        QUIT	        None
        ACTIVEEVENT	    gain, state
        VIDEORESIZE	    size, w, h
        VIDEOEXPOSE	    None
        USEREVENT	    Code
        """
        #Returne the capture events
        raise NotImplementedError

   class EventType(EnumBase):
        """ Enumeration with all events types supported 

    In this Events enumeration will be defined all the events supported
    by the engine that will be received as an input
    """
    QUIT = 12
    ACTIVEEVENT = 1
    KEYDOWN = 2
    KEYUP = 3
    MOUSEMOTION = 4
    MOUSEBUTTONUP = 6
    MOUSEBUTTONDOWN = 5
    JOYAXISMOTION = 7
    JOYBALLMOTION = 8
    JOYHATMOTION = 9
    JOYBUTTONUP = 11
    JOYBUTTONDOWN = 10
    VIDEORESIZE = 16
    VIDEOEXPOSE = 17
    USEREVENT = 24
    # New event added with the keys pressed
    KEYSPRESSED = 20

class MouseButton(EnumBase):
    """ Mouse button types
    """
    LEFT = 0
    MIDDLE =1
    RIGHT = 2

class KeyModifier(EnumBase):
    KMOD_NONE	=	0
    KMOD_LSHIFT	=	1
    KMOD_RSHIFT	=	2
    KMOD_SHIFT	=	3
    KMOD_LCTRL	=	64
    KMOD_RCTRL	=	128
    KMOD_CTRL	=	192
    KMOD_LALT	=	256
    KMOD_RALT	=	512
    KMOD_ALT	=	768
    KMOD_LMETA	=	1024
    KMOD_RMETA	=	2048
    KMOD_META	=	3072
    KMOD_NUM	=	4096
    KMOD_CAPS	=	8192
    KMOD_MODE	=	16384

class Key(EnumBase):
    """ Enumerataion with all the keys
    """
    K_FIRST	=	0
    K_UNKNOWN	=	0
    KEYDOWN	=	2
    KEYUP	=	3
    K_BACKSPACE	=	8
    K_TAB	=	9
    K_CLEAR	=	12
    K_RETURN	=	13
    K_PAUSE	=	19
    K_ESCAPE	=	27
    K_SPACE	=	32
    K_EXCLAIM	=	33
    K_QUOTEDBL	=	34
    K_HASH	=	35
    K_DOLLAR	=	36
    K_AMPERSAND	=	38
    K_QUOTE	=	39
    K_LEFTPAREN	=	40
    K_RIGHTPAREN	=	41
    K_ASTERISK	=	42
    K_PLUS	=	43
    K_COMMA	=	44
    K_MINUS	=	45
    K_PERIOD	=	46
    K_SLASH	=	47
    K_0	=	48
    K_1	=	49
    K_2	=	50
    K_3	=	51
    K_4	=	52
    K_5	=	53
    K_6	=	54
    K_7	=	55
    K_8	=	56
    K_9	=	57
    K_COLON	=	58
    K_SEMICOLON	=	59
    K_LESS	=	60
    K_EQUALS	=	61
    K_GREATER	=	62
    K_QUESTION	=	63
    K_AT	=	64
    K_LEFTBRACKET	=	91
    K_BACKSLASH	=	92
    K_RIGHTBRACKET	=	93
    K_CARET	=	94
    K_UNDERSCORE	=	95
    K_BACKQUOTE	=	96
    K_a	=	97
    K_b	=	98
    K_c	=	99
    K_d	=	100
    K_e	=	101
    K_f	=	102
    K_g	=	103
    K_h	=	104
    K_i	=	105
    K_j	=	106
    K_k	=	107
    K_l	=	108
    K_m	=	109
    K_n	=	110
    K_o	=	111
    K_p	=	112
    K_q	=	113
    K_r	=	114
    K_s	=	115
    K_t	=	116
    K_u	=	117
    K_v	=	118
    K_w	=	119
    K_x	=	120
    K_y	=	121
    K_z	=	122
    K_DELETE	=	127
    K_KP0	=	256
    K_KP1	=	257
    K_KP2	=	258
    K_KP3	=	259
    K_KP4	=	260
    K_KP5	=	261
    K_KP6	=	262
    K_KP7	=	263
    K_KP8	=	264
    K_KP9	=	265
    K_KP_PERIOD	=	266
    K_KP_DIVIDE	=	267
    K_KP_MULTIPLY	=	268
    K_KP_MINUS	=	269
    K_KP_PLUS	=	270
    K_KP_ENTER	=	271
    K_KP_EQUALS	=	272
    K_UP	=	273
    K_DOWN	=	274
    K_RIGHT	=	275
    K_LEFT	=	276
    K_INSERT	=	277
    K_HOME	=	278
    K_END	=	279
    K_PAGEUP	=	280
    K_PAGEDOWN	=	281
    K_F1	=	282
    K_F2	=	283
    K_F3	=	284
    K_F4	=	285
    K_F5	=	286
    K_F6	=	287
    K_F7	=	288
    K_F8	=	289
    K_F9	=	290
    K_F10	=	291
    K_F11	=	292
    K_F12	=	293
    K_F13	=	294
    K_F14	=	295
    K_F15	=	296
    K_NUMLOCK	=	300
    K_CAPSLOCK	=	301
    K_SCROLLOCK	=	302
    K_RSHIFT	=	303
    K_LSHIFT	=	304
    K_RCTRL	=	305
    K_LCTRL	=	306
    K_RALT	=	307
    K_LALT	=	308
    K_RMETA	=	309
    K_LMETA	=	310
    K_LSUPER	=	311
    K_RSUPER	=	312
    K_MODE	=	313
    K_HELP	=	315
    K_PRINT	=	316
    K_SYSREQ	=	317
    K_BREAK	=	318
    K_MENU	=	319
    K_POWER	=	320
    K_EURO	=	321
    K_LAST	=	323
