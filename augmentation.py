import librosa
import numpy as np
import os
import random
import argparse
from pyparsing import srange
import soundfile as sf
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

ROOT_DATA = "/home/hieuld/workspace/ASVspoof2019/PA"

# ADD BEFORE ANY OTHER PREPROCESSING
def time_stretching(signal):
    random_speedperturb = [0.95, 1.00, 1.05]
    stretch_rate = random.choice(random_speedperturb)
    new_signal = librosa.effects.time_stretch(signal, stretch_rate)    
    return new_signal
    
def noise_addition(signal_dir, noise_listname, data_folder):
    noise_name = random.choice(noise_listname)
    noise, noise_sr = librosa.load(os.path.join(data_folder, noise_name))
    signal, signal_sr = librosa.load(signal_dir)
    
    assert noise_sr == signal_sr
    print(noise_sr)
    print(signal_sr)
    # NEED PADDING NOISE
    if len(noise) < len(signal):
        # PADDING NOISE
        resid_len = len(signal) - len(noise)
        noise = np.pad(noise, (0, resid_len), 'constant', constant_values=0)
        # ADD NOISE
        noise_signal = signal + noise
    else:
        # PADDING SIGNAL
        add = 0
        resid_len = len(noise) - len(signal)
        if resid_len % 2 :
            add = 1
        resid_len = resid_len//2
        signal = np.pad(signal, (resid_len, resid_len + add), 'constant', constant_values=(0, 0))
        # ADD NOISE
        noise_signal = signal + noise

    return noise_signal, signal_sr, noise_name

def sortFunc(name):
    name = name.split('.')[0]
    name = name.split('_')[-1]
    return int(name)

def make_augdata(kind, ratio):
    cm_file = os.path.join(ROOT_DATA, "ASVspoof2019_PA_cm_protocols" , "ASVspoof2019.PA.cm." + kind + ".trn.txt")
    noisy_folder = os.path.join(ROOT_DATA, "ASVspoof2019_PA_" + kind , "noisy_signal")
    noise_folder = os.path.join(ROOT_DATA, "ASVspoof2019_PA_" + kind , "noise")
    noise_listdir = os.listdir(noise_folder)
    data_folder = os.path.join(ROOT_DATA, "ASVspoof2019_PA_" + kind , "flac")
    data_list = os.listdir(data_folder)
    data_list.sort(key=sortFunc)
    
    bona_data_list = data_list[:5400]
    spoof_data_list = data_list[5400:]
    bona_data_list = random.sample(bona_data_list, k= int(len(bona_data_list)*ratio ))
    spoof_data_list = random.sample(spoof_data_list, k= int(len(spoof_data_list)*(ratio+0.1)))

    bona_spoof_datalist = [bona_data_list, spoof_data_list]
    labels = ['bonafide', 'spoof', '-', 'BB']

    for i in range(2):
        for signal_dir in tqdm(bona_spoof_datalist[i], total=len(bona_spoof_datalist[i])):
            signal_dir_full = os.path.join(data_folder, signal_dir)
            noisy_signal, sr, noise_name = noise_addition(signal_dir_full, noise_listdir, noise_folder)
            stretched_signal = time_stretching(noisy_signal)

            # ADD TO FOLDER
            noisy_signal_dir = signal_dir.split('.')[0] + '_' + noise_name
            sf.write(os.path.join(noisy_folder, noisy_signal_dir), stretched_signal, sr)
            
            # ADD TO CM 
            # Open a file with access mode 'a'
            with open(cm_file, "a+") as file_object:
                # Move read cursor to the start of file.
                file_object.seek(0)
                # If file is not empty then append '\n'
                data = file_object.read(100)
                if len(data) > 0 :
                    file_object.write("\n")
                # Append 'hello' at the end of file
                new_line = "PA_noise " + noisy_signal_dir.split('.')[0] + " bbb " + labels[2+i] + " " + labels[i] 
                file_object.write(new_line)

def main(kind, ratio):
    make_augdata(kind, ratio)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--kind', action='store', type=str, default='train')
    parser.add_argument('--ratio', action='store', type=float, default=0.2)
    parser.add_argument('--random-seed', action='store', type=int, default=42)
    args = parser.parse_args()

    kind = args.kind
    ratio = args.ratio
    random_seed = args.random_seed
    np.random.seed(random_seed)
    random.seed(random_seed)

    main(kind, ratio)