from ._configmanager import ConfigManager


class Sinric:
    def __init__(self, apiKey):
        self.m_configmanager = ConfigManager()
        self.m_configmanager.setApiKey(apiKey)
