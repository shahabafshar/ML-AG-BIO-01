## split prepe code
import os
import pandas as pd
from sklearn.model_selection import train_test_split

# ============================================================
# USER SETTINGS
# ============================================================
data_dir = r"Z:\ME5920 Assignments\Sheep_Classes_All_Compressed"
video_extensions = {".mp4",}

# Keep the 5 behavior classes, drop extra activities
label_map = {
    "Standing": "standing",
    "Sitting": "sitting",
    "Running": "running",
    "Grazing": "grazing",
    "Walking": "walking"
}

random_state = 42

# ============================================================
# READ VIDEOS
# ============================================================
records = []

for class_name in os.listdir(data_dir):
    class_path = os.path.join(data_dir, class_name)

    if not os.path.isdir(class_path):
        continue

    if class_name not in label_map:
        continue

    for file_name in os.listdir(class_path):
        file_path = os.path.join(class_path, file_name)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file_name)[1].lower()
            if ext in video_extensions:
                records.append({
                    "filepath": file_path,
                    "filename": file_name,
                    "class_name": class_name
                })

df = pd.DataFrame(records)

# ============================================================
# CLEAN LABELS
# ============================================================
df["class_label"] = df["class_name"].map(label_map)

class_order = sorted(df["class_label"].unique())
class_to_id = {label: i for i, label in enumerate(class_order)}
df["class_id"] = df["class_label"].map(class_to_id)

print("\nTotal videos found:", len(df))
print("\nVideos per class:")
print(df["class_label"].value_counts())
print("\nClass to ID mapping:")
print(class_to_id)

# ============================================================
# 80/20 STRATIFIED SPLIT
# ============================================================
train_df, test_df = train_test_split(
    df,
    test_size=0.20,
    stratify=df["class_label"],
    random_state=random_state
)

train_df = train_df.copy()
test_df = test_df.copy()

train_df["split"] = "train"
test_df["split"] = "test"

all_split_df = pd.concat([train_df, test_df], ignore_index=True)

# ============================================================
# SAVE
# ============================================================
output_dir = os.path.join(data_dir, "splits_80_20_no_extra")
os.makedirs(output_dir, exist_ok=True)

train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
all_split_df.to_csv(os.path.join(output_dir, "all_videos_with_split.csv"), index=False)

print("\nTrain split counts:")
print(train_df["class_label"].value_counts())

print("\nTest split counts:")
print(test_df["class_label"].value_counts())






## split data
#1-frame extraction code
import os
import cv2
import pandas as pd
import numpy as np
import random

# ============================================================
# USER SETTINGS
# ============================================================
split_dir = r"Z:\ME5920 Assignments\Sheep_Classes_All_Compressed\splits_80_20_no_extra"
train_csv = os.path.join(split_dir, "train.csv")
test_csv = os.path.join(split_dir, "test.csv")

output_root = r"Z:\ME5920 Assignments\Sheep_Frames_1"
image_size = (112, 112)
random_seed = 42

video_extensions = {".mp4", ".avi", ".mov", ".mkv"}

# ============================================================
# REPRODUCIBILITY
# ============================================================
random.seed(random_seed)
np.random.seed(random_seed)

# ============================================================
# FUNCTION TO EXTRACT ONE RANDOM FRAME
# ============================================================
def extract_random_frame(video_path, image_size=(112, 112)):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None, None

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        return None, None

    frame_idx = random.randint(0, total_frames - 1)
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
    success, frame = cap.read()
    cap.release()

    if not success or frame is None:
        return None, None

    frame = cv2.resize(frame, image_size)
    return frame, frame_idx

# ============================================================
# FUNCTION TO PROCESS A SPLIT
# ============================================================
def process_split(csv_path, split_name):
    df = pd.read_csv(csv_path)
    saved_count = 0
    failed_videos = []

    for row in df.itertuples(index=False):
        video_path = row.filepath
        class_label = row.class_label
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        out_dir = os.path.join(output_root, split_name, class_label)
        os.makedirs(out_dir, exist_ok=True)

        frame, frame_idx = extract_random_frame(video_path, image_size=image_size)

        if frame is None:
            failed_videos.append(video_path)
            continue

        out_name = f"{video_name}_frame_idx{frame_idx}.jpg"
        out_path = os.path.join(out_dir, out_name)

        cv2.imwrite(out_path, frame)
        saved_count += 1

    print(f"\n{split_name.upper()} DONE")
    print(f"Saved images: {saved_count}")
    print(f"Failed videos: {len(failed_videos)}")

    if failed_videos:
        print("Example failed files:")
        for f in failed_videos[:5]:
            print(f)

# ============================================================
# RUN
# ============================================================
process_split(train_csv, "train")
process_split(test_csv, "test")

print("\n1-frame dataset extraction complete.")


##4-frame extraction code
import os
import cv2
import pandas as pd
import numpy as np
import random

# ============================================================
# USER SETTINGS
# ============================================================
split_dir = r"Z:\ME5920 Assignments\Sheep_Classes_All_Compressed\splits_80_20_no_extra"
train_csv = os.path.join(split_dir, "train.csv")
test_csv = os.path.join(split_dir, "test.csv")

output_root = r"Z:\ME5920 Assignments\Sheep_Frames_4"
image_size = (112, 112)
random_seed = 42
frames_per_video = 4

# ============================================================
# REPRODUCIBILITY
# ============================================================
random.seed(random_seed)
np.random.seed(random_seed)

# ============================================================
# FUNCTION TO EXTRACT N RANDOM FRAMES
# ============================================================
def extract_n_random_frames(video_path, n_frames=4, image_size=(112, 112)):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return []

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        cap.release()
        return []

    n_to_sample = min(n_frames, total_frames)
    frame_indices = sorted(random.sample(range(total_frames), n_to_sample))

    frames = []
    for frame_idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        success, frame = cap.read()

        if success and frame is not None:
            frame = cv2.resize(frame, image_size)
            frames.append((frame, frame_idx))

    cap.release()
    return frames

# ============================================================
# FUNCTION TO PROCESS A SPLIT
# ============================================================
def process_split(csv_path, split_name):
    df = pd.read_csv(csv_path)
    saved_count = 0
    failed_videos = []

    for row in df.itertuples(index=False):
        video_path = row.filepath
        class_label = row.class_label
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        out_dir = os.path.join(output_root, split_name, class_label)
        os.makedirs(out_dir, exist_ok=True)

        frames = extract_n_random_frames(
            video_path,
            n_frames=frames_per_video,
            image_size=image_size
        )

        if len(frames) == 0:
            failed_videos.append(video_path)
            continue

        for i, (frame, frame_idx) in enumerate(frames, start=1):
            out_name = f"{video_name}_f{i:02d}_idx{frame_idx}.jpg"
            out_path = os.path.join(out_dir, out_name)
            cv2.imwrite(out_path, frame)
            saved_count += 1

    print(f"\n{split_name.upper()} DONE")
    print(f"Saved images: {saved_count}")
    print(f"Failed videos: {len(failed_videos)}")

    if failed_videos:
        print("Example failed files:")
        for f in failed_videos[:5]:
            print(f)

# ============================================================
# RUN
# ============================================================
process_split(train_csv, "train")
process_split(test_csv, "test")

print("\n4-frame dataset extraction complete.")