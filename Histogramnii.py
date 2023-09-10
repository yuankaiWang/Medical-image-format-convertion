import numpy as np
import os  # 遍历文件夹
import nibabel as nib  # nii格式一般都会用到这个包
import imageio  # 转换成图像
import matplotlib.pyplot as plt
import matplotlib

center = -500 #肺部的窗宽窗位
width = 1500
 
def histogram(filepath,translation=0,filename = None):
    '''
    translation --> 位移
    
    filenames = os.listdir(filepath)  # 读取nii文件夹
  
 
    for f in filenames:
    # 开始读取nii文件
        img_path = os.path.join(filepath, f)
        print('The path of img is : ', img_path)
    '''

    #filenames = os.listdir(filepath)
    #print('the filenames consist of : ', filenames)
    img = nib.load(filepath)  # 读取nii
    img_fdata = img.get_fdata() # api 已完成转换，读出来的即为CT值
    print('start to initialize : ' ,filename)
    print('the shape of file %s is : '%filename,img_fdata.shape)
    img_fdata = np.array(img_fdata)
    img_fdatashaped = img_fdata.flatten() +translation

    posMax = np.unravel_index(np.argmax(img_fdata),img_fdata.shape)
    posMin = np.unravel_index(np.argmin(img_fdata),img_fdata.shape)
    maxHuValue = img_fdata[posMax[0]][posMax[1]][posMax[2]]
    minHuValue = img_fdata[posMin[0]][posMin[1]][posMin[2]]
    print('the maximum  HU is: ',maxHuValue)
    print('the minimum value of HU is: ',minHuValue)
    print('the range is : (%s,%s)'%(int(minHuValue),int(maxHuValue)))




    b = np.array([0])
    c = np.setdiff1d(img_fdatashaped,b)

    img_fdatashaped = deleteElement(img_fdatashaped,element = minHuValue)
    img_fdatashaped = deleteElement(img_fdatashaped,element = minHuValue +1 )

#    b = img_fdatashaped[~np.all(b == 0, axis=0)]
#    print('b is : %s and b shape is: %s '%(b,b.shape))
#    print('img_fdatashaped shape: ',img_fdatashaped.shape)
#    b += translation
#    print('the shape of data is : ', c.shape)#(51
    

    #-------------------------------

    # 设置matplotlib正常显示中文和负号
    
    #matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文


    # 指定分组个数
    n_bins=int(maxHuValue - minHuValue)
    
    
    


    #img_fdatalist = [img_fdata]

    #print('shape of img_fdatashaped is : ', img_fdatashaped.shape,x_multi_array.shape)
    #print('shape of x_multi_array: ',x_multi_array.shape)

    # 实际绘图代码与单类型直方图差异不大，只是增加了一个图例项
    # 在 ax.hist 函数中先指定图例 label 名称

 #   plt.hist(img_fdatashaped, bins=500, alpha = 0.6, histtype='step',label=list("Liverpool"))
 #   plt.title('Data from Project in format : nii')
 #   plt.xlabel('Range from : (%s to %s) \n maximum : %s \n minimum : %s'%(minHuValue,maxHuValue,maxHuValue,minHuValue))
    # 通过 ax.legend 函数来添加图例
    return img_fdatashaped
    


def histogramLine(mu1 = np.zeros(1000)):

    np.random.seed(19680801)

    Nsteps, Nwalkers = 1000,250
    t = np.arange(Nsteps)

    # an (Nsteps x Nwalkers) array of random walk steps
    S1 = 0.004 + 0.02*np.random.randn(Nsteps, Nwalkers)
    S2 = 0.002 + 0.01*np.random.randn(Nsteps, Nwalkers)
    print('S1 is :', S1.shape)
    # an (Nsteps x Nwalkers) array of random walker positions
    X1 = S1.cumsum(axis=0)
    X2 = S2.cumsum(axis=0)


    # Nsteps length arrays empirical means and standard deviations of both
    # populations over time
    mu1 = X1.mean(axis=1)
    sigma1 = X1.std(axis=1)
    mu2 = X2.mean(axis=1)
    sigma2 = X2.std(axis=1)
    print('X1 is :', X1.shape)
    # plot it!
    fig, ax = plt.subplots(1)

    mu1 = (1,3,4,2,5,8,3,2,4,6,2)
    
    ax.plot(mu1, lw=1, label='mean population 1')
    #ax.plot(t, mu2, lw=2, label='mean population 2')

    #ax.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor='C0', alpha=0.4)
    #ax.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='C1', alpha=0.4)
    #ax.fill_between(t, mu1+7, mu1, facecolor='C0', alpha=0.4)
    #ax.fill_between(t, mu2, mu2, facecolor='C1', alpha=0.4)
    ax.set_title(r'random walkers empirical $\mu$ and $\pm \sigma$ interval')
    ax.legend(loc='upper left')
    ax.set_xlabel('num steps')
    ax.set_ylabel('position')
    ax.grid()
    plt.show()
 
def deleteElement(original_array,element = 0):
#remove elements whose value is equal to 12
    new_array = np.delete(original_array, np.where(original_array == element))
    return new_array

if __name__ == '__main__':
#     filepath = (r'F:\\CTimage\\TE\\test')
    # filepath = (r'/media/yalin/KINGSTON/CTimage/DataProcessing/niifile')

    filepath = (r'/media/yalin/KINGSTON/CTimage/Data/liverpoolCTExample')
    filenames = os.listdir(filepath)
    
    # filenames2 = os.listdir(filepath2)  # 读取nii文件夹
    result = []
    for file in filenames:
    # 开始读取nii文件
        # if file != 'CJ297.nii':
        #     continue
        img_path = os.path.join(filepath, file)
        img_fdatashaped = histogram(img_path,filename = str(file))
        result.append((img_fdatashaped))

plt.title('Convert from original dcm data' )
plt.hist(result, bins=819, alpha = 0.6, histtype='step',label=list("Liverpool"))
plt.show()
#        break

#    filepath = ('F:\CTimage\TE\\test\\CJ297.nii')
 #   filepath1= ('F:\CTimage\TE\\test\\1-003.nii')
#    filepath2 =('F:\CTimage\TE\\test\FP694.nii')
#    histogram(filepath1,translation = -1024)
#    histogram(filepath)
#    histogram(filepath1)
    #plt.show()
    


    #img = nib.load(img_path)  # 读取nii
    #histogramLine()
