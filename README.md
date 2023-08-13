# sdxl-recommended-res-calc
A simple script (_**also converted into a ComfyUI custom node by**_ [CapsAdmin](https://github.com/marhensa/sdxl-recommended-res-calc/issues/1)) to calculate the recommended initial latent size for SDXL image generation and its Upscale Factor based on the desired Final Resolution output.

According to many references, it's advised to avoid arbitrary resolutions and stick to this initial resolution, as SDXL was trained using this specific resolution.

tl;dr : Basicaly, you are typing your FINAL target resolution, it will gives you :
1. what resolution you should use according to SDXL suggestion as initial input resolution
2. how much upscale it needs to get that final resolution (both normal upscaler or upscaler value that have been 4x scaled by upscale model)

[CapsAdmin](https://github.com/CapsAdmin) pointed [here](https://github.com/marhensa/sdxl-recommended-res-calc/issues/1), that modifying this Python script could be a custom node by itself in ComfyUI. Here's the edit from CapsAdmin that loads on ComfyUI, and its implementation

**In ComfyUI**

![image](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/c854e461-84d0-421c-8a41-7309d178ea2d)

**To install it as ComfyUI custom node installation** :
1. Go to this folder /ComfyUI/custom_nodes
2. Open command prompt, type
3. git clone https://github.com/marhensa/sdxl-recommended-res-calc.git
4. Restart ComfyUI, now it's located in "utils" node section.
5. To use: DesiredXSIZE and DesiredYSIZE is your TARGET FINAL RESOLUTION

Example Workflow of usage in ComfyUI : [JSON](https://github.com/marhensa/sdxl-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sdxl-recommended-res-calc_upscale-case.json) / [PNG](https://github.com/marhensa/sdxl-recommended-res-calc/blob/main/_use-case-example-comfyui-nodes/sdxl-recommended-res-calc_upscale-case.png)

As standalone (Not Using ComfyUI):
1. Download (Click green button Code > Download ZIP) from repo. Or direct link.
2. Make sure .Py and .Bat file on same folder
3. Double click .Bat file! (.Sh for Linux)
4. Input your desired Final Resolution
5. You'll get recommended SDXL Initial Image Size, and its upscale factor to reach the Final Resolution.


**As Standalone**

![Screenshot1xx](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/9dfebf48-c324-4459-bd8d-009689fc8964)

![Screenshot2xx](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/f229e761-ccaa-45ab-aa45-3e004fc2631e)

![Screenshot3xx](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/605ec1c0-1ef4-41a3-bb8e-3da39495a0de)


**References**

https://arxiv.org/abs/2307.01952 | https://arxiv.org/pdf/2307.01952.pdf | Page 17 

![image](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/b9526007-2509-4f9f-966c-c8b3a57c6fc9)
