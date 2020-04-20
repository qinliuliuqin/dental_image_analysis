from easydict import EasyDict as edict
from segmentation3d.utils.normalizer import FixedNormalizer, AdaptiveNormalizer

__C = edict()
cfg = __C

##################################
# general parameters
##################################
__C.general = {}

__C.general.training_image_list_file = '/mnt/projects/CT_Dental/dataset/landmark_detection/train.csv'

__C.general.validation_image_list_file = ''

__C.general.landmark_mask_folder = '/mnt/projects/CT_Dental/landmark_mask_2mm'

__C.general.landmark_files_folder = '/mnt/projects/CT_Dental/landmark'

# landmark label starts from 1, 0 represents the background.
__C.general.target_landmark_label = {
    'S': 1,
    'Gb': 2,
    'Rh': 4,
    'Fz-R': 7,
    'Fz-L': 8,
    'Ba': 21,
    'FMP': 22,
    'Zy-R': 30,
    'Zy-L': 33,
    'U0': 44,
    'Me': 83,
    'L7DBC-R': 135,
    'L7DBC-L': 136
}

# organ label starts from 1, 0 represents the background.
__C.general.target_organ_label = {
    'midface': 1,
    'mandible': 2
}

__C.general.save_dir = '/mnt/projects/CT_Dental/models/model_0419_2020'

__C.general.resume_epoch = -1

__C.general.num_gpus = 0

##################################
# dataset parameters
##################################
__C.dataset = {}

__C.dataset.crop_spacing = [2, 2, 2]      # mm

__C.dataset.crop_size = [48, 48, 48]   # voxel

__C.dataset.sampling_size = [6, 6, 6]      # voxel

__C.dataset.positive_upper_bound = 3    # voxel

__C.dataset.negative_lower_bound = 6    # voxel

__C.dataset.num_pos_patches_per_image = 3

__C.dataset.num_neg_patches_per_image = 9

# crop intensity normalizers (to [-1,1])
# one normalizer corresponds to one input modality
# 1) FixedNormalizer: use fixed mean and standard deviation to normalize intensity
# 2) AdaptiveNormalizer: use minimum and maximum intensity of crop to normalize intensity
__C.dataset.crop_normalizers = [AdaptiveNormalizer()]

# sampling method:
# 1) GLOBAL: sampling crops randomly in the entire image domain
# 2) MASK: sampling crops randomly within segmentation mask
# 3) HYBRID: Sampling crops randomly with both GLOBAL and MASK methods
# 4) CENTER: sampling crops in the image center
__C.dataset.sampling_method = 'CENTER'

# linear interpolation method:
# 1) NN: nearest neighbor interpolation
# 2) LINEAR: linear interpolation
__C.dataset.interpolation = 'LINEAR'

##################################
# data augmentation parameters
##################################
__C.augmentation = {}

__C.augmentation.turn_on = False

__C.augmentation.orientation_axis = [0, 0, 0]  # [x,y,z], axis = [0,0,0] will set it as random axis.

__C.augmentation.orientation_radian = [-30, 30]  # range of rotation in degree, 1 degree = 0.0175 radian

__C.augmentation.translation = [10, 10, 10]  # mm

##################################
# loss function
##################################
__C.landmark_loss = {}

__C.landmark_loss.name = 'Focal'          # 'Dice', or 'Focal'

__C.landmark_loss.focal_obj_alpha = [0.75] * 14  # class balancing weight for focal loss

__C.landmark_loss.focal_gamma = 2         # gamma in pow(1-p,gamma) for focal loss

##################################
# net
##################################
__C.net = {}

__C.net.name = 'vdnet'

##################################
# training parameters
##################################
__C.train = {}

__C.train.epochs = 101

__C.train.batch_size = 1

__C.train.num_threads = 1

__C.train.lr = 1e-4

__C.train.betas = (0.9, 0.999)

__C.train.save_epochs = 10

##################################
# debug parameters
##################################
__C.debug = {}

# random seed used in training
__C.debug.seed = 0

# whether to save input crops
__C.debug.save_inputs = True