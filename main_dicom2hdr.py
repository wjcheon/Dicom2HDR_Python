# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:23:59 2017

@author: Wonjoong Jason Cheon
@Version 1.0 
"""
%reset
#%%
# >> pip install pydicom 
import dicom
import os
import numpy
from matplotlib import pyplot, cm 
from matplotlib import pyplot as plt


#%% File lodes
os.chdir('D:\MEGA\Python\DICOM_PROJECT')
#PathDicom = "./TESTDICOMS/"
PathDicom = "./Realskull_convert/"
lstFilesDCM = []  # create an empty list
num_files = 0
for dirName, subdirList, fileList in os.walk(PathDicom):
    for filename in fileList:
        if ".dcm" in filename.lower():  # check whether the file's DICOM
            lstFilesDCM.append(os.path.join(dirName,filename))
            num_files += 1
print("{} of dicom image were loaded".format(num_files))
            
            
#%% GET Information 
# Get ref file
RefDs = dicom.read_file(lstFilesDCM[0])
#dir(RefDs)
# Load dimensions based on the number of rows, columns, and slices (along the Z axis)
ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

# Load spacing values (in mm)
ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), float(RefDs.SliceThickness))
#%%

x = numpy.arange(0.0, (ConstPixelDims[0]+1)*ConstPixelSpacing[0], ConstPixelSpacing[0])
y = numpy.arange(0.0, (ConstPixelDims[1]+1)*ConstPixelSpacing[1], ConstPixelSpacing[1])
z = numpy.arange(0.0, (ConstPixelDims[2]+1)*ConstPixelSpacing[2], ConstPixelSpacing[2])
#%%
# The array is sized based on 'ConstPixelDims'
# dtype is int16
ArrayDicom = numpy.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)

# loop through all the DICOM files
for filenameDCM in lstFilesDCM:
    # read the file
    ds = dicom.read_file(filenameDCM)
    # store the raw image data
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array 
    # Print
    if lstFilesDCM.index(filenameDCM) % 100 == 0:
        print ("{}/{} th file was sucessully loaded ".format(lstFilesDCM.index(filenameDCM), len(lstFilesDCM)))
               
#%%
pyplot.figure(dpi=300)
pyplot.axes().set_aspect('equal', 'datalim')
pyplot.set_cmap(pyplot.gray())
pyplot.pcolormesh(x, y, numpy.flipud(ArrayDicom[:, :, 1]))

#%%
Dicom_selected = ArrayDicom[1:671,1:671,255]
plt.figure()
plt.imshow(Dicom_selected)

#%%


#%%
# >> pip install nibabel
# A nibabel image object is the association of three things:
# an N-D array containing the image data;
# a (4, 4) affine matrix mapping array coordinates to coordinates in some RAS+ world coordinate space (Coordinate systems and affines);
# image metadata in the form of a header.

import nibabel as nib
import numpy as np
translation_affine = np.array([[1, 0, 0, 0], 
                               [0, 1, 0, 0],
                               [0, 0, 1, 0],
                               [0, 0, 0, 1]])

#translation_affine = np.diag([1, 1, 1, 1])
    #%%

img_dicom = nib.Nifti1Image(ArrayDicom.astype(np.int16), affine)
header_dicom = img_dicom.header
print(header_dicom)
# Should be change some variable in header_dicom 
# such as, pixdim, scl_slofe, scl_inter
header_dicom['pixdim'] = [1., ConstPixelSpacing[0], ConstPixelSpacing[1], ConstPixelSpacing[2]
, 1., 1., 1., 1.]
header_dicom['scl_slope'] = RefDs.RescaleSlope
header_dicom['scl_inter'] = RefDs.RescaleIntercept
print(header_dicom)

#img_dicom_data_shape = header_dicom.get_data_shape();
#img_dicom_data_type = header_dicom.get_data_dtype();
#img_dicom_data_szVoxel = header_dicom.get_zooms();    
nib.nifti1.save(img_dicom, os.getcwd()+'{}'.format(r'\test2.img'))


#%%





















































