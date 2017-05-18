# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 12:23:59 2017

@author: Wonjoong Jason Cheon
@Date: 2017.04.06
@Version 1.0 
@
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
#%% Generate coordinates for each axis

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
    # store the raw image data to target 3D matrix (i.e ArrayDicom)
    ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array 
    # Print progressing status
    if lstFilesDCM.index(filenameDCM) % 100 == 0:
        print ("{}/{} th file was sucessully loaded ".format(lstFilesDCM.index(filenameDCM), len(lstFilesDCM)))
#%% image rotate (option)
#test_m = numpy.arange(9).reshape(3,3)
#test_m_rotated = numpy.rot90(test_m,k=-1)
rotate_option = True
if rotate_option:
    ArrayDicom_rotated = ArrayDicom*0
    for iter_rot in range(0,len(lstFilesDCM)-1):
        ArrayDicom_rotated[:,:,iter_rot] = numpy.rot90(ArrayDicom[:,:,iter_rot],k=-1)
        if iter_rot % 100 == 0:
            print ("{}/{} th file was sucessully rotated ".format(iter_rot, len(lstFilesDCM)))
    ArrayDicom = ArrayDicom_rotated
    print ("Rotation process is done !!")               
#%%  Drawing 
Dicom_selected_transverse = ArrayDicom[1:sz_ArrayDicom[0]+1,1:sz_ArrayDicom[1]+1,sz_ArrayDicom[2]/2]
Dicom_selected_coronal = ArrayDicom[sz_ArrayDicom[0]/2,1:sz_ArrayDicom[1]+1,1:sz_ArrayDicom[2]+1]
Dicom_selected_saggital = ArrayDicom[1:sz_ArrayDicom[0]+1,sz_ArrayDicom[1]/2,1:sz_ArrayDicom[2]+1]

num_subplot = 3
def show_slices(slices):
    """ Function to display row of image slices """
    fig, axes = plt.subplots(1, num_subplot)
    for i, slice in enumerate(slices):
        axes[i].imshow(slice.T, cmap="gray", origin="lower")


show_slices([Dicom_selected_transverse, Dicom_selected_coronal, Dicom_selected_saggital])
plt.suptitle("Center slices for Dicom image")  


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

img_dicom = nib.Nifti1Image(ArrayDicom.astype(np.int16), translation_affine)
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





















































