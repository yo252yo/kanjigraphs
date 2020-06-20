# -*- coding: utf-8 -*-
import csv
import random
import codecs
from urllib.request import urlopen
from collections import defaultdict

class GetData(object):
    def get(kanjis_url, kanjisim_url, kanjis_file_name, kanjisim_file_name):
        response_kanjis = urlopen(kanjis_url)
        response_kanjisim = urlopen(kanjisim_url)

        lines_kanjis = response_kanjis.read().decode('utf-8').splitlines()
        lines_kanjisim = response_kanjisim.read().decode('utf-8').splitlines()

        kanjis_file = codecs.open(kanjis_file_name, 'w', 'utf-8')
        kanjisim_file = codecs.open(kanjisim_file_name, 'w', 'utf-8')


        for line in lines_kanjis:
            kanjis_file.write(line + "\r\n")
        for line in lines_kanjisim:
            kanjisim_file.write(line + "\r\n")

        kanjis_file.close()
        kanjisim_file.close()


        # ============== IMPORT DATA


        cr = csv.reader(lines_kanjis)

        kanjilist = []
        for row in cr:
            kanjilist.append(row)

        kanjis = set()
        colors = {}
        descriptions = {}
        for i, k in enumerate(kanjilist):
            if i == 0 or k[0] == '':
                continue

            kanjis.add(k[0])
            percent =  (i + 1) / len(kanjilist)
            index = pow(percent, 9) # 1 is new, 0 is old.

            if k[8] == "" or k[8] == "#N/A":
                ease = 0
            else:
                ease = int(k[8]) # number of days until resched
            #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
            # ease += 2
            # antiease = 2 / math.pow(math.log(ease+3),1.8) # 10d -> .4, 30d -> .2, 60d -> .1
            antiease = max(1-.05*ease, 0)  # 5d -> .75, 10d -> .5, 20d -> 0

            # redness = (4*max(index, antiease) + min(index, antiease))/5
            redness = max(index, antiease)
            #!!!!!!!!!!!!!!!!!!!! for now, everything will be around 0, so we'll artificially enforce
            #redness = math.pow(redness, 2)

            colors[k[0]] = '0.6 ' + str(redness) + ' 1.0'

            if i >= len(kanjilist)-4: # 4 most recent get spotlight
                colors[k[0]] = '0.8 1.0 1.0'

            if random.random() < 0.02: # Random spotlight
                colors[k[0]] = '0.0 0.9 1.0'
            descriptions[k[0]] = k[1] + " (" + k[2] + ")"

        #kanjis.remove('')

        radicals = ['己', '目', '中', '工', '木', '巳', '王', '田', '丁', '日', '人', '一', '二', '十', '亖', '阝', 'ꓘ', '八', '口', '兀', '丌', '夂', '廿', '尹', '灬', 'モ', '卌', 'ン', 'ヨ', 'ム', 'ヤ', 'セ', '匕', 'ネ', 'コ', 'ラ', 'シ', '厂', 'ク', 'ケ', 'ソ', '⻌', 'イ', '宀', 'ト', '个', 'ナ', '彳', '扌', '弋', '犭', '爿', '戈', '斗', '凵', '艾', '卩', '尺', '亅', '廾', '匕', '冂', '几', '尸', '冫', '匚', '广', '勹', '杰', '丙', '之']

        components = defaultdict(list)
        anticomponents = defaultdict(list)
        similars = defaultdict(list)
        semilars = defaultdict(list)

        for k in kanjilist:
            for kk in k[3]:#.split(" "):
                if kk in kanjis or kk in radicals:
                    components[k[0]].append(kk)
                    anticomponents[kk].append(k[0])
            splitkanjisim = k[4].split("###")
            for kk in splitkanjisim[0]:
                if kk in kanjis:
                    similars[k[0]].append(kk)
            if len(splitkanjisim) > 1:
                for kk in splitkanjisim[1]:
                    if kk in kanjis:
                        semilars[k[0]].append(kk)
        return (kanjis, colors, descriptions, components, anticomponents, radicals, similars, semilars)
