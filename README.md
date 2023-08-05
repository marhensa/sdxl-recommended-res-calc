# sdxl-recommended-res-calc
Here's a simple script to calculate the recommended initial latent size for SDXL image generation and its Upscale Factor based on the desired Final Resolution output.

According to many references, it's advised to avoid arbitrary resolutions and stick to this initial resolution, as SDXL was trained using this specific resolution.

[CapsAdmin](https://github.com/marhensa/sdxl-recommended-res-calc/issues/1#issue-1837648293) pointed [here](https://www.reddit.com/r/StableDiffusion/comments/15iou69/comment/juvgrqn/?utm_source=reddit&utm_medium=web2x&context=3), that modifying this Python script could be a custom node by itself in ComfyUI. Here's the edit from CapsAdmin that loads on ComfyUI, and its implementation

**In ComfyUI**

![image](https://github.com/marhensa/sdxl-recommended-res-calc/assets/816600/dc295c55-8ad6-4fb3-890f-1831d82c83d6)

To install it as ComfyUI custom node installation :
1. Go to this folder /ComfyUI/custom_nodes
2. Open command prompt, type
3. Git clone https://github.com/marhensa/sdxl-recommended-res-calc.git
4. Restart ComfyUI, now it's located in "utils" node section.


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
