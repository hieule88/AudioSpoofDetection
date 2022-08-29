import soundfile as sf
import os

# def compute_similar(au1, au2):
#     audiofolder = '/home/hieuld/workspace/ASVmodel/input/test'
#     audiolist = os.listdir(audiofolder)
#     audiolist.sort()
#     print(audiolist)
#     audiodata = []
#     for audio in audiolist:
#         audio = os.path.join(audiofolder, audio)
#         data, fs = sf.read(audio) 
#         audiodata.append(data)

#     import numpy as np
#     corr1 = np.correlate(a=audiodata[3], v=audiodata[4])
#     corr2 = np.correlate(a=audiodata[0], v=audiodata[1])

#     print(corr1)
#     print(corr2)
ROOTDIR = '/home/hieuld/workspace/AntiSpoof/ASVapp/ASVmodel/input/tmp'
import numpy as np
def compute_similar(au1, au2):
    audio1 = os.path.join(ROOTDIR, au1)
    audio2 = os.path.join(ROOTDIR, au2)
    au1, _ = sf.read(audio1)
    au2, _ = sf.read(audio2)
    if len(au1) > len(au2):
        au2 = np.pad(au2, (0, len(au1) - len(au2)), 'constant', constant_values=(0))
    else :
        au1 = np.pad(au1, (0, len(au2) - len(au1)), 'constant', constant_values=(0))
    corr = np.correlate(a=au1, v=au2)
    return corr
if __name__ == '__main__':
    au1 = 'atachfromaMinh.flac'
    au2 = 'atachfromaMinh_cutnoise.flac'
    au1 = os.path.join(ROOTDIR, au1)
    au2 = os.path.join(ROOTDIR, au2)
    print(compute_similar(au1,au2))