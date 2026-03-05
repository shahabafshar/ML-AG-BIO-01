# ME 592: Data Analytics and Machine Learning for Cyber-Physical Systems
## Homework 2 - Ag/Bio Applications

**Homework Assigned on:** February 28, 2026  
**Homework Due on:** March 12, 2026  
**One submission per group**

## Common duties (apply to all groups)

### Motivation

This homework is to provide an experience of Data Preparation involved in Data Analytics for Cyber-Physical Systems.

### General Instructions

The dataset and problems for each group are slightly different, but the motivation remains the same. Following are some instructions for all the theme groups. Specific instructions for each group shall be provided in the relevant sections.

1. The final code must be pushed to git before the deadline.
2. Use the discussion board in Canvas in case of any issue.

If you are using Gen AI tools for coding, indicate which tools you have used, your prompts, and how you validated the AI-generated content.

### Expected Outcome

1. A code pushed in git to preprocess each dataset provided.
2. A presentation video explaining your solution approach and results (video duration should be 10 minutes or less). Submit the video (preferably link to video) and github repo link through Canvas.

## Ag/Bio Applications and Image/Video Analytics

Video summarization, Keyframe extraction and Low-rank modeling of video

Given a short video, perform preprocessing and use PCA in multiple ways to analyze structure, motion, and importance of frames:

Use the data in "videos for Ag and Image.zip"

Ag/Bio Applications group - use the Soybean Timelapse video

### 1. Low-Rank Video Modeling (PCA on Raw Frames)

Convert the video into a matrix $X \in \mathbb{R}^{T \times (HWC)}$ by flattening each frame into a vector and stacking them across time. Perform Principal Component Analysis (PCA) across the temporal dimension and plot the cumulative explained variance ratio. Determine the number of principal components required to explain 80%, 90%, and 95% of the total variance. Reconstruct the video using 1 component, 5 components, and 20 components, and visually compare the reconstructed frames to the original frames. Comment on what the first principal component appears to represent, how motion and background information are encoded across different components, and what types of visual information are progressively lost as fewer components are retained.

### 2. Keyframe Extraction via Reconstruction Error

Perform PCA while retaining a fixed number of components (for example, 10). Reconstruct each frame from this reduced representation and compute the per-frame reconstruction error using the $\ell_2$ norm between the original frame $F_i$ and its reconstruction $\hat{F}_i$. Rank frames according to reconstruction error and extract the top 10 frames with the highest error values. Plot reconstruction error as a function of time and visualize the selected keyframes. Comment on whether high-error frames correspond to motion-heavy or event-rich moments, whether static frames yield lower errors, and whether peaks in the error curve align with meaningful play transitions.

### 3. Keyframe Extraction via PCA Projection Magnitude

Project each frame into the PCA subspace and compute the $\ell_2$ norm of its coordinate vector in principal component space. Rank frames according to this projection magnitude and extract the top-k frames that lie farthest from the origin. Plot the temporal trajectory of the first two principal component coordinates to visualize how the video evolves in PCA space over time. Comment on whether frames with large projection magnitude correspond to scene shifts or distinctive formations, how this method differs from reconstruction-error-based selection, and whether certain components appear to capture structured motion patterns.

### 4. PCA on Frame Differences (Motion Modeling)

Compute temporal frame differences using $D_t = F_t - F_{t-1}$ in order to isolate motion information. Flatten the difference frames and apply PCA to this motion-focused representation. Plot the explained variance ratio and visualize the dominant principal components as motion patterns. Identify frames associated with large projections in this difference-based PCA space and extract frames corresponding to high motion energy. Comment on whether background content is suppressed in this formulation, whether moving players become more distinguishable, and how this motion-based PCA compares to applying PCA directly on raw frames.

### 5. Low-Rank and Sparse Decomposition (Robust PCA Perspective)

Model the video as a combination of a low-rank component representing the static background and a sparse component capturing dynamic foreground motion. Perform a robust PCA decomposition or approximate it by subtracting the low-rank reconstruction from the original frames to obtain residual motion maps. Visualize both the low-rank and sparse components and identify frames where the sparse magnitude is largest. Comment on whether dynamic objects are effectively isolated in the sparse component, whether subtle motion is captured, and how this decomposition compares with classical PCA-based reconstruction error in isolating meaningful events.

## Attachments

The datasets below can be found at https://iastate.box.com/s/5t667my9187fesvrvs70450xlr0s1rzt

1. videos for Ag and Image.zip
