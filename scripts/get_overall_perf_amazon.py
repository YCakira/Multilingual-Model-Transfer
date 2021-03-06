# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# python get_overall_perf.py model_dir suffix src_lang
from collections import defaultdict
import os
import re
import sys


domains = ['books', 'dvd', 'music']
langs = ['en', 'de', 'fr', 'ja']


def get_overall_perf(folder, suffix, source_lang=None):
    devperf = defaultdict(lambda: {})
    testperf = defaultdict(lambda: {})
    for domain in domains:
        for i, lang in enumerate(langs):
            if source_lang:
                if source_lang == 1:
                    lang = f'en2{langs[i]}'
                    if lang == 'en':
                        continue
                elif source_lang == 3:
                    srcs = [l for l in langs if l != langs[i]]
                    lang = ''.join(srcs)+'2'+langs[i]
            logfile = os.path.join(folder, f"{domain}_{lang}_{suffix}", 'log.txt')
            if not os.path.exists(logfile):
                print('File not found:', logfile)
                continue
            else:
                print('Processing file:', logfile)
            with open(logfile) as inf:
                lines = inf.readlines()[-2:]
            try:
                devperf[domain][lang] = float(lines[0].split()[-1])
                testperf[domain][lang] = float(lines[1].split()[-1])
            except:
                print('Errors in ', logfile)
            
    rowtemp = "{0:8}{1:8}\t{2:8}"
    for domain in domains:
        if len(devperf[domain]) > 0:
            print(f'Domain: {domain}, Dev and Test')
            print(rowtemp.format('Lang', 'F1', 'F1'))
            for lang in devperf[domain]:
                row = [lang] + [devperf[domain][lang]] + [testperf[domain][lang]]
                print(rowtemp.format(*row))
            print(rowtemp.format(*['Avg',
                sum(devperf[domain].values())/len(devperf[domain]),
                sum(testperf[domain].values())/len(testperf[domain])]))
            print()


if __name__ == '__main__':
    assert len(sys.argv) > 1, 'Model dir is required.'
    suffix = sys.argv[2]
    src = 3
    if len(sys.argv) > 3:
        src = int(sys.argv[3])
    
    get_overall_perf(sys.argv[1], suffix, src)
    for seed in range(1, 6):
        new_suffix = suffix + '_seed' + str(seed)
        print(f"Results for seed {seed}:")
        get_overall_perf(sys.argv[1], new_suffix, src)
