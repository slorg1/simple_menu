from ConfigParser import RawConfigParser
from types import StringType
import codecs
import collections
from simple_menu.builders.AbstractMenuBuilder import AbstractMenuBuilder


class PropertiesMenuBuilder(AbstractMenuBuilder):
    """
        Implementation of a L{menu builder<simple_menu.AbstractMenuBuilder.AbstractMenuBuilder>}. Builds a
        menu hierarchy from a properties file.

        The properties file is read using the C{UTF-8} encoding to attempt to accommodate with accented
        characters.
    """

    SEPARATOR = '.'
    """ Default separator (see initializer)"""

    DEFAULT_SETTINGS = "default_settings"
    """
        Portion defining the location of the settings for the L{root menu<simple_menu.builders.
        AbstractMenuBuilder.AbstractMenuBuilder.Menu>}.
    """

    LABEL = "label"
    """ Portion of an option of a section used in the property file to setup label. """

    CALLBACK = "callback"
    """ Portion of an option of a section used in the property file to setup a hook for a callback. """

    def __init__(self, properties_file, name_to_property_sep=SEPARATOR):
        """
             Initializes this menu builder from the given L{properties_file}.

             @type properties_file: StringType
             @param name_to_property_sep: separator used in the properties files. Each property should follow
             the format C{property}L{name_to_property_sep}C{PropertiesMenuBuilder.LABEL}.
             @type name_to_property_sep: StringType

             @precondition: len(properties_file) > 0
             @precondition: len(name_to_property_sep) > 0
        """
        assert isinstance(properties_file, StringType)
        assert properties_file
        assert isinstance(name_to_property_sep, StringType)
        assert name_to_property_sep

        self.__properties_file = properties_file
        self.__name_to_property_sep = name_to_property_sep

    def build(self):
        with codecs.open(self.__properties_file, 'r', encoding='utf8') as f:
            parser = RawConfigParser()
            parser.readfp(f)

        roots = []
        root_callback = None
        name_to_property_sep = self.__name_to_property_sep
        LABEL = PropertiesMenuBuilder.LABEL
        CALLBACK = PropertiesMenuBuilder.CALLBACK
        DEFAULT_SETTINGS = PropertiesMenuBuilder.DEFAULT_SETTINGS

        for section_name in parser.sections():
            if section_name == DEFAULT_SETTINGS:
                root_callback = parser.get(section_name, CALLBACK)
            else:
                sections = collections.OrderedDict()
                for option_str, value in parser.items(section_name):
                    option_l = option_str.split(name_to_property_sep)
                    if len(option_l) == 2:
                        opt_name, opt_property = option_l
                        if opt_name not in sections:
                            sections[opt_name] = [None] * 2
                        if opt_property == LABEL:
                            sections[opt_name][0] = value.encode('utf-8')
                        elif opt_property == CALLBACK:
                            sections[opt_name][1] = value
                        else:
                            print u'Unknown option %s' % opt_name.encode('utf-8')

                sections = tuple(AbstractMenuBuilder.Section(k, s[0], s[1], None) for k, s in sections.iteritems())
                if not sections:
                    raise ValueError("Not sections could be found.")
                roots.append(AbstractMenuBuilder.Section(section_name.encode('utf-8'), None, None, sections))

        return AbstractMenuBuilder.Menu(tuple(roots), root_callback, 2)

    def name_to_property_sep(): # @NoSelf
        def fget(self):
            return self.__name_to_property_sep
        return locals()

    name_to_property_sep = property(**name_to_property_sep())
    """
        Getter:
        =======
        Gets the name to property separator for this entity

        @rtype: StringType
        @postcondition: len(return) > 0

        Setter:
        =======
        Not settable.
    """

