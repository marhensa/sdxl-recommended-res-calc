def calculate_aspect_ratios(desiredXSIZE, desiredYSIZE):
    # Accepted aspect ratios and corresponding XSIZE, YSIZE, and NUMRATIO
    accepted_ratios_horizontal = {
        "4:3": (1152, 896, 1.29),
        "3:2": (1216, 832, 1.46),
        "16:9": (1344, 768, 1.75),
        "21:9": (1536, 640, 2.40)
    }
    
    accepted_ratios_vertical = {
        "3:4": (896, 1152, 0.78),
        "2:3": (832, 1216, 0.68),
        "9:16": (768, 1344, 0.57),
        "9:21": (640, 1536, 0.42)
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
    print(colorGREEN + "SDXL  :", accepted_YSIZE, colorRESET)
    
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
    print("calculated from (", more_less, ") avoid shortage,")
    print("you can crop (", excesstocrop, ") excess later")
    print(colorGREEN + "Scale factor :", scaling_factor, colorRESET)

    # Calculate the downscale factor from Upscale 4x Node and round to 3 digits
    downscalefrom4x_factor = round(scaling_factor / 4, 3)
    
    print("\nOr downscale factor after using 4x-Upscaler Node = (", scaling_factor, "/ 4 )")
    print(colorGREEN + "Downscale AFTER 4x-Upscaler Node usage :", downscalefrom4x_factor, colorRESET)
    print("")
    print("")
    print("=====")

# Function to get user input and ask for another set of sizes
def get_user_input():
    while True:
        desiredXSIZE = int(input("\nEnter the Desired Final Width (X Size): "))
        desiredYSIZE = int(input("Enter the Desired Final Height (Y Size): "))

        # Call the function to calculate the aspect ratios and scaling factor
        calculate_aspect_ratios(desiredXSIZE, desiredYSIZE)

        another_input = input("Do you want to input another set of sizes? (Y/N): ")
        if another_input.lower() != 'y':
            break

# Start the script by getting user input for the first set of sizes
get_user_input()
