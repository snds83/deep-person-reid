from __future__ import division, print_function, absolute_import
import glob
import os.path as osp
import os
from torchreid.utils import read_json

from ..dataset import VideoDataset


class Saly2022(VideoDataset):

    dataset_dir = 'saly2022'
    dataset_url = None

    def __init__(self, root='', split_id=0, **kwargs):
        self.root = osp.abspath(osp.expanduser(root))
        self.dataset_dir = osp.join(self.root, self.dataset_dir)
        self.download_dataset(self.dataset_dir, self.dataset_url)

        self.split_path = osp.join(self.dataset_dir, 'splits_saly.json')
        self.cam_a_dir = osp.join(
            self.dataset_dir, 'saly2022', 'cam_a'
        )
        self.cam_b_dir = osp.join(
            self.dataset_dir, 'saly2022', 'cam_b'
        )

        required_files = [self.dataset_dir, self.cam_a_dir, self.cam_b_dir]
        self.check_before_run(required_files)

        splits = read_json(self.split_path)
        if split_id >= len(splits):
            raise ValueError(
                'split_id exceeds range, received {}, but expected between 0 and {}'
                    .format(split_id,
                            len(splits) - 1)
            )
        split = splits[split_id]
        #train_dirs, test_dirs = split['train'], split['test']

        train_dirs = os.listdir(self.cam_b_dir)
        test_dirs = os.listdir(self.cam_b_dir)

        print("TRAIN DIR: ",  train_dirs)
        train = self.process_dir(train_dirs, cam1=True, cam2=True)
        query = self.process_dir(test_dirs, cam1=True, cam2=False)
        gallery = self.process_dir(test_dirs, cam1=False, cam2=True)

        super(Saly2022, self).__init__(train, query, gallery, **kwargs)

    def process_dir(self, dirnames, cam1=True, cam2=True):
        tracklets = []
        dirname2pid = {dirname: i for i, dirname in enumerate(dirnames)}

        for dirname in dirnames:
            if cam1:
                print("=====================verify=======================")
                print(dirname)
                print(self.cam_a_dir)
                person_dir = osp.join(self.cam_a_dir, str(dirname))
                print(person_dir)
                img_names = glob.glob(osp.join(person_dir, '*.jpg'))
                assert len(img_names) > 0
                img_names = tuple(img_names)
                pid = dirname2pid[dirname]
                tracklets.append((img_names, pid, 0))

            if cam2:
                person_dir = osp.join(self.cam_b_dir, str(dirname))
                img_names = glob.glob(osp.join(person_dir, '*.jpg'))
                assert len(img_names) > 0
                img_names = tuple(img_names)
                pid = dirname2pid[dirname]
                tracklets.append((img_names, pid, 1))

        return tracklets