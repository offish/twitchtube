class TwitchTubeError(Exception):
    """ General error class for TwitchTube."""


class InvalidCategory(TwitchTubeError):
    """ Error for when the specified category is invalid """


class VideoPathAlreadyExists(TwitchTubeError):
    """ Error for when a path already exists. """


class NoClipsFound(TwitchTubeError):
    """ Error for when no clips are found. """
