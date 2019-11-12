# This script aims to generate datasets for segmentation.

import numpy as np
import os

import md.image3d.python.image3d_io as cio
import md.image3d.python.image3d_tools as ctools


def rename_files_for_dataset1():
  data_path = '/shenlab/lab_stor4/work1/deqiang/CBCT_CT-for-CMF-Segmentation/CBCT-16'
  out_folder = '/shenlab/lab_stor6/qinliu/CT_Dental/data'
  
  files = os.listdir(data_path)
  files.sort()
  idx = 0
  for _, file in enumerate(files):
    if file.endswith('origin.nii.gz'):
      idx += 1
      image = cio.read_image(os.path.join(data_path, file))
      
      mask_label1_path = file.replace('origin', 'midface')
      mask_label1 = cio.read_image(os.path.join(data_path, mask_label1_path))
      
      mask_label2_path = file.replace('origin', 'mandible')
      mask_label2 = cio.read_image(os.path.join(data_path, mask_label2_path))
      
      assert np.linalg.norm(image.size() - mask_label1.size()) == 0
      assert np.linalg.norm(image.size() - mask_label2.size()) == 0
      assert np.linalg.norm(image.spacing() - mask_label1.spacing()) < 1e-3
      assert np.linalg.norm(image.spacing() - mask_label2.spacing()) < 1e-3
      
      print(image.size(), image.spacing(), image.size() * image.spacing())
      print(image.frame().axes())
      
      # merge label 1 and label2 as a single mask
      mask = ctools.create_image3d_like(image)
      mask.fill(0)
      
      mask_npy = mask.to_numpy()
      mask_label1_npy = mask_label1.to_numpy()
      mask_label2_npy = mask_label2.to_numpy()
      
      num_voxel_label1 = np.sum(mask_label1_npy)
      num_voxel_label2 = np.sum(mask_label2_npy)
      print('# label1: ', num_voxel_label1)
      print('# label2: ', num_voxel_label2)
      
      mask_npy[mask_label1_npy > 0] = 1
      mask_npy[mask_label2_npy > 0] = 2
      mask.from_numpy(mask_npy)
      
      # rename
      image_type = 'cbct'
      patient_type = 'patient'
      if file.find('02') > 0 or file.find('03') > 0 or file.find('13') > 0 or \
        file.find('14') > 0:
        patient_type = 'normal'
        
      file_name = 'case_{}_{}_{}'.format(idx, image_type, patient_type)
      image_save_folder = os.path.join(out_folder, file_name)
      if not os.path.isdir(image_save_folder):
        os.makedirs(image_save_folder)
        
      cio.write_image(image, os.path.join(image_save_folder, 'org.mha'),
                      dtype=np.float32, compression=True)
      cio.write_image(mask, os.path.join(image_save_folder, 'seg.mha'),
                      dtype=np.int8, compression=True)
      
  assert idx == 16
  
  
def rename_files_for_dataset2():
  data_path = '/shenlab/lab_stor4/work1/deqiang/CBCT_CT-for-CMF-Segmentation/CBCT-57'
  out_folder = '/shenlab/lab_stor6/qinliu/CT_Dental/data'

  files = os.listdir(data_path)
  files.sort()
  idx = 16
  for _, file in enumerate(files):
    if file.endswith('origin.nii.gz'):
      idx += 1
      print(idx, file)
      image = cio.read_image(os.path.join(data_path, file))

      mask_label1_path = file.replace('origin', 'midface')
      if os.path.isfile(os.path.join(data_path, mask_label1_path)):
        mask_label1 = cio.read_image(os.path.join(data_path, mask_label1_path))
      else:
        mask_label1 = None

      mask_label2_path = file.replace('origin', 'mandible')
      if os.path.isfile(os.path.join(data_path, mask_label2_path)):
        mask_label2 = cio.read_image(os.path.join(data_path, mask_label2_path))
      else:
        mask_label2 = None

      if mask_label1 is not None and mask_label2 is not None:
        assert np.linalg.norm(image.size() - mask_label1.size()) == 0
        assert np.linalg.norm(image.size() - mask_label2.size()) == 0
        assert np.linalg.norm(image.spacing() - mask_label1.spacing()) < 1e-3
        assert np.linalg.norm(image.spacing() - mask_label2.spacing()) < 1e-3

      print(image.size(), image.spacing(), image.size() * image.spacing())
      print(image.frame().axes())

      # merge label 1 and label2 as a single mask
      mask = ctools.create_image3d_like(image)
      mask.fill(0)

      mask_npy = mask.to_numpy()

      if mask_label1 is not None:
        mask_label1_npy = mask_label1.to_numpy()
        num_voxel_label1 = np.sum(mask_label1_npy)
        print('# label1: ', num_voxel_label1)

      if mask_label2 is not None:
        mask_label2_npy = mask_label2.to_numpy()
        num_voxel_label2 = np.sum(mask_label2_npy)
        print('# label2: ', num_voxel_label2)

      if mask_label1 is not None:
        mask_npy[mask_label1_npy > 0] = 1

      if mask_label2 is not None:
        mask_npy[mask_label2_npy > 0] = 2
      mask.from_numpy(mask_npy)
    
      # rename
      image_type = 'cbct'
      patient_type = 'patient'

      file_name = 'case_{}_{}_{}'.format(idx, image_type, patient_type)
      image_save_folder = os.path.join(out_folder, file_name)
      if not os.path.isdir(image_save_folder):
        os.makedirs(image_save_folder)

      cio.write_image(image, os.path.join(image_save_folder, 'org.mha'),
                      dtype=np.float32, compression=True)
      cio.write_image(mask, os.path.join(image_save_folder, 'seg.mha'),
                      dtype=np.int8, compression=True)
  assert idx == 90


