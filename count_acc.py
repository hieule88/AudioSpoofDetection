cm_scoring_file = '/home/hieuld/workspace/ASVmodel/scoring/cm_scores/SEResNet34-epoch15-dev_scores.txt'
THRESHOLD = -2.677955

true_ps = 0
true_ng = 0
false_ps = 0
false_ng = 0
with open(cm_scoring_file, 'r') as f :
    lines = f.readlines()
    total = len(lines)
    for line in lines:
        score = line.split()[-1]
        label = line.split()[-2]
        if float(score) < THRESHOLD and label == 'spoof':
            true_ps = true_ps + 1
        elif float(score) >= THRESHOLD and label == 'bonafide':
            true_ng = true_ng + 1
        elif float(score) < THRESHOLD and label == 'bonafide':
            false_ps = false_ps + 1
        elif float(score) >= THRESHOLD and label == 'spoof':
            false_ng = false_ng + 1

acc= (true_ng + true_ps) / total 
print(acc)
    