#!/bin/bash

# Begin configuration section.
nj=1
cmd=run.pl
feats_config=conf/feats/spec.conf
compress=true

# End configuration section.
if [ -f path.sh ]; then . ./path.sh; fi
. parse_options.sh || exit 1;

if [ $# != 2 ]; then
   echo "usage: predict.sh <data-name> <model-dir> - for data stored input";
   echo "or";
   echo "usage: predict.sh stream <model-dir> - for streaming input"
   exit 1;
fi

data=$1
if [ "$data" == "stream" ]; then 
   data="input"
   # Get streaming input by python
   python3 getinput.py
fi

modeldir=$2
inputfolder=/home/hieuld/workspace/ASV-anti-spoofing-with-Res2Net/input
logdir=$inputfolder/log
spectrogramdir=$inputfolder/spec

mkdir -p $spectrogramdir || exit 1;
mkdir -p $logdir || exit 1;

# create protofile 
bitpersample=$(sox --info -b $inputfolder/$data.flac)

if [ $bitpersample -ne 16 ]; then 
   echo "$bitpersample"
   sox $inputfolder/$data.flac -b 16 $inputfolder/${data}_16.flac
   rm $inputfolder/$data.flac
   mv $inputfolder/${data}_16.flac $inputfolder/$data.flac
   echo "Converted to 16 bits-per-sample"
fi

echo "$data" > ${inputfolder}/protofile.txt
protofile=$inputfolder/protofile.txt

# flac to wav
awk -v dir="${inputfolder}" \
'{print $1" sox "dir"/"$1".flac -t wav - |"}' \
$protofile >${inputfolder}/wav.scp || exit 1

scp=$inputfolder/wav.scp

# create spectrogram
split_scps=""
for ((n=1; n<=nj; n++)); do
   split_scps="$split_scps $logdir/wav.$n.scp"
done

utils/split_scp.pl $scp $split_scps || exit 1;
# add ,p to the input rspecifier so that we can just skip over
# utterances that have bad wave data.

$cmd JOB=1:$nj $logdir/make_spectrogram.JOB.log \
   compute-spectrogram-feats  $vtln_opts --verbose=2 --config=$feats_config \
   scp,p:$logdir/wav.JOB.scp ark:- \| \
   copy-feats --compress=$compress ark:- \
   ark,scp:$spectrogramdir/raw_spectrogram.JOB.ark,$spectrogramdir/raw_spectrogram.JOB.scp \
   || exit 1;
   
# concatenate the .scp files together.
for ((n=1; n<=nj; n++)); do
  cat $spectrogramdir/raw_spectrogram.$n.scp || exit 1;
done > $inputfolder/feats.scp

rm $logdir/wav.*.scp  $logdir/segments.* 2>/dev/null

nf=`cat $inputfolder/feats.scp | wc -l`

# slicing
python3 feats_extraction/feat_slicing.py --in-scp ${inputfolder}/feats.scp --out-scp ${inputfolder}/feats_slicing.scp --out-ark ${inputfolder}/feats_slicing.ark || exit 1

confdir=conf/training_mdl/seresnet34.json

KALDI_ROOT='/home/hieuld/kaldi' python3 predict.py --modeldir $modeldir \
                                                   --specdir ${inputfolder}/feats_slicing.scp \
                                                   --confdir $confdir