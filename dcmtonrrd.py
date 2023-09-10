import SimpleITK as sitk
import numpy as np
import os
import matplotlib.pyplot as plt



def gather_files(
        root_dir='F:\CTimage\LIDC-IDRI\manifest-1600709154662\LIDC-IDRI\\LIDC-IDRI-0001\\01-01-2000-NA-NA-30178\\3000566.000000-NA-03192',
        keep_suffixs=['dcm']):
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
                    # folder_path = (r"F:\\CTimage\\LIDC-IDRI\\manifest-1600709154662\\LIDC-IDRI\\LIDC-IDRI-0001\\01-01-2000-NA-NA-30178\\3000566.000000-NA-03192\\1-009.dcm")
                    file = sitk.ReadImage(file_path)

                    # img_array = sitk.GetArrayFromImage(file)
                    # posMax = np.unravel_index(np.argmax(img_array),img_array.shape)
                    # posMin = np.unravel_index(np.argmin(img_array),img_array.shape)
                    # maxHuValue = img_array[posMax[0]][posMax[1]][posMax[2]]
                    # minHuValue = img_array[posMin[0]][posMin[1]][posMin[2]]
                    # print("Maximum : ",maxHuValue,"Minimum : ",minHuValue )

                    # table = PrettyTable(['Minimum', 'Maximum', 'Range','Spacing'])

                    # table.add_row([maxHuValue, minHuValue, maxHuValue - minHuValue ,Spacing])

                    n_files += 1
                    break
    # print(table)
    if len(all_files) > 10:
        filePath = all_files[0]
        parent_path = os.path.abspath(os.path.join(filePath, ".."))
        return parent_path
    else:
        return 'msk'
# 使用listdir()函数获取目录中的所有文件和子目录名称
def recursionLIDC(path):
    i = 1
    dir_list = os.listdir(path)  # dir_list:  ['LIDC-IDRI-0001', 'LIDC-IDRI-0012']
    result_list_path = []
    # 遍历目录中的每一个一级目录
    for name in dir_list:
        print('accessing : ', name)
        #        if os.path.isdir(os.path.join(path, name)):
        name_path = os.path.join(path, name)  # F:\CTimage\test\LIDC-IDRI-0012
        # 判断是否为子目录，如果是，则打印目录名称
        # 返回此路径下的文件名称列表
        name_path_fileFirst = os.listdir(name_path)  # name_path_fileFirst :  ['LIDC-IDRI-0001', 'LIDC-IDRI-0012']
        for file in name_path_fileFirst:
            name_path_second = os.path.join(name_path, file)  # F:\CTimage\test\LIDC-IDRI-0012\01-01-2000-NA-NA-26735
            name_path_fileSecond = os.listdir(name_path_second)  # ['3000975.000000-NA-50170']
            for subfile in name_path_fileSecond:
                resultpath = os.path.join(name_path_second,
                                          subfile)  # F:\CTimage\test\LIDC-IDRI-0012\01-01-2000-NA-NA-26735\3000975.000000-NA-50170
                result = gather_files(resultpath, keep_suffixs=['dcm'])
                if result != 'msk':
                    print(i)
                    i += 1
                    result_list_path.append(result)
    return result_list_path

def recursionLiverpool(path):
    i = 1
    dir_list = os.listdir(path)  # dir_list:  ['LIDC-IDRI-0001', 'LIDC-IDRI-0012']
    result_list_path = []
    # 遍历目录中的每一个一级目录
    for name in dir_list:
        print('accessing : ', name)
        #        if os.path.isdir(os.path.join(path, name)):
        name_path = os.path.join(path, name)  # F:\CTimage\test\LIDC-IDRI-0012
        # 判断是否为子目录，如果是，则打印目录名称
        # 返回此路径下的文件名称列表
        name_path_fileFirst = os.listdir(name_path)  # name_path_fileFirst :  ['LIDC-IDRI-0001', 'LIDC-IDRI-0012']
        result_list_path.append(name_path)
            
    print(result_list_path)
    return result_list_path

def getrange(folder_path):
    file = sitk.ReadImage(folder_path)
    img_array = sitk.GetArrayFromImage(file)
    size = file.GetSize()  # 大小
    Origin = file.GetOrigin()  # 坐标原点
    Spacing = file.GetSpacing()  # 像素间距
    Direction = file.GetDirection()  # 方向
    attributeSlice = []

    posMax = np.unravel_index(np.argmax(img_array), img_array.shape)
    posMin = np.unravel_index(np.argmin(img_array), img_array.shape)
    maxHuValue = img_array[posMax[0]][posMax[1]][posMax[2]]
    minHuValue = img_array[posMin[0]][posMin[1]][posMin[2]]

    attributeSlice.extend((maxHuValue, minHuValue, maxHuValue - minHuValue, size, Origin, Spacing, Direction))

    return attributeSlice
def getvolumnrange(VolumnPath):
    MinimumList, MaximumList, RangeList = [], [], []
    volumnAtrribute = []
    for file in os.listdir(VolumnPath):
        filepath = os.path.join(VolumnPath, file)
        f = os.path.splitext(filepath)
        filename, type = f
        if type != '.dcm':
            continue
        attributeSlice = getrange(filepath)
        MaximumSlice = attributeSlice[0]
        MinimumSlice = attributeSlice[1]
        RangeSlice = attributeSlice[2]
        SizeSlice = attributeSlice[3]
        Origin = attributeSlice[4]
        Spacing = attributeSlice[5]
        Direction = attributeSlice[6]
        MaximumList.append(MaximumSlice)
        MinimumList.append(MinimumSlice)

    rangeOfVolumn = max(MaximumList) - min(MinimumList)
    maximunValue = max(MaximumList)
    minimumValue = min(MinimumList)
    volumnAtrribute.extend((maximunValue, minimumValue))
    return volumnAtrribute
#    print(max(MaximumSlice), min(MinimumList), max(MaximumSlice)- min(MinimumList),SizeSlice)
#resultList = recursion(path="/media/yalin/KINGSTON/CTimage/LIDC-IDRI/manifest-1600709154662/LIDC-IDRI")
#resultList = recursion(path = "F:\CTimage\LIDC-IDRI\manifest-1600709154662\LIDC-IDRI")

def DCMtoNRRD(file_path,sn,nrrdPath):
#    out_path = 'E:\\nrrdfile\\test'
    dcms_name = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(file_path)
    dcms_read = sitk.ImageSeriesReader()
    dcms_read.SetFileNames(dcms_name)
    dcms_series = dcms_read.Execute()
#       
#    out_path = ('/media/yalin/5E87-811D/nrrdfile/raw/'+'%s'%(1400+sn))
    out_path = (nrrdPath+'%s'%(5000+sn))
    # 创建文件夹
    if not os.path.exists(out_path):
        os.makedirs(out_path)    
    sitk.WriteImage(dcms_series,out_path+'/img'+'.nrrd') #保存


#resultList = recursion(path = "F:\\CTimage\\LIDC-IDRI\\manifest-1600709154662\\LIDC-IDRI")


nrrdPath = "F:\\CTimage\\DataProcessing\\test\\nrrdfile\\"
resultList =recursionLiverpool('F:\\CTimage\\DataProcessing\\test\\dicomFile')

for i,path in enumerate(resultList):
    if path != 'msk':
        print(i+1,path)
        DCMtoNRRD(path,i,nrrdPath)


