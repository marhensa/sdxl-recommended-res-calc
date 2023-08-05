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

class RecommendedResCalc:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "desiredXSIZE": ("INT", {
                    "default": 1024, 
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 64 #Slider's step
                }),
                "desiredYSIZE": ("INT", {
                    "default": 1024, 
                    "min": 0, #Minimum value
                    "max": 4096, #Maximum value
                    "step": 64 #Slider's step
                }),
            },
        }

    RETURN_TYPES = ("INT","INT", "FLOAT", "FLOAT",)
    RETURN_NAMES = ("recom width","recom height","upscale factor", "downscale factor (from 4x upscaler)",)
    FUNCTION = "calc"
    CATEGORY = "utils"

    def calc(self, desiredXSIZE, desiredYSIZE):
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

        if closest_ratio in accepted_ratios_horizontal:
            accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_horizontal[closest_ratio]
        elif closest_ratio in accepted_ratios_vertical:
            accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_vertical[closest_ratio]
        else:
            accepted_XSIZE, accepted_YSIZE, _ = accepted_ratios_square[closest_ratio]
        
        upscale_factor_width = desiredXSIZE / accepted_XSIZE
        upscale_factor_height = desiredYSIZE / accepted_YSIZE

        # Compare the upscale factors for width and height and select the larger one
        if upscale_factor_width >= upscale_factor_height:
            scaling_factor = round(upscale_factor_width, 3)
        else:
            scaling_factor = round(upscale_factor_height, 3)

        downscalefrom4x_factor = round(scaling_factor / 4, 3)

        return (accepted_XSIZE, accepted_YSIZE, scaling_factor, downscalefrom4x_factor)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "RecommendedResCalc": RecommendedResCalc
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RecommendedResCalc": "Recommended Resolution Calculator"
}