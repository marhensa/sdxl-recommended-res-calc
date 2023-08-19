# sdxl-recommended-res-calc
A simple script (_**also a ComfyUI custom node thanks to [CapsAdmin](https://github.com/marhensa/sdxl-recommended-res-calc/issues/1)**_). It is used to calculate the recommended initial latent size for SDXL image generation and its Upscale Factor based on the desired Final Resolution output.

According to [SDXL paper references](https://arxiv.org/pdf/2307.01952.pdf) (Page 17), it's advised to avoid arbitrary resolutions and stick to this initial resolution, as SDXL was trained using this specific resolution.

tl;dr : Basicaly, you are typing your FINAL target resolution, it will gives you :
1. what resolution you should use according to SDXL suggestion as initial input resolution
2. how much upscale it needs to get that final resolution (both normal upscaler or upscaler value that have been 4x scaled by upscale model)

[CapsAdmin](https://github.com/CapsAdmin) pointed [here](https://github.com/marhensa/sdxl-recommended-res-calc/issues/1), that modifying this Python script could be a custom node by itself in ComfyUI. Now this repo also can be used as custom node in ComfyUI

**Usage Showcase In ComfyUI**
![image](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/91ce3c67-f5af-4978-b27f-ebd14260ce3e)

**To install it as ComfyUI custom node installation** :
1. Go to this folder /ComfyUI/custom_nodes/
2. Open command prompt to that folder, type
3. git clone https://github.com/marhensa/sdxl-recommended-res-calc.git
4. Restart ComfyUI, now this custo node is located in "utils" node section.
5. Usage: DesiredXSIZE and DesiredYSIZE is your TARGET FINAL RESOLUTION, Upscale Factor OR Reverse Upscale Factor is used as example above

Example Workflow of usage in ComfyUI : [JSON](https://github.com/marhensa/sdxl-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sdxl-recommended-res-calc_upscale-case.json) / [PNG](https://github.com/marhensa/sdxl-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sdxl-recommended-res-calc_upscale-case.png)

As standalone (Not Using ComfyUI):
1. Download (Click green button Code > Download ZIP) from repo. Or this [direct link](https://github.com/marhensa/sdxl-recommended-res-calc/archive/refs/heads/main.zip).
2. Make sure .Py and .Bat file on same folder
3. Double click .Bat file! (.Sh for Linux)
4. Input your desired Final Resolution
5. You'll get recommended SDXL Initial Image Size, and its upscale factor to reach the Final Resolution.


**As Standalone**
![Screenshot 2023-08-19 173513](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/e5f4a34e-cb07-4339-bcca-0bbf08c29946)
![Screenshot 2023-08-19 173523](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/6a9e170b-9028-466a-b942-f50bd48ce44c)
![Screenshot 2023-08-19 173615](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/fd557a6e-e80d-4815-9f2e-2a9f7337554c)

**References**
SDXL Paper: https://arxiv.org/abs/2307.01952 | https://arxiv.org/pdf/2307.01952.pdf | Page 17
