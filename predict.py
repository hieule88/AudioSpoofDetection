import torch 
import argparse
from kaldi_io import read_mat
import numpy as np
from model import Detector
import json

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# read input 
def readinput(specdir):
    with open(specdir) as f:
        temp = f.readlines()
    content = [x.strip() for x in temp]
    ark_dic = {index: i.split()[1] for (index, i) in enumerate(content)}
    inputtomodel = np.expand_dims(read_mat(ark_dic[0]), axis=0)
    inputtomodel = torch.tensor(inputtomodel).to(device, non_blocking=True)
    inputtomodel = inputtomodel.unsqueeze(0)
    return inputtomodel

# load model 
def loadmodel(modeldir, modelconf):
    # build model
    kwargs = {'num_workers': 4, 'pin_memory': True} if device == torch.device('cuda') else {}
    # create model
    model = Detector(**modelconf).to(device) 

    checkpoint = torch.load(modeldir, map_location=lambda storage, loc: storage)
    from collections import OrderedDict
    state_dict=checkpoint['state_dict']
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:] # remove `module.`
        new_state_dict[name] = v
        check_module_resid = k[:6]
    if check_module_resid != 'module':
        new_state_dict = checkpoint['state_dict']
    model.load_state_dict(new_state_dict)
    return model

# predict
def predict(model, data, threshold):
    model.eval()
    with torch.no_grad():
        output = model(data)
        print('ALL OUTPUT: ', output)
    print(output)
    # output = output[:,0]
    output = output.argmax().cpu().detach().numpy()
    print('OUTPUT: ', output)
    # print('THRESHOLD: ', threshold)
    # if output < threshold:
    if output:
        print('Replay Attack')
    else:
        print('Successful Authentication')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--modeldir', action='store', type=str, default='')
    parser.add_argument('--confdir', action='store', type=str, default='')
    parser.add_argument('--specdir', action='store', type=str, default='')
    parser.add_argument('--threshold', action='store', type=float, default=-0.0001)

    args = parser.parse_args()
    modeldir = args.modeldir
    confdir = args.confdir
    specdir = args.specdir
    threshold = args.threshold
    
    with open(confdir) as json_file:
        config = json.load(json_file)
    modelconf = config['model_params']
    model = loadmodel(modeldir, modelconf)
    inputtomodel = readinput(specdir)
    
    predict(model, inputtomodel, threshold)  