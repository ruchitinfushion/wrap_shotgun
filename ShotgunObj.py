# -*- coding: utf-8 -*-
###################################################################
# Author: Mu yanru
# Date  : 2017.6
# Email : muyanru345@163.com
###################################################################

from shotgun_api3 import Shotgun
import ConfigParser
import sys
import os


class ShotgunObj(Shotgun):
    def __init__(self, base_url, script_name, api_key):
        super(ShotgunObj, self).__init__(base_url,
                                         script_name=script_name,
                                         api_key=api_key)

    def find_one_by_one(self, entity, filterList, fields):
        index = 1
        summarizeDataDict = self.summarize(entity_type=entity,
                                           filters=filterList,
                                           summary_fields=[{'field': 'id', 'type': 'count'}, ])
        count = summarizeDataDict['summaries']['id']
        while True:
            result = self.find(entity, filterList, fields, limit=1, page=index)
            if result:
                yield result[0], index, count
                index += 1
            else:
                break


class MyShotgun(ShotgunObj):
    _config = ConfigParser.SafeConfigParser()
    _config.read(os.path.realpath(sys.path[0]) + '/sg.conf')
    url = _config.get('shotgun', 'url')
    script = _config.get('shotgun', 'script')
    key = _config.get('shotgun', 'key')

    def __init__(self):
        super(MyShotgun, self).__init__(self.url, self.script, self.key)


my_sg = MyShotgun()