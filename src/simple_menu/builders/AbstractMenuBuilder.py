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

    def build(self):
        """
            Abstract method which builds and returns a new L{AbstractMenuBuilder.Menu} from the information
            collected by this builder.

            @rtype: AbstractMenuBuilder.Menu
        """
        raise NotImplementedError()
