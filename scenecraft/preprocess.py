import os, shutil
from tqdm import tqdm
import numpy as np
import re
from difflib import SequenceMatcher

def match_sim(a, b):
    return SequenceMatcher(None, a, b).ratio()

def get_folder_size(folder_path):
    total_size = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    return total_size

sizes = []
cnt = 0
del_fns = []
for fn in os.listdir('assets/'):
    size = get_folder_size(os.path.join('assets/', fn))
    size /= 1e6
    if size > 1000:
        del_fns += [os.path.join('assets/', fn)]
for fn in del_fns:
    shutil.rmtree(fn)

from zipfile import ZipFile 
exps = []
for fn in tqdm(os.listdir('assets/')):
    if fn == '.DS_Store' or fn == 'data_dict':
        continue
    for fi in os.listdir(os.path.join('assets/', fn)):
        if '.zip' in fi:
            try:
                with ZipFile(os.path.join('assets/', fn, fi), 'r') as zObject: 
                    zObject.extractall(path=os.path.join('assets/', fn)) 
                zObject.close() 
                os.remove(os.path.join('assets/', fn, fi))
            except Exception as e:
                print(e)
                exps += [fn]
            break

for fn in os.listdir('assets/'):
    if fn == '.DS_Store' or fn == 'data_dict':
        continue
    print(fn)
    fs = []
    for i, j, k in os.walk(os.path.join('assets/', fn)):
        for ki in k:
            if ki != '.DS_Store' and '.obj' not in ki and '.mtl' not in ki:
                if 'normal' in ki or 'NORMAL' in ki or 'nor_' in ki or 'NOR_' in ki:
                    print(ki)
                    continue
                fs += [ki]
    fs = np.unique(fs)
    for fi in os.listdir(os.path.join('assets/', fn)):
        file_name = os.path.join('assets/', fn, fi)
        if '.mtl' in fi:
            try:
                with open(file_name, 'r') as f:
                    lines = f.readlines()
                    f.close()
                mtl = ''
                res = ''
                ress = {}
                imgs = []
                mat_key = ''
                for line in lines:
                    if line[0] == '#' or line == '\n':
                        res += line
                    if 'newmtl' in line:
                        if mtl != '':
                            if not imgs:
                                all_sim = [match_sim(mat_key, fsi) for fsi in fs]
                                if np.max(all_sim) >= 0.3:
                                    mtl += '\nmap_Kd ' + fs[np.argmax(all_sim)]
                                    print(mat_key, fs[np.argmax(all_sim)])
                                    print('add!!!')
                            res += '\n' + mtl + '\n'
                            mtl = ''
                            mat_key = ''
                            imgs = []
                        mtl += line
                        mat_key = line[:-1].split('newmtl ')[-1]
                    else:
                        if 'refl' in line:
                            continue
                        if 'map_' in line or 'bump' in line:
                            tokens = line.split(' ')
                            map_token = tokens[0]
                            remain = ' '.join(tokens[1:])
                            last_token = remain.split('\\')[-1].split('/')[-1].replace('\n', '')
                            if last_token not in fs:
                                print(last_token + '   missing !!!!!')
                            else:
                                mtl += map_token + ' ' + last_token + '\n'
                                imgs += [last_token[:-1]]
                        elif mtl != '':
                            mtl += line
                if mtl != '':
                    if not imgs:
                        all_sim = [match_sim(mat_key, fsi) for fsi in fs]
                        if np.max(all_sim) >= 0.3:
                            mtl += '\nmap_Kd ' + fs[np.argmax(all_sim)]
                            print(mat_key, fs[np.argmax(all_sim)])
                            print('add!!!')
                    res += '\n' + mtl+ '\n'
                res = re.sub(r'\n\n+', '\n\n', res)
                with open(file_name, 'w') as f:
                    f.write(res)
                    f.close()
            except Exception as e:
                print(e) 