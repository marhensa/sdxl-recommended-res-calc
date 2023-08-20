import os

"""
    
This is the standalone python script, for ComfyUI custom node it's on other file: customnode_sdxl_recommended_res_calc.py
    
A simple tool to calculate the recommended initial latent size 
for SDXL image generation and its Upscale Factor 
based on the desired Final Resolution output 
    
Marhensa Aditya Hadi (2023)
    
"""

def calculate_aspect_ratios(desiredXSIZE, desiredYSIZE):
    # Accepted aspect ratios and corresponding XSIZE, YSIZE, and NUMRATIO
    
    # Accepted aspect ratios and pixel size is derived from this SDXL paper
    # https://arxiv.org/abs/2307.01952 https://arxiv.org/pdf/2307.01952.pdf
    # Page 17 "We use the following image resolutions for mixed-aspect ratio finetuning as described in Section 2.3"
    
# Horizontal aspect ratio
    accepted_ratios_horizontal = {
    "4:1": (2048, 512, 4.000),
    "31:8": (1984, 512, 3.875),
    "15:4": (1920, 512, 3.750),
    "29:8": (1856, 512, 3.625),
    "28:9": (1792, 576, 3.111),
    "3:1": (1728, 576, 3.000),
    "26:9": (1664, 576, 2.889),
    "5:2": (1600, 640, 2.502),
    "12:5": (1536, 640, 2.402),
    "23:11": (1472, 704, 2.091),
    "2:1": (1408, 704, 2.002),
    "21:11": (1344, 704, 1.909),
    "7:4": (1344, 768, 1.750),
    "5:3": (1280, 768, 1.667),
    "19:13": (1216, 832, 1.462),
    "18:13": (1152, 832, 1.385),
    "9:7": (1152, 896, 1.286),
    "17:14": (1088, 896, 1.214),
    "17:15": (1088, 960, 1.133),
    "16:15": (1024, 960, 1.067)
    }

# Vertical aspect ratio
    accepted_ratios_vertical = {
    "15:16": (960, 1024, 0.938),
    "15:17": (960, 1088, 0.882),
    "14:17": (896, 1088, 0.824),
    "7:9": (896, 1152, 0.778),
    "13:18": (832, 1152, 0.722),
    "13:19": (832, 1216, 0.684),
    "3:5": (768, 1280, 0.600),
    "4:7": (768, 1344, 0.571),
    "11:21": (704, 1344, 0.524),
    "1:2": (704, 1408, 0.500),
    "11:23": (704, 1472, 0.478),
    "5:12": (640, 1536, 0.417),
    "2:5": (640, 1600, 0.400),
    "9:26": (576, 1664, 0.346),
    "1:3": (576, 1728, 0.333),
    "9:28": (576, 1792, 0.321),
    "8:29": (512, 1856, 0.276),
    "4:15": (512, 1920, 0.267),
    "8:31": (512, 1984, 0.258),
    "1:4": (512, 2048, 0.250)
    }
    
