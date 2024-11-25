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

![Uploading ezgif-2-14c20ef111.gif…]()




