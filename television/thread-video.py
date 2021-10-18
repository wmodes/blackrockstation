"""Video thread class for television subsystem."""

from shared import config
from shared.controller import Controller

import os
import platform

logger = logging.getLogger()


class Thread_video(Controller):
    """Video thread class."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.system = __determine_platform()

    """
        SETUP
    """

    def __determine_platform(self):
        """
        Determine platform we are running on.

        Returns a short string we can use as an index.
        """
        if 'arm' in platform.platform().lower():
            return "rapsi"
        elif 'darwin' in platform.platform().lower():
            return "macos"
