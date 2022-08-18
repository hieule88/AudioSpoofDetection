# import os

# root = "/home/hieuld/workspace/ASVspoof2019/PA/ASVspoof2019_PA_train/noise"
# list_dir = os.listdir(root)
# index = 0
# for dir in list_dir:
#     index = index + 1
#     new_dir = dir[5:]
#     dir = os.path.join(root, dir)
#     new_dir = os.path.join(root, new_dir)
#     os.rename(dir, new_dir)

import numpy as np    
a = [1, 2, 3, 4, 5]
a = np.pad(a, (0, 2), 'constant', constant_values=0)
print(a)