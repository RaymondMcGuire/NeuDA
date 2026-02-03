import argparse
import os
import shutil
from glob import glob


def collect_images(image_dir, exts):
    files = []
    for ext in exts:
        files.extend(glob(os.path.join(image_dir, f"*.{ext}")))
    return sorted(files)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", help="Path to images/ folder")
    parser.add_argument("--prefix", default="",
                        help="Optional filename prefix")
    parser.add_argument("--digits", type=int, default=4,
                        help="Zero-padding digits (0 = auto)")
    parser.add_argument("--exts", default="png,jpg,jpeg",
                        help="Comma-separated extensions")
    parser.add_argument("--out-dir", default="",
                        help="If set, copy renamed files into this dir")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    exts = [e.strip().lstrip(".") for e in args.exts.split(",") if e.strip()]
    files = collect_images(args.image_dir, exts)
    if len(files) == 0:
        raise SystemExit(
            f"No images found in {args.image_dir} with exts {exts}")

    digits = args.digits or len(str(len(files)))
    out_dir = args.out_dir or args.image_dir
    os.makedirs(out_dir, exist_ok=True)

    # Rename through a temporary mapping to avoid collisions.
    tmp_names = []
    for idx, src in enumerate(files, start=1):
        ext = os.path.splitext(src)[1].lower()
        tmp = os.path.join(out_dir, f".tmp_rename_{idx:0{digits}d}{ext}")
        tmp_names.append((src, tmp))

    final_names = []
    for idx, (src, _) in enumerate(tmp_names, start=1):
        ext = os.path.splitext(src)[1].lower()
        final = os.path.join(out_dir, f"{args.prefix}{idx:0{digits}d}{ext}")
        final_names.append(final)

    if args.dry_run:
        for (src, tmp), final in zip(tmp_names[:5], final_names[:5]):
            print(f"{src} -> {final}")
        if len(files) > 5:
            print(f"... ({len(files)} files total)")
        return

    if out_dir == args.image_dir:
        # Two-step rename inside the same folder to avoid name collisions.
        for src, tmp in tmp_names:
            os.rename(src, tmp)
        for tmp, final in zip([t for _, t in tmp_names], final_names):
            os.rename(tmp, final)
    else:
        for src, final in zip(files, final_names):
            shutil.copy2(src, final)

    print(f"Renamed {len(files)} images in {out_dir}")


if __name__ == "__main__":
    main()
