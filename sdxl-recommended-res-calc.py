import os

def calculate_aspect_ratios(desiredXSIZE, desiredYSIZE):
    # Accepted aspect ratios and corresponding XSIZE, YSIZE, and NUMRATIO
    
    # Accepted aspect ratios and pixel size is derived from this SDXL paper
    # https://arxiv.org/abs/2307.01952 https://arxiv.org/pdf/2307.01952.pdf
    # Page 17 "We use the following image resolutions for mixed-aspect ratio finetuning as described in Section 2.3"
    
    accepted_ratios_horizontal = {
        "4:1": (2048, 512, 4.00),
        "97:25": (1984, 512, 3.88),
        "15:4": (1920, 512, 3.75),
        "101:28": (1856, 512, 3.63),
        "311:100": (1792, 576, 3.11),
        "3:1": (1728, 576, 3.00),
        "289:100": (1664, 576, 2.89),
        "5:2": (1600, 640, 2.50),
        "12:5": (1536, 640, 2.40),
        "209:100": (1472, 704, 2.09),
        "2:1": (1408, 704, 2.00),
        "191:100": (1344, 704, 1.91),
        "7:4": (1344, 768, 1.75),
        "5:3": (1280, 768, 1.67),
        "73:50": (1216, 832, 1.46),
        "69:50": (1152, 832, 1.38),
        "129:100": (1152, 896, 1.29),
        "121:100": (1088, 896, 1.21),
        "113:100": (1088, 960, 1.13),
        "107:100": (1024, 960, 1.07)
    }
    
    accepted_ratios_vertical = {
        "47:50": (960, 1024, 0.94),
        "22:25": (960, 1088, 0.88),
        "41:50": (896, 1088, 0.82),
        "39:50": (896, 1152, 0.78),
        "18:25": (832, 1152, 0.72),
        "17:25": (832, 1216, 0.68),
        "3:5": (768, 1280, 0.60),
        "4:7": (768, 1344, 0.57),
        "13:25": (704, 1344, 0.52),
        "1:2": (704, 1408, 0.50),
        "12:25": (704, 1472, 0.48),
        "7:17": (640, 1536, 0.42),
        "2:5": (640, 1600, 0.40),
        "7:20": (576, 1664, 0.35),
        "1:3": (576, 1728, 0.33),
        "4:13": (576, 1792, 0.32),
        "7:25": (512, 1856, 0.28),
        "1:4": (512, 1920, 0.27),
        "13:50": (512, 1984, 0.26),
        "1:4": (512, 2048, 0.25)
    }
    
    # Square aspect ratio
    accepted_ratios_square = {
        "1:1": (1024, 1024, 1)
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
    print("Nearest recommended ratio from", colorGREEN + str(desiredXSIZE) + colorRESET, "x", colorGREEN + str(desiredYSIZE) + colorRESET, ":")
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
    downscalefrom4x_factor = round(scaling_factor / 4, 3)
    
    print("\nOr downscale factor after using 4x-Upscaler Node = (", scaling_factor, "/ 4 )")
    print(colorGREEN + "Downscale AFTER 4x-Upscaler Node usage :", downscalefrom4x_factor, colorRESET)
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
