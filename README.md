# ASV-anti-spoofing-with-Res2Net
This repository provides the implementation of the paper:
[Replay and Synthetic Speech Detection with Res2Net architecture](https://arxiv.org/abs/2010.15006) (ICASSP 2021).

## Checkpoints
Download checkpoint at: 
https://drive.google.com/file/d/1r7YcPf6eWeCwkZiTjfmOG8ysJOgZSlxd/view?usp=sharing
then move the checkpoint to "model_snapshots/SEResNet34_finetune/"

## Dependencies

1. Python and packages

    This code was tested on Python 3.7 with PyTorch 1.6.0.
    Other packages can be installed by:

    ```bash
    pip install -r requirements.txt
    ```

2. Kaldi

   This work used Kaldi to extract features, you need to install [Kaldi](https://github.com/kaldi-asr/kaldi) before running our scripts.

3. MATLAB

   The LFCC feature adopted in this work is extracted via the MALTAB codes privided by ASVspoof2019 orgnizers.

## Dataset
   This work is conducted on [ASVspoof2019 Dataset](https://arxiv.org/pdf/1904.05441.pdf), which can be downloaded via https://datashare.ed.ac.uk/handle/10283/3336. It consists of two subsets, i.e. physical access (PA) for replay attacks and logical access (LA) for synthetic speech attacks.

### For augmenting data.
   Need to modify some absolute directions
   ```
   python augmentation.py 
   ```
   
### Feature extraction
   
   The top script for feature extraction is `extract_feats.sh`, where the first step (Stage 0) is required to prepare dataset before feature extraction. Extraction for Spec (Stage 1). Required to be truncated by the Stage 4 in `extract_feats.sh`.
   ```bash
   ./extract_feats.sh --stage NUM
   ```

### System training and evaluation
   
   This repo supports different system architectures, as configured in the `conf/training_mdl` directory. You can specify the system architecture, acoustic features in `start.sh`, then run the codes below to train and evaluate your models.
   ```bash
   ./start.sh
   ```
   Remember to rename your `runid` in `start.sh` to differentiate each configuration.

   For evaluating systems\
   ```bash
   python scoring/evaluate_tDCF_asvspoof19.py scoring/la_asv_scores/ASVspoof2019.LA.asv.eval.gi.trl.scores.txt NameofScoringFile.txt
   ```

### Predict
   Input's Dependence: .flac, 16kHZ sample_rate, 16bits, place in input/tmp/
   ```bash
   ./predict.sh <input_name_without_tail>
   ```
   