# Square aspect ratio
    accepted_ratios_square = {
    "1:1": (1024, 1024, 1.000)
    }

    
    # Calculate the aspect ratio of the desired size
    desired_ratio = desiredXSIZE / desiredYSIZE
    
    # Find the closest accepted aspect ratio
    closest_ratio = None
    closest_diff = float('inf')
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_horizontal.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    for ratio, (x_size, y_size, num_ratio) in accepted_ratios_vertical.items():
        diff = abs(num_ratio - desired_ratio)
        if diff < closest_diff:
            closest_ratio = ratio
            closest_diff = diff
    
    # Compare with square aspect ratio
    x_size, y_size, num_ratio = accepted_ratios_square["1:1"]
    diff = abs(num_ratio - desired_ratio)
    if diff < closest_diff:
        closest_ratio = "1:1"
   
   # ANSI escape sequences for text colors
    colorGREEN = "\033[32m"
    colorRESET = "\033[0m"

    # Display the accepted aspect ratio
    print("=====")
    print("")
    print("Resolutions and ratios are based from SDXL paper")
    print("https://arxiv.org/pdf/2307.01952.pdf Page-17")
    print("")
    print("Nearest SDXL recommended ratio from", colorGREEN + str(desiredXSIZE) + colorRESET, "x", colorGREEN + str(desiredYSIZE) + colorRESET, ":")
    if closest_ratio in accepted_ratios_horizontal:
        print(colorGREEN + "HORIZONTAL", colorRESET)
    elif closest_ratio in accepted_ratios_vertical:
        print(colorGREEN + "VERTICAL", colorRESET)
    else:
        print(colorGREEN + "SQUARE", colorRESET)
    print(colorGREEN + closest_ratio, colorRESET)
    
    # Display the corresponding accepted XSIZE and YSIZE
    if closest_ratio in accepted_ratios_horizontal:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_horizontal[closest_ratio]
    elif closest_ratio in accepted_ratios_vertical:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_vertical[closest_ratio]
    else:
        accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_square[closest_ratio]
    print("\nRecommended initial SDXL size for", closest_ratio, ":")
    print(colorGREEN + "SDXL Width  :", accepted_XSIZE, colorRESET)
    print(colorGREEN + "SDXL Height :", accepted_YSIZE, colorRESET)
    
    # Calculate the upscale factor for width and height
    upscale_factor_width = desiredXSIZE / accepted_XSIZE
    upscale_factor_height = desiredYSIZE / accepted_YSIZE

    # Compare the upscale factors for width and height and select the larger one
    if upscale_factor_width >= upscale_factor_height:
        more_less = "SDXL Width"
        accepted_size = accepted_XSIZE
        desired_size = desiredXSIZE
        excesstocrop = "Final Height"
        scaling_factor = round(upscale_factor_width, 3)
    else:
        more_less = "SDXL Height"
        accepted_size = accepted_YSIZE
        desired_size = desiredYSIZE
        excesstocrop = "Final Width"
        scaling_factor = round(upscale_factor_height, 3)
    
    print("\nScaling factor to reach", desiredXSIZE, "x", desiredYSIZE)
    print("calculated from (", more_less, ") to avoid shortage,")
    print("you can crop (", excesstocrop, ") excess later")
    print(colorGREEN + "Scale factor :", scaling_factor, colorRESET)

    # Calculate the downscale factor from Upscale 4x Node and round to 3 digits
    downscalefrom2x_factor = round(scaling_factor / 4, 3)
    
    print("\nReverse Upscale Factor after using 4x-Upscaler Node = (", scaling_factor, "/ 4 )")
    print(colorGREEN + "Reverse Upscale Factor for 4x-Upscaler :", downscalefrom2x_factor, colorRESET)
    
    # Calculate the downscale factor from Upscale 2x Node and round to 3 digits
    downscalefrom4x_factor = round(scaling_factor / 2, 3)
    
    print("\nReverse Upscale Factor after using 2x-Upscaler Node = (", scaling_factor, "/ 2 )")
    print(colorGREEN + "Reverse Upscale Factor for 2x-Upscaler :", downscalefrom4x_factor, colorRESET)
    print("")
    print("=====")

# Function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to get user input and ask for another set of sizes
def get_user_input():
    while True:
        clear_screen()  # Clear the terminal screen
        desiredXSIZE = int(input("\nEnter the Desired Final Width (X Size): "))
        desiredYSIZE = int(input("Enter the Desired Final Height (Y Size): "))

        # Call the function to calculate the aspect ratios and scaling factor
        calculate_aspect_ratios(desiredXSIZE, desiredYSIZE)

        another_input = input("Do you want to input another set of sizes? (Y/N): ")
        if another_input.lower() != 'y':
            break

# Start the script by getting user input for the first set of sizes
get_user_input()
