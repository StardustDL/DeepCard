from api import get_result
import os
import shutil
from glob import glob
from PIL import Image

if __name__ == '__main__':
    image_files = glob('./test_images/*.*')
    result_dir = './test_results'
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    os.mkdir(result_dir)

    txt_file = os.path.join(result_dir, 'result.txt')
    txt_f = open(txt_file, 'w')

    for image_file in sorted(image_files):
        if ".gitkeep" in image_files:
            continue
        print("Finded file", image_file, end=" ")
        result = get_result(Image.open(image_file))
        print(":", result)
        txt_f.write(image_file.split('/')[-1].split('.')[0] + ':' + result + '\n')
    
    txt_f.close()