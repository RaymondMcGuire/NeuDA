import argparse
import os
from glob import glob

import colmap_read_model as read_model


def find_image_dir(case_path):
    for candidate in ("image", "images"):
        candidate_dir = os.path.join(case_path, candidate)
        if os.path.isdir(candidate_dir):
            return candidate_dir
    return None


def find_images_bin(case_path, sparse_dir):
    if sparse_dir:
        candidate = os.path.join(sparse_dir, "images.bin")
        if os.path.isfile(candidate):
            return candidate
    for candidate_dir in (os.path.join(case_path, "sparse", "0"), os.path.join(case_path, "sparse")):
        candidate = os.path.join(candidate_dir, "images.bin")
        if os.path.isfile(candidate):
            return candidate
    return None


def collect_images(image_dir, exts):
    files = []
    for ext in exts:
        files.extend(glob(os.path.join(image_dir, f"*.{ext}")))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case_path", help="Dataset root path")
    parser.add_argument("--image-dir", default="", help="Override images directory")
    parser.add_argument("--sparse-dir", default="", help="Override sparse directory (containing images.bin)")
    parser.add_argument("--exts", default="png,jpg,jpeg", help="Comma-separated extensions")
    parser.add_argument("--out", default="", help="Write unregistered list to file")
    parser.add_argument("--delete", action="store_true", help="Delete unregistered images from disk")
    parser.add_argument("--delete-masks", action="store_true", help="Delete matching masks in mask folder")
    parser.add_argument("--mask-dir", default="", help="Override mask directory")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without deleting")
    args = parser.parse_args()

    image_dir = args.image_dir or find_image_dir(args.case_path)
    if not image_dir:
        raise SystemExit("Could not find image/images directory; use --image-dir.")

    images_bin = find_images_bin(args.case_path, args.sparse_dir)
    if not images_bin:
        raise SystemExit("Could not find images.bin; use --sparse-dir.")

    exts = [e.strip().lstrip(".") for e in args.exts.split(",") if e.strip()]
    images = collect_images(image_dir, exts)
    image_names = [os.path.basename(p) for p in images]

    imdata = read_model.read_images_binary(images_bin)
    registered = {imdata[k].name for k in imdata}

    unregistered = [name for name in image_names if name not in registered]

    print(f"[images] dir={image_dir}")
    print(f"[images] total={len(image_names)}")
    print(f"[colmap] images.bin={images_bin}")
    print(f"[colmap] registered={len(registered)}")
    print(f"[unregistered] count={len(unregistered)}")

    if len(unregistered) > 0:
        print("[unregistered] head:", unregistered[:10])

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            for name in unregistered:
                f.write(name + "\n")
        print(f"[unregistered] written={args.out}")

    if args.delete and len(unregistered) > 0:
        mask_dir = args.mask_dir or os.path.join(args.case_path, "mask")
        for name in unregistered:
            img_path = os.path.join(image_dir, name)
            if args.dry_run:
                print(f"[delete] image: {img_path}")
            else:
                try:
                    os.remove(img_path)
                except OSError as exc:
                    print(f"[delete] failed: {name} ({exc})")
            if args.delete_masks:
                stem, _ = os.path.splitext(name)
                mask_candidates = [
                    os.path.join(mask_dir, f"{stem}.png"),
                    os.path.join(mask_dir, f"{stem}.jpg"),
                    os.path.join(mask_dir, f"{stem}.jpeg"),
                ]
                if args.dry_run:
                    for mask_path in mask_candidates:
                        if os.path.exists(mask_path):
                            print(f"[delete] mask: {mask_path}")
                else:
                    for mask_path in mask_candidates:
                        if os.path.exists(mask_path):
                            try:
                                os.remove(mask_path)
                            except OSError as exc:
                                print(f"[delete] mask failed: {mask_path} ({exc})")
        if not args.dry_run:
            print(f"[delete] removed={len(unregistered)}")


if __name__ == "__main__":
    main()
