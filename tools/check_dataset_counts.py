import argparse
import os
from glob import glob

import numpy as np


def count_images(case_path: str):
    image_dir = None
    for candidate in ("image", "images"):
        candidate_dir = os.path.join(case_path, candidate)
        if os.path.isdir(candidate_dir):
            image_dir = candidate_dir
            break
    if image_dir is None:
        image_dir = os.path.join(case_path, "image")
    images = (
        glob(os.path.join(image_dir, "*.png"))
        + glob(os.path.join(image_dir, "*.jpg"))
        + glob(os.path.join(image_dir, "*.jpeg"))
    )
    images = sorted(images)
    return image_dir, len(images), images[:3], images[-3:]


def count_cameras(case_path: str, camera_file: str):
    cam_path = os.path.join(case_path, camera_file)
    cam = np.load(cam_path)
    world_idx = sorted(
        [int(k.split("_")[-1]) for k in cam.files if k.startswith("world_mat_") and not k.startswith("world_mat_inv_")]
    )
    scale_idx = sorted(
        [int(k.split("_")[-1]) for k in cam.files if k.startswith("scale_mat_") and not k.startswith("scale_mat_inv_")]
    )
    return cam_path, len(world_idx), len(scale_idx), (world_idx[:3], world_idx[-3:])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case_path", type=str)
    parser.add_argument("--camera-file", default="cameras_sphere.npz")
    args = parser.parse_args()

    image_dir, image_count, img_head, img_tail = count_images(args.case_path)
    cam_path, world_count, scale_count, (w_head, w_tail) = count_cameras(args.case_path, args.camera_file)

    print(f"[images] dir={image_dir}")
    print(f"[images] count={image_count}")
    print(f"[images] head={img_head}")
    print(f"[images] tail={img_tail}")
    print(f"[cameras] file={cam_path}")
    print(f"[cameras] world_mat_* count={world_count}")
    print(f"[cameras] scale_mat_* count={scale_count}")
    print(f"[cameras] world_mat_* head={w_head}")
    print(f"[cameras] world_mat_* tail={w_tail}")


if __name__ == "__main__":
    main()