def rename_files_for_dataset2_fix():
  data_path = '/shenlab/lab_stor4/work1/deqiang/CBCT_CT-for-CMF-Segmentation/CBCT-57'
  out_folder = '/shenlab/lab_stor6/qinliu/CT_Dental/data'
  
  files = os.listdir(data_path)
  files.sort()
  for _, file in enumerate(files):
  
    matched = False
    if file.endswith('origina.nii.gz'):
      idx = 91
      image_type = 'cbct'
      patient_type = 'patient'
      pattern = 'origina'
      matched = True
    
    if file.endswith('orgin.nii.gz'):
      idx = 92
      image_type = 'cbct'
      patient_type = 'patient'
      pattern = 'orgin'
      matched = True

    if matched:
      print(file)
      image = cio.read_image(os.path.join(data_path, file))
      
      mask_label1_path = file.replace(pattern, 'midface')
      if os.path.isfile(os.path.join(data_path, mask_label1_path)):
        mask_label1 = cio.read_image(os.path.join(data_path, mask_label1_path))
      else:
        mask_label1 = None
      
      mask_label2_path = file.replace(pattern, 'mandible')
      if os.path.isfile(os.path.join(data_path, mask_label2_path)):
        mask_label2 = cio.read_image(os.path.join(data_path, mask_label2_path))
      else:
        mask_label2 = None
      
      if mask_label1 is not None and mask_label2 is not None:
        assert np.linalg.norm(image.size() - mask_label1.size()) == 0
        assert np.linalg.norm(image.size() - mask_label2.size()) == 0
        assert np.linalg.norm(image.spacing() - mask_label1.spacing()) < 1e-3
        assert np.linalg.norm(image.spacing() - mask_label2.spacing()) < 1e-3
      
      print(image.size(), image.spacing(), image.size() * image.spacing())
      print(image.frame().axes())
      
      # merge label 1 and label2 as a single mask
      mask = ctools.create_image3d_like(image)
      mask.fill(0)
      
      mask_npy = mask.to_numpy()
      
      if mask_label1 is not None:
        mask_label1_npy = mask_label1.to_numpy()
        num_voxel_label1 = np.sum(mask_label1_npy)
        print('# label1: ', num_voxel_label1)
      
      if mask_label2 is not None:
        mask_label2_npy = mask_label2.to_numpy()
        num_voxel_label2 = np.sum(mask_label2_npy)
        print('# label2: ', num_voxel_label2)
      
      if mask_label1 is not None:
        mask_npy[mask_label1_npy > 0] = 1
      
      if mask_label2 is not None:
        mask_npy[mask_label2_npy > 0] = 2
      mask.from_numpy(mask_npy)
      
      file_name = 'case_{}_{}_{}'.format(idx, image_type, patient_type)
      image_save_folder = os.path.join(out_folder, file_name)
      if not os.path.isdir(image_save_folder):
        os.makedirs(image_save_folder)

      print(file_name)
      cio.write_image(image, os.path.join(image_save_folder, 'org.mha'),
                      dtype=np.float32, compression=True)
      cio.write_image(mask, os.path.join(image_save_folder, 'seg.mha'),
                      dtype=np.int8, compression=True)


