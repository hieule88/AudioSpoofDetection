import os
import librosa
from tqdm import tqdm
root = "/home/hieuld/workspace/ASVspoof2019/PA/ASVspoof2019_PA_train/flac"
list_dir = os.listdir(root)
index = 0
count = 0
for dir in tqdm(list_dir, total=len(list_dir)):
    dir = os.path.join(root, dir)
    wav_file, sr = librosa.load(dir)
    index = index + 1
    if sr != 16000:
        print(dir)
        print(sr)
    if index %1000 == 0:
        print(count)

print(len(list_dir))
print(index)