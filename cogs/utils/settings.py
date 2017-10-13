from .dataIO import dataIO
from copy import deepcopy
import discord
import os
import argparse

default_path = "data/bot/settings.json"


class Settings:

    def __init__(self, path=default_path, parse_args=True):
        self.path = path
        self.check_folders()
        self.default_settings = {
            "TOKEN": None, #bot token
            "BOTSDISCORDPW_TOKEN": None, # https://bots.discord.pw token
            "DISCORDBOTSORG_TOKEN": None, # https://discordbots.org token
            "OWNER": None, #owner id
            "DEVELOPER": None, #dev id
            "PREFIXES": [], #server prefix
			"DEV_MODE": "0", #dev mode
            "default": {"ADMIN_ROLE": "NanoBot Admin",
                        "MOD_ROLE": "NanoBot Mod"}
			}
        self._memory_only = False

        if not dataIO.is_valid_json(self.path):
            self.bot_settings = deepcopy(self.default_settings)
            self.save_settings()
        else:
            current = dataIO.load_json(self.path)
            if current.keys() != self.default_settings.keys():
                for key in self.default_settings.keys():
                    if key not in current.keys():
                        current[key] = self.default_settings[key]
                        print("Adding " + str(key) +
                              " field to settings.json")
                dataIO.save_json(self.path, current)
            self.bot_settings = dataIO.load_json(self.path)

        self.save_settings()

    def check_folders(self):
        folders = ("data", os.path.dirname(self.path), "cogs", "cogs/utils")
        for folder in folders:
            if not os.path.exists(folder):
                print("Creating " + folder + " folder...")
                os.makedirs(folder)

    def save_settings(self):
        if not self._memory_only:
            dataIO.save_json(self.path, self.bot_settings)

    @property
    def owner(self):
        return self.bot_settings["OWNER"]

    @owner.setter
    def owner(self, value):
        self.bot_settings["OWNER"] = value

    @property
    def dev(self):
        return self.bot_settings["DEVELOPER"]

    @dev.setter
    def dev(self, value):
        self.bot_settings["DEVELOPER"] = value

    @property
    def token(self):
        return os.environ.get("NANO_TOKEN", self.bot_settings["TOKEN"])

    @token.setter
    def token(self, value):
        self.bot_settings["TOKEN"] = value

    @property
    def dev_mode(self):
        return self.bot_settings["DEV_MODE"]

    @property
    def login_credentials(self):
        if self.token:
            return (self.token)
        else:
            return tuple()

    @property
    def prefixes(self):
        return self.bot_settings["PREFIXES"]

    @prefixes.setter
    def prefixes(self, value):
        assert isinstance(value, list)
        self.bot_settings["PREFIXES"] = value

    @property
    def discordbotsorg_token(self):
        return self.bot_settings["DISCORDBOTSORG_TOKEN"]

    @property
    def botsdiscordpw_token(self):
        return self.bot_settings["BOTSDISCORDPW_TOKEN"]

    @property
    def default_admin(self):
        if "default" not in self.bot_settings:
            self.update_old_settings()
        return self.bot_settings["default"].get("ADMIN_ROLE", "")

    @default_admin.setter
    def default_admin(self, value):
        if "default" not in self.bot_settings:
            self.update_old_settings()
        self.bot_settings["default"]["ADMIN_ROLE"] = value

    @property
    def default_mod(self):
        if "default" not in self.bot_settings:
            self.update_old_settings_v1()
        return self.bot_settings["default"].get("MOD_ROLE", "")

    @default_mod.setter
    def default_mod(self, value):
        if "default" not in self.bot_settings:
            self.update_old_settings_v1()
        self.bot_settings["default"]["MOD_ROLE"] = value

    @property
    def servers(self):
        ret = {}
        server_ids = list(
            filter(lambda x: str(x).isdigit(), self.bot_settings))
        for server in server_ids:
            ret.update({server: self.bot_settings[server]})
        return ret

    def get_server(self, server):
        if server is None:
            return self.bot_settings["default"].copy()
        assert isinstance(server, discord.Server)
        return self.bot_settings.get(server.id,
                                     self.bot_settings["default"]).copy()

    def get_server_admin(self, server):
        if server is None:
            return self.default_admin
        assert isinstance(server, discord.Server)
        if server.id not in self.bot_settings:
            return self.default_admin
        return self.bot_settings[server.id].get("ADMIN_ROLE", "")

    def set_server_admin(self, server, value):
        if server is None:
            return
        assert isinstance(server, discord.Server)
        if server.id not in self.bot_settings:
            self.add_server(server.id)
        self.bot_settings[server.id]["ADMIN_ROLE"] = value
        self.save_settings()

    def get_server_mod(self, server):
        if server is None:
            return self.default_mod
        assert isinstance(server, discord.Server)
        if server.id not in self.bot_settings:
            return self.default_mod
        return self.bot_settings[server.id].get("MOD_ROLE", "")

    def set_server_mod(self, server, value):
        if server is None:
            return
        assert isinstance(server, discord.Server)
        if server.id not in self.bot_settings:
            self.add_server(server.id)
        self.bot_settings[server.id]["MOD_ROLE"] = value
        self.save_settings()

    def get_server_prefixes(self, server):
        if server is None or server.id not in self.bot_settings:
            return self.prefixes
        return self.bot_settings[server.id].get("PREFIXES", [])

    def set_server_prefixes(self, server, prefixes):
        if server is None:
            return
        assert isinstance(server, discord.Server)
        if server.id not in self.bot_settings:
            self.add_server(server.id)
        self.bot_settings[server.id]["PREFIXES"] = prefixes
        self.save_settings()

    def get_prefixes(self, server):
        """Returns server's prefixes if set, otherwise global ones"""
        p = self.get_server_prefixes(server)
        return p if p else self.prefixes

    def add_server(self, sid):
        self.bot_settings[sid] = self.bot_settings["default"].copy()
        self.save_settings()
