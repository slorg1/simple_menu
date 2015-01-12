from types import DictType, StringType, UnicodeType, BooleanType
import collections
from simple_menu.builders.AbstractMenuBuilder import AbstractMenuBuilder

class MenuHandler(object):
    """
        Implements a menu 'handler' or navigator from a L{menu<simple_menu.builders.AbstractMenuBuilder.
        AbstractMenuBuilder.Menu>}.

        An instance of this class keeps track a its user's navigation through the menu. It is design to follow
        the basic navigation functionality through the menu with a multi directional arrow
        (up/down, left/right).

        L{Menu callback<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Menu.callback>} or
        L{section callbacks<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Section.callback>} are
        invoked without parameters once the user of this menu handler L{reaches<MenuHandler.next>} the same
        'node' (menu or section) twice in a row. This is only possible with leaf sections. For the root
        menu it is hit when hitting it as a lead twice in a row (MenuHandler.back twice).

        The descriptions of the navigation made in the contracts of this class assume a menu as follow:
        L1 (A)
          -> L2 (A.a)
          -> L2 (A.b)
        L1 (B)
          -> L2 (B.a)
            -> L3 (B.a.a)
    """

    def __init__(self, menu, callbacks=None):
        """
            Initializes this menu handler.

            @param menu: the menu to handle
            @type menu:AbstractMenuBuilder.Menu
            @param callbacks: dictionary of L{menu callback<simple_menu.builders.AbstractMenuBuilder.
            AbstractMenuBuilder.Menu.callback>} or L{section callbacks<simple_menu.builders.AbstractMenuBuilder.
            AbstractMenuBuilder.Section.callback>}. Those functions will be invoked as described by the class
            contract.

            @precondition: callbacks is None or isinstance(callbacks, DictType)
            @precondition: callbacks is None or all( isinstance(k, (StringType, UnicodeType)
                                                                and callable(v) for k, v in callbacks.iteritems())
        """
        assert isinstance(menu, AbstractMenuBuilder.Menu)
        assert menu.sections
        assert callbacks is None or isinstance(callbacks, DictType)
        assert callbacks is None or callbacks
        assert callbacks is None or isinstance(callbacks, DictType)
        assert callbacks is None or all(isinstance(k, (StringType, UnicodeType,))
                                        and callable(v) for k, v in callbacks.iteritems())

        self.__menu = menu
        self.__callbacks = callbacks
        self.__current_location = collections.deque()
        self.__current_location.append(0)

    def back(self):
        """
            Sets the L{current position<MenuHandler.get_current_location>} of the user on the menu to 1 level
            "back".

            Based on the class contract's sample menu:
                - if the position before invocation was on (A.a) after this method the user would end on (A)
                - if the position before invocation was on (A), executing this method again would trigger
                (A)'s callback (if present).
                - if the position before invocation was on (B), executing this method again would trigger
                (B)'s callback (if present).
                - if the position before invocation was on (B.a.a), executing this method again would set the
                new current location to (B.a).

            @return: returns the result of the invocation of L{current location method<MenuHandler.
            get_current_location>} on the new location.

            @postcondition: return is None or isinstance(return, (StringType, UnicodeType,))
        """
        if len(self.__current_location) > 1:
            self.__current_location.pop()
            use_callback = False
        else:
            use_callback = True

        return self.get_current_location(use_callback)

    def forward(self):
        """
            Sets the L{current position<MenuHandler.get_current_location>} of the user on the menu to 1 level
            "forward".

            Based on the class contract's sample menu:
                - if the position before invocation was on (A) after this method the user would end on (A.a)
                - if the position before invocation was on (A.a), executing this method again would trigger
                (A.a)'s callback (if present).
                - if the position before invocation was on (B.a.a), executing this method again would trigger
                (B.a.a)'s callback (if present).

            @return: returns the result of the invocation of L{current location method<MenuHandler.
            get_current_location>} on the new location.

            @postcondition: return is None or isinstance(return, (StringType, UnicodeType,))
        """
        section = self.__get_location(self.__menu.sections, iter(self.__current_location))
        if section.sections is not None:
            use_callback = False
            self.__current_location.append(0)
        else:
            use_callback = True

        return self.get_current_location(use_callback)

    def next(self):
        """
            Sets the L{current position<MenuHandler.get_current_location>} of the user on the menu to the "next"
            element in the menu on the same level. At the end of a level the method just loops back to the
            first element of the level.

            Based on the class contract's sample menu:
                - if the position before invocation was on (A) after this method the user would end on (B)
                - if the position before invocation was on (A.a) after this method the user would end on (A.b)
                - if the position before invocation was on (A.b) after this method the user would end on (A.a)
                - if the position before invocation was on (B.a.a), executing this method again would do
                nothing.

            @return: returns the result of the invocation of L{current location method<MenuHandler.
            get_current_location>} on the new location.

            @postcondition: return is None or isinstance(return, (StringType, UnicodeType,))
        """
        parent_section = self.__get_parent_current_location()

        if parent_section.sections is not None:
            current_idx = self.__current_location.pop()
            next_idx = current_idx + 1

            if len(parent_section.sections) == next_idx:
                next_idx = 0 # infinite loop

            self.__current_location.append(next_idx)

        return self.get_current_location()

    def previous(self):
        """
            Sets the L{current position<MenuHandler.get_current_location>} of the user on the menu to the "previous"
            element in the menu on the same level. At the end of a level the method just loops back to the
            last element of the level.

            Based on the class contract's sample menu:
                - if the position before invocation was on (B) after this method the user would end on (A)
                - if the position before invocation was on (A) after this method the user would end on (B)
                - if the position before invocation was on (A.a) after this method the user would end on (A.b)
                - if the position before invocation was on (A.b) after this method the user would end on (A.a)
                - if the position before invocation was on (B.a.a), executing this method again would do
                nothing.

            @return: returns the result of the invocation of L{current location method<MenuHandler.
            get_current_location>} on the new location.

            @postcondition: return is None or isinstance(return, (StringType, UnicodeType,))
        """

        parent_section = self.__get_parent_current_location()
        if parent_section.sections is not None:
            current_idx = self.__current_location.pop()

            if current_idx == 0:
                current_idx = len(parent_section.sections) # infinite loop

            next_idx = current_idx - 1

            self.__current_location.append(next_idx)

        return self.get_current_location()

    def get_current_location(self, use_callback=False):
        """
            From the current location internally kept, returns the
            L{section's label<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Section.label>}
            if L{use_callback} is set to C{False}.
            It L{use_callback} is set to C{True}, it will first execute the L{section's callback<simple_menu.
            builders.AbstractMenuBuilder.AbstractMenuBuilder.Section.callback>} or
            the L{menu's callback<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Menu.
            callback>} and returns the resulting string or C{None} if the callback returned C{None}.

            If no label or callbacks are defined, this method will return the L{section's name
            <simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Section.name>}

            @type use_callback: BooleanType

            @postcondition: return is None or isinstance(r, (StringType, UnicodeType,))
        """
        assert isinstance(use_callback, BooleanType)
        if len(self.__current_location) == 1 and use_callback: # root menu is a special sections
            section = self.__menu
        else:
            section = self.__get_location(self.__menu.sections, iter(self.__current_location))


        if use_callback and section.callback is not None:
            r = self.__callbacks[section.callback]()

            if r is None:
                return r

            assert isinstance(r, (StringType, UnicodeType,)), str(r)
            return r

        if section.label is not None:
            assert section.label
            return section.label

        assert section.name
        return section.name

    def __get_parent_current_location(self,):
        """
            Returns the parent L{section<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Section>} or
            the L{menu<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Menu>} for the the current
            location internally kept.

            @rtype: AbstractMenuBuilder.Menu or AbstractMenuBuilder.Section
        """
        if len(self.__current_location) <= 1: # we want the menu
            return self.__menu

        last_index = len(self.__current_location) - 2

        section = self.__menu
        for idx, loc in enumerate(self.__current_location):
            section = section.sections[loc]
            if last_index == idx:
                return section

    def __get_location(self, sections, location_iterator):
        """
            Returns the L{section<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Section>} or
            the L{menu<simple_menu.builders.AbstractMenuBuilder.AbstractMenuBuilder.Menu>} for the the current
            location internally kept.

            @param sections: tuple of sections to travel to get to the current location
            @type sections: TupleType
            @param location_iterator: iterator over the current location maintaining data structure. It yields
            integer indexes to be used in the L{sections}.

            @rtype: AbstractMenuBuilder.Menu or AbstractMenuBuilder.Section

            @precondition: iter(location_iterator)
        """
        idx = next(location_iterator)

        try:
            return self.__get_location(sections[idx].sections, location_iterator)
        except StopIteration:
            return sections[idx]
