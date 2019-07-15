import torch
from torch.autograd import Variable
from PIL import Image
import numpy as np
import cv2
import torch.nn.functional as F
from recognize import keys, crnn_model as crnn, mydataset, crnn_utils

gpu = True
if not torch.cuda.is_available():
    gpu = False

model_path = './checkpoints/BANKCARD_CRNN_62.pth'
alphabet = keys.alphabet
imgH = 32

model = crnn.CRNN(imgH, 1, len(alphabet) + 1, 256)
if gpu:
    model = model.cuda()
print('loading pretrained model from %s' % model_path)
if gpu:
    model.load_state_dict( torch.load( model_path ) )
else:
    model.load_state_dict(torch.load(model_path,map_location=lambda storage,loc:storage))
model.eval()
print('done')
print('starting...')
converter = crnn_utils.strLabelConverter(alphabet)


def recognize_cv2_image(img):
    img = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
    image = Image.fromarray(np.uint8(img)).convert('L')
    h, w = img.shape[:2]
    imgW = imgH * w // h
    transformer = mydataset.resizeNormalize2((imgW, imgH))
    image = transformer( image )
    if gpu:
        image = image.cuda()
    image = image.view(1, *image.size())
    preds = model( image )
    preds = F.log_softmax(preds,2)
    conf, preds = preds.max( 2 )
    preds = preds.transpose( 1, 0 ).contiguous().view( -1 )

    preds_size = Variable( torch.IntTensor( [preds.size( 0 )] ) )
    raw_pred = converter.decode( preds.data, preds_size.data, raw=True )
    sim_pred = converter.decode( preds.data, preds_size.data, raw=False )
    return sim_pred.upper()

def recognize_batch_img(img_list):
    ratios = list()
    sim_preds = list()
    for img in img_list:
        w, h = img.size
        ratios.append(w / float(h))
    ratios.sort()
    max_ratio = ratios[-1]
    imgW = int(np.floor(max_ratio * imgH))
    transform = mydataset.resizeNormalize((imgW, imgH), is_test=True)
    images = [transform(image) for image in img_list]
    images = torch.cat([t.unsqueeze(0) for t in images], 0)
    if gpu:
        images = images.cuda()
    preds = model(images)
    preds = F.log_softmax(preds, 2)
    conf, preds = preds.max(2)
    for i in range(len(ratios)):
        pred = preds[:, i]
        pred_size = Variable(torch.IntTensor([pred.size(0)]))
        sim_pred = converter.decode(pred.data, pred_size.data, raw=False)
        sim_preds.append(sim_pred)
    print(sim_preds)
    return sim_preds

def recognize_PIL_image(img):
    w,h = img.size
    imgW = imgH * w // h
    transformer = mydataset.resizeNormalize2((imgW, imgH))
    image = transformer(img)
    if gpu:
        image = image.cuda()
    image = image.view(1, *image.size())
    preds = model(image)
    preds = F.log_softmax(preds, 2)
    conf, preds = preds.max(2)
    preds = preds.transpose(1, 0).contiguous().view(-1)

    preds_size = Variable(torch.IntTensor([preds.size(0)]))
    raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
    sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
    return sim_pred.upper()

if __name__ == '__main__':
    fname = 'data/images/000059.jpg'
    img = cv2.imread(fname)
    res = recognize_cv2_image(img)
    print(res)





