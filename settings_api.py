import json
import os
import datetime as dt

__author__ = 'Gareth Mok'


class Settings:
    def __init__(self):
        """
        Settings file for YoutubeFeed application
        """
        self.filepath = 'settings.json'
        self.data = {}

        if os.path.isfile(self.filepath):
            self.read()
            if not all(key in self.data.keys() for key in ('API Key', 'Client Secret File', 'Last Checked')):
                self.data = {'API Key': '', 'Client Secrets File': '', 'Last Checked': str(dt.date.today())}
                self.write()

            if not self.data['Last Checked']:
                self.data['Last Checked'] = str(dt.date.today())
                self.write()

        else:
            self.data = {'API Key': '', 'Client Secrets File': '', 'Last Checked': str(dt.date.today())}
            self.write()

    def new(self):
        with open(self.filepath, 'w') as outfile:
            json.dump({}, outfile, indent=4)
        self.read()

    def read(self):
        with open(self.filepath, 'r') as readfile:
            self.data = json.load(readfile)

    def write(self):
        with open(self.filepath, 'w') as outfile:
            json.dump(self.data, outfile, indent=4)
        self.read()

    def get_api_key(self):
        """
        :return: Youtube API key string
        """
        return self.data['API Key']

    def get_client_secrets_file(self):
        """
        :return: Client Secret File Name
        """
        return self.data['Client Secret File']

    def get_last_checked(self):
        """
        :return: date string in '%Y-%m-%d' format
        """
        return self.data['Last Checked']

    def update_last_run(self, date):
        """
        Update the last run date
        :type date: str
        :param date: date string in '%Y-%m-%d' format
        :return:
        """
        assert isinstance(date, str)

        self.data['Last Checked'] = date
        self.write()
