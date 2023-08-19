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

    RETURN_TYPES = ("INT","INT", "FLOAT", "FLOAT", "FLOAT",)
    RETURN_NAMES = ("recomm width","recomm height","upscale factor", "reverse upscale for 4x", "reverse upscale for 2x",)
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
        
        downscalefrom2x_factor = round(scaling_factor / 2, 3)

        return (accepted_XSIZE, accepted_YSIZE, scaling_factor, downscalefrom4x_factor, downscalefrom2x_factor)


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "RecommendedResCalc": RecommendedResCalc
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RecommendedResCalc": "Recommended Resolution Calculator"
}
