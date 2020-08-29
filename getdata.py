# -*- coding: utf-8 -*-
import csv
import random
import codecs
from urllib.request import urlopen
from collections import defaultdict

class GetData(object):
    def __init__(self):
        self.radicals = ['己', '目', '中', '工', '木', '巳', '王', '田', '丁', '日', '人', '一', '二', '十', '亖', '阝', 'ꓘ', '八', '口', '兀', '丌', '夂', '廿', '尹', '灬', 'モ', '卌', 'ン', 'ヨ', 'ム', 'ヤ', 'セ', '匕', 'ネ', 'コ', 'ラ', 'シ', '厂', 'ク', 'ケ', 'ソ', '⻌', 'イ', '宀', 'ト', '个', 'ナ', '彳', '扌', '弋', '犭', '爿', '戈', '斗', '凵', '艾', '卩', '尺', '亅', '廾', '匕', '冂', '几', '尸', '冫', '匚', '广', '勹', '杰', '丙', '之']
        self.kanjis = set()
        self.ease = {}
        self.colors = {}
        self.descriptions = {}
        self.spotlight = set()
        self.components = defaultdict(list)
        self.anticomponents = defaultdict(list)
        self.similars = defaultdict(list)
        self.semilars = defaultdict(list)

    def get(self, kanjis_url, kanjisim_url, kanjis_file_name, kanjisim_file_name):
        response_kanjis = urlopen(kanjis_url)
        response_kanjisim = urlopen(kanjisim_url)

        lines_kanjis = response_kanjis.read().decode('utf-8').splitlines()
        lines_kanjisim = response_kanjisim.read().decode('utf-8').splitlines()

        kanjis_file = codecs.open(kanjis_file_name, 'w', 'utf-8')
        kanjisim_file = codecs.open(kanjisim_file_name, 'w', 'utf-8')

        if(len(lines_kanjis) < 2 or len(lines_kanjisim) < 2):
            raise Exception('unavailable spreadsheet')

        for line in lines_kanjis:
            kanjis_file.write(line + "\r\n")
        for line in lines_kanjisim:
            kanjisim_file.write(line + "\r\n")

        kanjis_file.close()
        kanjisim_file.close()

        cr = csv.reader(lines_kanjis)

        kanjilist = []
        for row in cr:
            kanjilist.append(row)

        for i, k in enumerate(kanjilist):
            if i == 0 or k[0] == '':
                continue

            self.kanjis.add(k[0])
            percent =  (i + 1) / len(kanjilist)
            index = pow(percent, 9) # 1 is new, 0 is old.

            if k[8] == "" or k[8] == "#N/A":
                if i == 3:
                    raise Exception('unavailable spreadsheet')
                ease = 0
            else:
                ease = int(k[8]) # number of days until resched
            #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
            # ease += 2
            # antiease = 2 / math.pow(math.log(ease+3),1.8) # 10d -> .4, 30d -> .2, 60d -> .1
            antiease = max(1-.05*ease, 0)  # 5d -> .75, 10d -> .5, 20d -> 0

            # redness = (4*max(index, antiease) + min(index, antiease))/5
            redness = max(index, antiease)
            self.ease[k[0]] = redness
            #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
            #redness = math.pow(redness, 2)

            self.colors[k[0]] = '0.6 ' + str(redness) + ' 1.0'

            if i >= len(kanjilist)-4: # 4 most recent get spotlight
                self.colors[k[0]] = '0.8 1.0 1.0'
                self.spotlight.add(k[0])

            if random.random() < 0.015: # Random spotlight
                self.colors[k[0]] = '0.0 0.9 1.0'
                self.spotlight.add(k[0])
            self.descriptions[k[0]] = k[1] + " (" + k[2] + ")"

        #kanjis.remove('')

        for k in kanjilist:
            for kk in k[3]:#.split(" "):
                if kk in self.kanjis or kk in self.radicals:
                    self.components[k[0]].append(kk)
                    self.anticomponents[kk].append(k[0])
            splitkanjisim = k[4].split("###")
            for kk in splitkanjisim[0]:
                if kk in self.kanjis:
                    self.similars[k[0]].append(kk)
            if len(splitkanjisim) > 1:
                for kk in splitkanjisim[1]:
                    if kk in self.kanjis:
                        self.semilars[k[0]].append(kk)
