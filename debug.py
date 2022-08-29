import os
import librosa
from tqdm import tqdm
cmfile = "/home/hieuld/workspace/ASVspoof2019/PA/ASVspoof2019_PA_cm_protocols/ASVspoof2019.PA.cm.eval.trl.txt"

with open(cmfile, mode='r') as f:
    temp = f.readlines()

cnt = 0 
for file in tqdm(temp, total=len(temp)):
    if_spoof = file.split()[-1]
    if if_spoof == "spoof":
        cnt = cnt + 1
print("Ratio of Spoof / SUM: ", cnt/len(temp))