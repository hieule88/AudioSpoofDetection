import argparse
import librosa
import os
import soundfile as sf
ROOTPATH = 'input/tmp/' 

def convert(audir):
    absdir = os.path.join(ROOTPATH, audir)
    name = audir.split('.')[-2]
    audio, sr = librosa.load(absdir, sr=16000)
    sf.write(ROOTPATH + name + '.flac', audio, sr, 'PCM_16')
    os.remove(absdir)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--audir', action='store', type=str, default='')
    args = parser.parse_args()
    audir = args.audir
    convert(audir)