def rename_files_for_dataset3():
  data_path = '/shenlab/lab_stor4/work1/deqiang/CBCT_CT-for-CMF-Segmentation/CBCT-57/CT'
  out_folder = '/shenlab/lab_stor6/qinliu/CT_Dental/data'
  
  files = os.listdir(data_path)
  files.sort()
  idx = 92
  for _, file in enumerate(files):
    if file.endswith('origin.nii.gz'):
      idx += 1
      image = cio.read_image(os.path.join(data_path, file))
      
      mask_label1_path = file.replace('origin', 'midface')
      mask_label1 = cio.read_image(os.path.join(data_path, mask_label1_path))
      
      mask_label2_path = file.replace('origin', 'mandible')
      mask_label2 = cio.read_image(os.path.join(data_path, mask_label2_path))
      
      assert np.linalg.norm(image.size() - mask_label1.size()) == 0
      assert np.linalg.norm(image.size() - mask_label2.size()) == 0
      assert np.linalg.norm(image.spacing() - mask_label1.spacing()) < 1e-3
      assert np.linalg.norm(image.spacing() - mask_label2.spacing()) < 1e-3
      
      print(image.size(), image.spacing(), image.size() * image.spacing())
      print(image.frame().axes())
      
      # merge label 1 and label2 as a single mask
      mask = ctools.create_image3d_like(image)
      mask.fill(0)
      
      mask_npy = mask.to_numpy()
      mask_label1_npy = mask_label1.to_numpy()
      mask_label2_npy = mask_label2.to_numpy()
      
      num_voxel_label1 = np.sum(mask_label1_npy)
      num_voxel_label2 = np.sum(mask_label2_npy)
      print('# label1: ', num_voxel_label1)
      print('# label2: ', num_voxel_label2)
      
      mask_npy[mask_label1_npy > 0] = 1
      mask_npy[mask_label2_npy > 0] = 2
      mask.from_numpy(mask_npy)
      
      # rename
      image_type = 'ct'
      patient_type = 'patient'
      
      file_name = 'case_{}_{}_{}'.format(idx, image_type, patient_type)
      image_save_folder = os.path.join(out_folder, file_name)
      if not os.path.isdir(image_save_folder):
        os.makedirs(image_save_folder)
      
      cio.write_image(image, os.path.join(image_save_folder, 'org.mha'),
                      dtype=np.float32, compression=True)
      cio.write_image(mask, os.path.join(image_save_folder, 'seg.mha'),
                      dtype=np.int8, compression=True)

  assert idx == 117


def rename_files_for_dataset4():
  data_path = '/shenlab/lab_stor4/work1/deqiang/CBCT_CT-for-CMF-Segmentation/CT-30'
  out_folder = '/shenlab/lab_stor6/qinliu/CT_Dental/data'
  
  files = os.listdir(data_path)
  files.sort()
  idx = 117
  for _, file in enumerate(files):
    if file.endswith('origin.nii.gz') or file.endswith('original.nii.gz'):
      print(file)
      idx += 1
      image = cio.read_image(os.path.join(data_path, file))
      
      pattern = 'original'
      if file.endswith('origin.nii.gz'):
        pattern = 'origin'

      mask_label1_path = file.replace(pattern, 'midface')
      mask_label1 = cio.read_image(os.path.join(data_path, mask_label1_path))
      
      mask_label2_path = file.replace(pattern, 'mandible')
      mask_label2 = cio.read_image(os.path.join(data_path, mask_label2_path))
      
      assert np.linalg.norm(image.size() - mask_label1.size()) == 0
      assert np.linalg.norm(image.size() - mask_label2.size()) == 0
      assert np.linalg.norm(image.spacing() - mask_label1.spacing()) < 1e-3
      assert np.linalg.norm(image.spacing() - mask_label2.spacing()) < 1e-3
      
      print(image.size(), image.spacing(), image.size() * image.spacing())
      print(image.frame().axes())
      
      # merge label 1 and label2 as a single mask
      mask = ctools.create_image3d_like(image)
      mask.fill(0)
      
      mask_npy = mask.to_numpy()
      mask_label1_npy = mask_label1.to_numpy()
      mask_label2_npy = mask_label2.to_numpy()
      
      num_voxel_label1 = np.sum(mask_label1_npy)
      num_voxel_label2 = np.sum(mask_label2_npy)
      print('# label1: ', num_voxel_label1)
      print('# label2: ', num_voxel_label2)
      
      mask_npy[mask_label1_npy > 0] = 1
      mask_npy[mask_label2_npy > 0] = 2
      mask.from_numpy(mask_npy)
      
      # rename
      image_type = 'ct'
      patient_type = 'normal'
      
      file_name = 'case_{}_{}_{}'.format(idx, image_type, patient_type)
      image_save_folder = os.path.join(out_folder, file_name)
      if not os.path.isdir(image_save_folder):
        os.makedirs(image_save_folder)
      
      cio.write_image(image, os.path.join(image_save_folder, 'org.mha'),
                      dtype=np.float32, compression=True)
      cio.write_image(mask, os.path.join(image_save_folder, 'seg.mha'),
                      dtype=np.int8, compression=True)
  assert idx == 181


if __name__ == "__main__":
  
  datasets = [0]
  
  if 1 in datasets:
    rename_files_for_dataset1()
    
  if 2 in datasets:
    rename_files_for_dataset2()
    rename_files_for_dataset2_fix()
    
  if 3 in datasets:
    rename_files_for_dataset3()
    
  if 4 in datasets:
    rename_files_for_dataset4()