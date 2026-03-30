##
import os
import subprocess

# ============================================================
#SETTINGS
# ============================================================
input_root = r"Z:\ME5920 Assignments\Sheep_Classes_All"
output_root = r"Z:\ME5920 Assignments\Sheep_Classes_All_Compressed"
ffmpeg_path = r"Z:\ME5920 Assignments\ffmpeg-2026-03-26-git-fd9f1e9c52-essentials_build\bin\ffmpeg.exe"

video_exts = {".mp4", ".avi", ".mov", ".mkv"}

# Long side becomes 480 pixels
scale_filter = "scale='if(gt(iw,ih),480,-2)':'if(gt(iw,ih),-2,480)'"

# ============================================================
# CHECK FFMPEG EXISTS
# ============================================================
if not os.path.exists(ffmpeg_path):
    raise FileNotFoundError(f"ffmpeg.exe not found at: {ffmpeg_path}")

# ============================================================
# CREATE OUTPUT ROOT
# ============================================================
os.makedirs(output_root, exist_ok=True)

# ============================================================
# COMPRESS VIDEOS
# ============================================================
for class_name in os.listdir(input_root):
    in_class_dir = os.path.join(input_root, class_name)
    out_class_dir = os.path.join(output_root, class_name)

    if not os.path.isdir(in_class_dir):
        continue

    os.makedirs(out_class_dir, exist_ok=True)

    for fname in os.listdir(in_class_dir):
        in_path = os.path.join(in_class_dir, fname)

        if not os.path.isfile(in_path):
            continue

        ext = os.path.splitext(fname)[1].lower()
        if ext not in video_exts:
            continue

        base_name = os.path.splitext(fname)[0]
        out_path = os.path.join(out_class_dir, f"{base_name}_compressed.mp4")

        if os.path.exists(out_path):
            print(f"Skipping existing: {out_path}")
            continue

        cmd = [
            ffmpeg_path,
            "-i", in_path,
            "-vf", scale_filter,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "28",
            "-an",
            "-y",
            out_path
        ]

        print(f"Compressing: {in_path}")
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed: {in_path}")
            print(e)

print("Done.")