
mkdir -p logs || exit 1

randomseed=0 # 0, 1, 2, ...
# config=conf/training_mdl/seres2net50_26w_8s.json # configuration files in conf/training_mdl
config=conf/training_mdl/seresnet34.json # configuration files in conf/training_mdl
feats=pa_spec  # `pa_spec`, `pa_cqt`, `pa_lfcc`, `la_spec`, `la_cqt` or `la_lfcc`
runid=SEResNet34_finetune
pretrained=model_snapshots/SEResNet34/model_best.pth.tar
# runid=SERes2Net50_26w_8s_finetune
# pretrained=/home/hieuld/workspace/checkpoints/SERes2Net50_26w_8s/17_98.381.pth.tar

# echo "Start training."
# KALDI_ROOT='/home/hieuld/kaldi' python3 train.py --pretrained $pretrained --run-id $runid --random-seed $randomseed --data-feats $feats --configfile $config >logs/$runid || exit 1

echo "Start evaluation on all checkpoints."
for model in model_snapshots/$runid/*_[0-9]*.pth.tar; do
# for model in model_snapshots/$runid/15_97.777.pth.tar; do
# for model in /home/hieuld/workspace/checkpoints/$runid/model_best.pth.tar; do
    KALDI_ROOT='/home/hieuld/kaldi' python3 eval.py --random-seed $randomseed --data-feats $feats --configfile $config --pretrained $model || exit 1
done