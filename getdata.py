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

    def get(self, kanjis_url, kanjis_file_name):
        print("Getting kanjis")
        response_kanjis = urlopen(kanjis_url)

        lines_kanjis = response_kanjis.read().decode('utf-8').splitlines()

        kanjis_file = codecs.open(kanjis_file_name, 'w', 'utf-8')

        if(len(lines_kanjis) < 2):
            raise Exception('unavailable spreadsheet')

        for line in lines_kanjis:
            kanjis_file.write(line + "\r\n")

        kanjis_file.close()

        cr = csv.reader(lines_kanjis)

        kanjilist = []
        for row in cr:
            kanjilist.append(row)

        for i, k in enumerate(kanjilist):
            if i == 0 or k[0] == '':
                continue

            self.kanjis.add(k[0])

            if len(k) < 8:
                raise Exception('spreadsheet has empty lines:' + str(i) + "/" + k[0])
            elif k[8] == "" or k[8] == "#N/A":
                if i == 3:
                    raise Exception('spreadsheet has no data')
                ease = 0
            else:
                ease = 1 - float(k[8])
            self.ease[k[0]] = ease
            self.colors[k[0]] = '0.6 ' + str(ease) + ' 1.0'

            if i >= len(kanjilist)+1:#-4: # 4 most recent get spotlight
                self.colors[k[0]] = '0.8 1.0 1.0'
                self.spotlight.add(k[0])

            if random.random() < 0.02: # Random spotlight
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
        return True

    def bufferKanjiSimData(self, kanjisim1_url, kanjisim2_url, kanjisim_file_name):
        print("Getting kanjisim")
        response_kanjisim1 = urlopen(kanjisim1_url, timeout=10)
        response_kanjisim2 = urlopen(kanjisim2_url, timeout=10)

        lines_kanjisim1 = response_kanjisim1.read().decode('utf-8').splitlines()
        lines_kanjisim2 = response_kanjisim2.read().decode('utf-8').splitlines()

        if(len(lines_kanjisim1) < 2 or len(lines_kanjisim2) < 2):
            return False

        kanjisim_file = codecs.open(kanjisim_file_name, 'w', 'utf-8')


        for line in lines_kanjisim1:
            kanjisim_file.write(line + "\r\n")
        for line in lines_kanjisim2:
            kanjisim_file.write(line + "\r\n")

        kanjisim_file.close()
        return True
