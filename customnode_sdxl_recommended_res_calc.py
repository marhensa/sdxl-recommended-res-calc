# As Per CapsAdmin (https://github.com/CapsAdmin) suggest, it could be a ComfyUI Custom Node if modified.
# https://github.com/marhensa/sdxl-recommended-res-calc/issues/1
# This is his/her edit add suggestion
# Many thanks!

# Accepted aspect ratios and corresponding XSIZE, YSIZE, and NUMRATIO
# Accepted aspect ratios and pixel size is derived from this SDXL paper
# https://arxiv.org/abs/2307.01952 https://arxiv.org/pdf/2307.01952.pdf
# Page 17 "We use the following image resolutions for mixed-aspect ratio finetuning as described in Section 2.3"

# Horizontal aspect ratio
accepted_ratios_horizontal = {
    "4:1": (2048, 512, 4.00),
    "31:8": (1984, 512, 3.88),
    "15:4": (1920, 512, 3.75),
    "25:7": (1856, 512, 3.63),
    "28:9": (1792, 576, 3.11),
    "3:1": (1728, 576, 3.00),
    "26:9": (1664, 576, 2.89),
    "5:2": (1600, 640, 2.50),
    "12:5": (1536, 640, 2.40),
    "25:12": (1472, 704, 2.09),
    "2:1": (1408, 704, 2.00),
    "25:13": (1344, 704, 1.91),
    "7:4": (1344, 768, 1.75),
    "5:3": (1280, 768, 1.67),
    "25:17": (1216, 832, 1.46),
    "25:18": (1152, 832, 1.38),
    "50:39": (1152, 896, 1.29),
    "50:41": (1088, 896, 1.21),
    "25:22": (1088, 960, 1.13),
    "50:47": (1024, 960, 1.07)
}

# Vertical aspect ratio
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
    "5:12": (640, 1536, 0.42),
    "2:5": (640, 1600, 0.40),
    "9:26": (576, 1664, 0.35),
    "1:3": (576, 1728, 0.33),
    "9:28": (576, 1792, 0.32),
    "7:25": (512, 1856, 0.28),
    "4:15": (512, 1920, 0.27),
    "8:31": (512, 1984, 0.26),
    "1:4": (512, 2048, 0.25)
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
                    "max": 8192, #Maximum value
                    "step": 2 #Slider's step
                }),
                "desiredYSIZE": ("INT", {
                    "default": 1024, 
                    "min": 0, #Minimum value
                    "max": 8192, #Maximum value
                    "step": 2 #Slider's step
                }),
            },
        }

    RETURN_TYPES = ("INT","INT", "FLOAT", "FLOAT",)
    RETURN_NAMES = ("recom width","recom height","upscale factor", "reverse upscale (for 4x-upscaler)",)
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
