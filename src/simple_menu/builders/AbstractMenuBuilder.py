from types import StringType, TupleType, DictType, ListType, UnicodeType
import collections


class AbstractMenuBuilder(object):
    """
        Abstract class used the build a L{menu<AbstractMenuBuilder.Menu>}. It provides basic
        functionalities and hooks for the task.
    """

    Menu = collections.namedtuple('Menu',
                                        (
                                       'sections',
                                        'callback',
                                        )
                                  )
    """
        Menu root.
        Properties of the menu root:
            - sections: tuple of L{sections<AbstractMenuBuilder.Section>}
            - callback: single function to be executed without parameters. This is a function to run for this
            level.
    """

    Section = collections.namedtuple(
                                     'Section',
                                     (
                                      'name',
                                      'label',
                                      'callback',
                                      'sections',
                                      )
                                     )
    """
        One section in a L{menu<AbstractMenuBuilder.Menu>}.
        Properties of the menu root:
            - name: string name of the section.
            - label: (optional) string label of the section. If C{None} it could be defaulted to C{name}
            - callback: (optional) single function to be executed without parameters. This is a function to
            run for this level. It is C{None} when not a function.
            - sections: (optional) tuple of L{sub sections<AbstractMenuBuilder.Section>}
    """

    DYNAMIC = "dynamic"
    """
        Portion of an option of a section used in the property file to specify that this section
        will be dynamically filled in at runtime.
    """


    def build(self, dynamic_sections_by_opt_name=None):
        """
            Abstract method which builds and returns a new L{AbstractMenuBuilder.Menu} from the information
            collected by this builder.

            @param dynamic_sections_by_opt_name: additional set of sections defined as L{AbstractMenuBuilder.
            DYNAMIC}
            @rtype: AbstractMenuBuilder.Menu

            @precondition: dynamic_sections_by_opt_name is None or isinstance(dynamic_sections_by_opt_name, DictType)
            @precondition: dynamic_sections_by_opt_name is None or all(
                            isinstance(k, StringType)
                            and isinstance(v, (TupleType, ListType))
                            for k, v in dynamic_sections_by_opt_name.iteritems())
            @precondition: dynamic_sections_by_opt_name is None or all(
                            isinstance(v, (TupleType, ListType))
                            and len(v) == 2
                            and isinstance(v[0], (StringType, UnicodeType))
                            and (v[1] is None or isinstance(v[1], (StringType, UnicodeType)))
                            for values in dynamic_sections_by_opt_name.itervalues()
                            for v in values
                                                            )
        """
        assert dynamic_sections_by_opt_name is None or isinstance(dynamic_sections_by_opt_name, DictType)
        assert dynamic_sections_by_opt_name is None or all(
                            isinstance(k, StringType)
                            and isinstance(v, (TupleType, ListType))
                            for k, v in dynamic_sections_by_opt_name.iteritems())
        assert dynamic_sections_by_opt_name is None or all(
                            isinstance(v, (TupleType, ListType))
                            and len(v) == 2
                            and isinstance(v[0], (StringType, UnicodeType))
                            and (v[1] is None or isinstance(v[1], (StringType, UnicodeType)))
                            for values in dynamic_sections_by_opt_name.itervalues()
                            for v in values
                                                            )
        raise NotImplementedError()
