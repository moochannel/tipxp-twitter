"""
Configuration object that does not need to instantiate.

Usage:
> from bot_config import BotConfig
> BotConfig.SOME_PROPERTY
"""
import os
from collections import ChainMap

DEFAULTS = {
    'CONSUMER_KEY': None,
    'CONSUMER_SECRET': None,
    'ACCESS_TOKEN': None,
    'ACCESS_TOKEN_SECRET': None,
    'RPC_URL': None,
    'RPC_USER': None,
    'RPC_PASSWORD': None,
}


class Singleton(type):
    """Make class to be a singleton"""
    _instances = {}

    def __call__(self, *args, **kwargs):
        """If instance exists, just return it."""
        if self not in self._instances:
            self._instances[self] = super().__call__(*args, **kwargs)
        return self._instances[self]


class BotConfigFactory(object, metaclass=Singleton):
    """Factory provides BotConfig instance as a singleton."""

    def __init__(self):
        """Pick variables from environment variables, `setting.py`, DEFAULTS.

        Only the keys in `settings.py` are case insensitive."""
        environments = dict((key, val) for key, val in os.environ.items() if key in DEFAULTS)
        from_settings = {}
        try:
            import settings
            from_settings = dict((key.upper(), getattr(settings, key)) for key in dir(settings)
                                 if key.upper() in DEFAULTS)
        except ModuleNotFoundError:
            print('settings.py not found. continue with using environment variables.')

        _configs = ChainMap(environments, from_settings, DEFAULTS)

        for key, val in _configs.items():
            setattr(self, key, val)


BotConfig = BotConfigFactory()
