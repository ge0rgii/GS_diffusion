# GS_diffusion
This repository is part of the research conducted under the [Implicit Deepfake](https://github.com/quereste/implicit-deepfake) project. The primary goal of that project is to explore techniques for generating and manipulating 3D models using implicit representations. This experiment extends this work by focusing on the transformation of a 3D Blender model into a new 3D model using Gaussian Splatting through Stable Diffusion.

## Reproducing the Results

### Tools

To reproduce the results of this experiment, you will need to install the following tools:
- [**Blender**](https://www.blender.org/)
- [**Gaussian Splatting**](https://github.com/graphdeco-inria/gaussian-splatting)
- [**Stable Diffusion**](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- [**EbSynth**](https://ebsynth.com/)
- [**ffmpeg**](https://ffmpeg.org/)

### Steps to Reproduce the Experiment

1. **Render Images from Blender**  
   Render a series of images from your 3D model in Blender. These images will serve as the input for the diffusion process. We recommend performing 360 degrees video render to ensure consistency while applying diffusion
   [An example open source 3D model](https://sketchfab.com/3d-models/tina-head-530fab5eb2aa44f699052624794aeaa9)

2. **Apply Diffusion using Stable Diffusion**
   Use Stable Diffusion to apply transformations defined by a prompt to the rendered frames.
   The process of applying Stable Diffusion that ensures the highest consistency of the result across among different angles along with optimal parameters is described [here](https://stable-diffusion-art.com/video-to-video/#Method_5_Temporal_Kit) and requires the use of EbSynth

4. **Convert Rendered Images to a 3D Model using Gaussian Splatting**  
   Feed the transformed images into the Gaussian Splatting process to generate the final 3D model.

### Results

After completing the experiment, the following results were observed:

![result_0](https://github.com/user-attachments/assets/c5a3b2c6-1c72-4b2a-83a4-c6f61ff258a1)

Used prompts:
positive - "Photo of a bronze bust of a woman, detailed and lifelike, in the style of Auguste Rodin, polished bronze, classical sculpture aesthetics, 32k uhd, timeless and elegant, intricate details, full head and shoulders, museum quality, realistic texture, warm bronze tones, photorealistic, black background."
negative - "Deformed, disfigured, ugly."

![result_1](https://github.com/user-attachments/assets/b35b4082-7efc-4ad8-975a-29bb8ca5dec7)

Used prompts:
positive - "Photo of a head with realistic facial features, hair color changed to vibrant red, smooth and lifelike skin texture, sharp and expressive eyes, natural human proportions, high-definition detail, consistent appearance from all angles (front, side, back view), cinematic composition, trending on ArtStation."
negative - "Unrealistic colors, distorted proportions, blurred details, heavy shadows, lack of detail."

![result_2](https://github.com/user-attachments/assets/75e50f82-d48d-4c38-8341-dadb27d210f1)

Used prompts:
positive - "An elf, with pointed ears, ethereal and elegant features, detailed and lifelike, in the style of Alan Lee, smooth and flawless skin, sharp and expressive eyes, long and flowing hair, otherworldly and mystical appearance, 32k uhd, high-definition detail, wearing simple yet stylish elven attire, black background, cinematic lighting, photorealistic, studio portrait."
negative - "Distorted, disfigured, ugly, human features, unrealistic proportions, poor lighting, low detail."

### TODO:
Explore improvements by iteratively applying Stable Diffusion (after the first step, it may be better to use [this approach](https://stable-diffusion-art.com/video-to-video/#Method_2_ControlNet_img2img) along with the DDIM Sampler) and Gaussian Splatting on the resulting models. The hypothesis is that Gaussian Splatting increases consistency between adjacent frames, while Stable Diffusion enhances quality.

Results from the first experiment:

![output_combined-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/50c06644-d332-4141-a1ab-c90802ba5e27)

### Scripts to reproduce the results (only Windows)
First you need to install the software mentioned in **Tools** Section (we provide example dataset in the [link](https://ujchmura-my.sharepoint.com/:f:/g/personal/georgii_stanishevskii_student_uj_edu_pl/Ei93fzknaspDp0sxhWXdLrABSdBNXTFAv_dIHjPHHxWFEA?e=flv8KE), in such case you do not need Blender)
Then copy all the scripts listed in this repository into stable Automatic1111 folder, run Stable Diffusion with --api parameter and open the folder in CMD Terminal (Powershell may not work properly). Activate venv located in .\venv\Scripts\activate.bat

**Usage**
python loop.py /path/to/main_folder "My Prompt" --start 0 --end 3 (optional parameters)

Main folder should contain video render of the object and transforms json. There are additional optional parameters (resolution, fps, etc.) which I will add later to the description. Code will generate (end - start) folders named as iter1, iter2, etc. which will contain gaussian splatting model and generated frames. Video results (360 degrees renders) will appear in main_folder named as iter1.mp4, iter2.mp4, ...
In the middle of generating process the program will pause and wait till you use EbSynth program to propagate changes from diffusion to all frames. Unfortunately you need to do it manually.

### TODO:
metrics for 3 faces 10 iterations:

Results from the second experiment:

![ezgif-2-14c20ef111](https://github.com/user-attachments/assets/a6d14863-d3e4-4e19-ad65-e4184b746dd8)

## Theory behind

### Stable Diffusion

#### Latent Diffusion Models

![image](https://github.com/user-attachments/assets/60137b42-23e0-4d10-84f4-4e3e1f42be9e)

**Latent Diffusion Models** were introduced by Rombach *et al.* in  
*“High-Resolution Image Synthesis with Latent Diffusion Models”* (arXiv : 2112.10752, 20 Dec 2021). 
The authors propose to embed the diffusion process inside a pretrained auto-encoder so that all noisy forward / denoising reverse steps run **in a much lower-dimensional latent space** rather than in pixel space. This design slashes memory and compute while preserving visual fidelity, and it underpins Stable Diffusion.

**Pipeline overview**

1. **Encode** – an image \(x\) is compressed by an encoder \(E\) to a latent tensor \(z = E(x)\).  
2. **Diffuse & Denoise in Latent Space** – the DDPM/SDE process operates on \(z\), training a U-Net to predict noise in the latent domain. 
3. **Decode** – after the reverse diffusion yields \(\hat{z}\), a decoder \(D\) reconstructs the final high-resolution image \(\hat{x}=D(\hat{z})\).  

Because \(h{\,\times\,}w \ll H{\,\times\,}W\) (e.g., \(64{\times}64\) vs.\ \(512{\times}512\)), training and inference become tractable on a single GPU while maintaining photorealistic detail. Subsequent work—most notably **Stable Diffusion**—extends this framework with text conditioning and **ControlNet** branches for structural guidance. 

#### Text-Prompt Guidance in Diffusion Models

Before introducing **ControlNet**, it is useful to recall that modern diffusion models can already be **steered by natural-language prompts**.  
The mechanism was formalised in the OpenAI paper *“GLIDE: Towards Photorealistic Image Generation and Editing with Text-Guided Diffusion Models”* (Nichol *et al.*, 2022). The authors demonstrate that if you pass a prompt through a text encoder—initially CLIP ViT-L/14—and concatenate the resulting embedding to the U-Net’s latent or cross-attention layers, the denoising process learns to minimise noise *while satisfying the text condition*. 

Two guidance strategies proved especially effective:

| Strategy | Idea |
|----------|------|
| **CLIP Guidance** | During sampling, use the CLIP image encoder to rank intermediate images by semantic similarity to the prompt and nudge the diffusion trajectory towards higher-ranked samples. | 
| **Classifier-Free Guidance (CFG)** | Train the model with and without a prompt (empty string) and, at inference, interpolate between the two predictions to trade diversity for fidelity. | 

This text-conditioning recipe underpins **Stable Diffusion**:  
* v1.x checkpoints inherit the *pre-trained* OpenAI CLIP encoder used in GLIDE and DALL·E 2.  
* v2.x replaces it with **OpenCLIP**—a from-scratch replication trained on the LAION-2B dataset—which improves prompt adherence and removes the need for proprietary weights.

In short, a prompt such as  
`"Photo of a bronze bust, polished, museum lighting"`  
is converted into a CLIP embedding that conditions **every** denoising step, yielding images that match the described content even before any additional control mechanisms (e.g., ControlNet) are applied.

#### ControlNet

![image](https://github.com/user-attachments/assets/a101b591-9108-4b67-a9c9-4c1c7ad652d2)

**ControlNet** adds an *extra, trainable branch* to a **frozen** text-guided Latent Diffusion Model so that generation can be steered by pixel-aligned inputs such as edge maps, depth, pose, or segmentation. 
A duplicate of the U-Net encoder–decoder receives the condition map \(c\); its layers are connected to the frozen backbone through **zero-initialised 1 × 1 convolutions**, which output zeros at the start of training and therefore leave the base model’s behaviour untouched.
During fine-tuning, these “ZeroConvs” gradually learn a residual that injects just enough spatial information to satisfy \(c\), allowing robust training even on datasets as small as 50 k pairs and preventing catastrophic drift. 
Official checkpoints cover Canny edges, depth, OpenPose skeletons, normal maps, and more, and the **ControlNet 1.1** release adds “guess-mode” and cached feature variants for ~45 % faster inference. 

*Role in this repo:* we use ControlNet (edge or depth) to lock geometry across chosen 360° renders which are then being transformed by Stable Diffusion into new images according to the prompt. It takes place before EbSynth propagates style and Gaussian Splatting rebuilds the 3-D model, ensuring both structural fidelity and temporal coherence.

### EbSynth (Example-Based Image Synthesis)

**EbSynth** is a patch-based, example-guided algorithm that propagates an artist-painted key frame across the remaining frames of a video while preserving both local texture details and global temporal coherence. The method was first presented as *“Stylizing Video by Example”* at SIGGRAPH 2019 and builds on earlier work such as *StyLit* (SIGGRAPH 2016) and the PatchMatch family of nearest-neighbour algorithms. 

#### How it works

1. **Key-frame stylisation** – The user paints or edits one (or more) reference frames with any 2-D tool.  
2. **Guidance map computation** – Dense correspondences between the key frame(s) and each target frame are estimated (usually with optical flow).  
3. **PatchMatch transfer** – For every patch in the target frame, EbSynth finds the best-matching patch in the key frame and copies its pixels; a confidence map weights the blending. 
4. **Edge-aware blending & refinement** – Overlaps are resolved with guided filtering; an optional temporal pass enforces consistency over successive frames. 

Because the algorithm works in image space, it inherits the exact style of the artist painting—including brush strokes and high-frequency detail—something that neural style-transfer often washes out. The process is fast (real-time or faster per frame) and runs entirely on the GPU.

#### Practical tips for this repository

| Step | Recommendation |
|------|---------------|
| Key-frame count | 9 – 16 well-chosen views usually suffice for a 360 ° turntable; add more only when topology changes drastically. |
| Resolution | Keep the rendered frames and painted key frames at the same native resolution to avoid resampling artefacts. |
| Integration with A1111 | The community extension `CiaraStrawberry/TemporalKit` can automate the call from Stable Diffusion to EbSynth if you prefer a single click workflow. |
#### Role in our 3-D pipeline

After Stable Diffusion + ControlNet generates high-quality but *per-key-frame* stylised renders, EbSynth sweeps through the sequence and harmonises consistency of transformed frames across time. This step is crucial before we pass the imagery to **Gaussian Splatting**, because temporal consistency directly improves the quality of the reconstructed 3-D point-cloud.








