import os
import pandas as pd
import shutil


# rename landmark files
def rename_landmark_files():
  path_file = '/home/qinliu/projects/CT_Dental/data_debug/path.csv'
  df = pd.read_csv(path_file)
  
  output_landmark_folder = '/home/qinliu/projects/CT_Dental/landmark'
  for idx in range(len(df)):
    series = df.loc[idx]
    src, dest = series['source'], series['destination']

    print(src, dest)

    folder = os.path.basename(os.path.dirname(src))
    src_image_name = os.path.basename(src)
    dest_image_name = os.path.basename(dest)
    if folder == 'CBCT-57' or folder == 'CT' or folder == 'CT-30':
      # print(src, dest)
      if folder == 'CBCT-57':
        landmark_folder = '/tmp/data/CT_Dental/CBCT_CT-for-CMF-Landmarks-Localization/Patient-CBCT-Data-All'
        landmark_idx = src_image_name[8:10]
        landmark_file = os.path.join(landmark_folder, 'patient_{}_landmarks_bone.txt'.format(landmark_idx))

      elif folder == 'CT':
        landmark_folder = '/tmp/data/CT_Dental/CBCT_CT-for-CMF-Landmarks-Localization/Patient-CBCT-Data-All/CT'
        landmark_idx = src_image_name[8:11]
        if landmark_idx[-1] == '_':
          landmark_idx = landmark_idx[:-1]
        landmark_file = os.path.join(landmark_folder, 'patient_{}_landmarks_bone.txt'.format(landmark_idx))

      else:
        landmark_folder = '/tmp/data/CT_Dental/CBCT_CT-for-CMF-Landmarks-Localization/Normal-CT-Data-Xiao-6_20'
        landmark_idx = src_image_name[10:12]
        landmark_file = os.path.join(landmark_folder, 'normal_CT_{}_landmarks_bone.txt'.format(landmark_idx))

      assert os.path.isfile(landmark_file), landmark_file

      output_landmark_file_temp = os.path.join(output_landmark_folder, '{}_temp.csv'.format(dest_image_name))
      shutil.copy(landmark_file, output_landmark_file_temp)
      
      # re-organize the format of csv file
      if dest_image_name in ['case_166_ct_normal', 'case_167_ct_normal', 'case_168_ct_normal', 'case_169_ct_normal',
                             'case_170_ct_normal', 'case_171_ct_normal', 'case_172_ct_normal', 'case_173_ct_normal',
                             'case_174_ct_normal', 'case_175_ct_normal', 'case_176_ct_normal', 'case_177_ct_normal',
                             'case_178_ct_normal', 'case_179_ct_normal', 'case_180_ct_normal']:
        sep = '\t'
      else:
        sep = ' '
      landmark_df = pd.read_csv(output_landmark_file_temp, header=None, skiprows=[0], sep=sep)
      landmark_df = landmark_df[[0, 1, 2]]
      landmark_df.columns = ['x', 'y', 'z']
      output_landmark_file = os.path.join(output_landmark_folder, '{}.csv'.format(dest_image_name))
      landmark_df.to_csv(output_landmark_file, index=False)
      os.remove(output_landmark_file_temp)


def add_landmark_name():
  landmark_file_folder = '/mnt/projects/CT_Dental/landmark'
  landmark_name_file = '/mnt/projects/CT_Dental/landmark/landmark_name.csv'

  landmark_name_df = pd.read_csv(landmark_name_file)
  landmark_name_dict = {}
  for idx, row in landmark_name_df.iterrows():
    landmark_name_dict[row['landmark_idx']] = row['landmark_name']

  landmark_file_output_folder = '/mnt/projects/CT_Dental/landmark_debug'
  if not os.path.isdir(landmark_file_output_folder):
    os.makedirs(landmark_file_output_folder)

  landmark_files = os.listdir(landmark_file_folder)
  for landmark_file in landmark_files:
    if landmark_file.startswith('case'):
      content = []
      df = pd.read_csv(os.path.join(landmark_file_folder, landmark_file))
      for idx, row in df.iterrows():
        content.append([landmark_name_dict[idx + 1], row['x'], row['y'], row['z']])
      df_out = pd.DataFrame(data=content, columns=['name', 'x', 'y', 'z'])
      df_out.to_csv(os.path.join(landmark_file_output_folder, landmark_file), index=False)


if __name__ == '__main__':
  
  steps = [2]
  
  if 1 in steps:
    rename_landmark_files()

  if 2 in steps:
    add_landmark_name()