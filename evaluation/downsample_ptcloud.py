'''For downsampling point clouds

'''

import numpy as np
import argparse

import sys
import os
import datetime

from plyfile import PlyData, PlyElement
from utils import get_ply

sys.path.append("..")
from shapenet import get_split

DATA_PATH = "../data/shape_net_core_uniform_samples_2048"
TARGET_PATH = "ply"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = "Split file"
    parser.add_argument("-s", "--split_file", default='data/chair_exp.json', help=help_)
    help_ = "Downsample by this factor"
    parser.add_argument("-d", "--downsample", default=2, type=int, help=help_)
    args = parser.parse_args()

    TARGET_PATH = os.path.join(TARGET_PATH, str(args.downsample))
    os.makedirs(TARGET_PATH, exist_ok=True) 
    split_file = args.split_file
    js = get_ply(split_file)
    for key in js.keys():
        target_path = os.path.join(TARGET_PATH, key)
        os.makedirs(target_path, exist_ok=True) 
        data = js[key]
        test = data['test']
        for tag in test:
            source_path = os.path.join(DATA_PATH, key)
            source_ply = os.path.join(source_path, tag + ".ply")
            ply_data = PlyData.read(source_ply)
            points = ply_data['vertex']
            pc = np.vstack([points['x'], points['y'], points['z']]).T
            pc = [pc]
            if len(pc) == 1:  # Unwrap the list
                pc = pc[0]

            target_ply = os.path.join(target_path, tag + ".ply")
            # pc = load_ply(source_ply)
            pc = pc[0::args.downsample,:]
            # pc = np.repeat(pc, args.downsample, axis=0)
            points = []
            for p in pc:
                points.append(tuple(p))
            vertex = np.array(points, dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
            el = PlyElement.describe(vertex, 'vertex')
            PlyData([el]).write(target_ply)
            print(target_ply)




