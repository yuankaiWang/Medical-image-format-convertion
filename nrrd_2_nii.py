import os
from glob import glob
import nrrd #pip install pynrrd, if pynrrd is not already installed
import nibabel as nib #pip install nibabel, if nibabel is not already installed
import numpy as np
def gather_files(root_dir, keep_suffixs=['jpg', 'png']):
    """
    根据文件后缀递归获取root_dir下所有的该类型文件
    输出：数组，每个元素是一个文件路径
    """
    file_counts = {}
    for suffix in keep_suffixs:
        file_counts[suffix] = 0
    n_files = 0
    all_files = []
    for parent, dirnames, filenames in os.walk(root_dir, followlinks=False):
        for filename in filenames:
            for suffix in keep_suffixs:
                if filename.endswith(suffix):
                    file_counts[suffix] += 1
                    file_path = os.path.join(parent, filename)
                    all_files.append(file_path)
                    n_files += 1
                    break
    return all_files



# ----------------------------------------------------------------------------
# Author Yuankai
# Time:2023-08-01
# This code could be work correctlly
# ----------------------------------------------------------------------------

root_dir = 'F:\\CTimage\\DataProcessing\\test\\nrrdfile'
allfile = gather_files(root_dir, keep_suffixs=['nrrd'])
baseDir = os.path.normpath('F:\\CTimage\\DataProcessing\\test\\niifile')
files = glob(baseDir+'/*.nrrd')

i = 1

for file in allfile:
#load nrrd 
    print('converting  %sth file'%i)
    i += 1 
    print(file)
    _nrrd = nrrd.read(file)
    data = _nrrd[0]
    header = _nrrd[1]

#save nifti
    img = nib.Nifti1Image(data, np.eye(4))

    # print(i,'th ' ,os.path.join(baseDir.replace('nrrdfile','niifile/'), file[-13:-9]+'.nii'))
    nib.save(img,os.path.join(baseDir.replace('nrrdfile','niifile/'), file[-13:-9]+'.nii'))

print("total %s file"%(i-1))