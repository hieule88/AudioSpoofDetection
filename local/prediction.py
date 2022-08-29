import numpy as np
import os
import random
import shutil
import time
import warnings
from collections import defaultdict
from functools import reduce

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.distributed as dist
import torch.optim
import torch.utils.data
import torch.utils.data.distributed
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
from tqdm import tqdm

def prediction(val_loader, model, device, output_file, utt2systemID_file):
    
    # switch to evaluate mode
    utt2scores = defaultdict(list) 
    utt2label = defaultdict(list) 
    model.eval()
    # find = False
    # samples = 0
    # print(len(val_loader))
    with torch.no_grad():
        for i, (utt_list, input, target) in tqdm(enumerate(val_loader), total= len(val_loader)):
            input  = input.to(device, non_blocking=True)
            target = target.to(device, non_blocking=True).view((-1,))

            # compute output
            output = model(input)
            pred = [out.argmax().cpu().detach().numpy() for out in output]
            score = output[:,0] # use log-probability of the bonafide class for scoring 

            for index, utt_id in enumerate(utt_list):
                curr_utt = ''.join(utt_id.split('-')[0])
                utt2scores[curr_utt].append(score[index].item()) 
                utt2label[curr_utt].append(pred[index].item())
    
        # first do averaging
        with open(utt2systemID_file, 'r') as f:
            temp = f.readlines()
        content  = [x.strip() for x in temp]
        utt_list = [x.split()[0] for x in content]
        id_list  = [x.split()[1] for x in content]

        eerfile = output_file+'.eer'
        with open(output_file, 'w') as f, open(eerfile, 'w') as eerf:
            for index, utt_id in enumerate(utt_list):
                score_list = utt2scores[utt_id]
                label_list = utt2label[utt_id]
                assert score_list != [], '%s' %utt_id   
                avg_score  = reduce(lambda x, y: x + y, score_list) / len(score_list)
                avg_label  = reduce(lambda x, y: max(x,y), label_list)
                spoof_id = id_list[index]
                if spoof_id == '-':
                    f.write('%s %s %s %f %f\n' % (utt_id, '-', 'bonafide', avg_score, avg_label))
                    eerf.write('%f target\n' %avg_score)
                else: 
                    f.write('%s %s %s %f %f\n' % (utt_id, spoof_id, 'spoof', avg_score, avg_label))
                    eerf.write('%f nontarget\n' %avg_score)