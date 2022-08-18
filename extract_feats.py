# Suppose our dataset have just the flacs

# 1. PREPARE DATASET

# Protofile:  PA_0079    PA_T_0000001   aaa    -    bonafide
#            speaker_id     utt_id     Env_id        Label
#             PA_0095    PA_T_0005731   aaa    AA    spoof
#            speaker_id     utt_id     Env_id        Label                                                                                                                               

# utt2systemID
# utt2spk
# spk2utt
# wav.scp


# 2. EXTRACT SPEC FEAT 

# run make_spectrogram.sh


# 3. TRUNCATE FEATS AND GENERATE LABELS
# 
# feat_slicing.py --> out: feat.scp, feat.ark(contain spec data)
# convertID2index.py --> utt2index


# 4.INPUT AND OUTPUT
# What input have: file flac: PA_T_0000001.flac
#                  cm_protocols: ASVspoof2019.PA.cm.train.trn.txt:
#                       PA_0079 PA_T_0000001 aaa - bonafide
                   

# Need for output: feats_slicing.scp: PA_T_0000001  -  0     data/spec/PA_train/feats_slicing.ark:15
#                                        utt_id    index_s              line in ark file

#                  utt2index: PA_T_0000001  -  0                    0
#                                utt_id    index_slc    label (0: real, !0: spoof)