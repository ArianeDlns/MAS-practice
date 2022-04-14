#!/usr/bin/env python3

from enum import Enum

CRED = '\033[91m'
CGREEN = '\033[92m'
CYELLOW = '\033[93m'
CPURPLE = '\033[95m'
CEND = '\033[0m'


class MessagePerformative(Enum):
    """MessagePerformative enum class.
    Enumeration containing the possible message performative.
    """
    PROPOSE = CYELLOW + 'PROPOSE' + CEND
    ACCEPT = CYELLOW + 'ACCEPT' + CEND
    COMMIT = CGREEN + 'COMMIT' + CEND
    ASK_WHY = CRED + 'ASK_WHY' + CEND
    ARGUE = CPURPLE + 'ARGUE' + CEND
    QUERY_REF = 106
    INFORM_REF = 107

    def __str__(self):
        """Returns the name of the enum item.
        """
        return '{0}'.format(self.value)
