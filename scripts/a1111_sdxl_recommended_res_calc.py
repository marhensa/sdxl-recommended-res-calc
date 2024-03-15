import logging

import gradio as gr

from modules import scripts
from modules.processing import StableDiffusionProcessing
from customnode_sdxl_recommended_res_calc import RecommendedResCalc

calc = RecommendedResCalc().calc

class ScriptRecommendedResCalc(scripts.Script):
    name = "SDXL Recommended Resolution Calculator"
    section = "dimensions"

    def title(self):
        return self.name
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    
    def ui(self, is_img2img):
        enable = gr.Checkbox(label="Use SDXL recommended resolution", value=False, elem_id="sdxl_recommended_resolution_calculator_enable")
        return [
            enable,
        ]

    def before_process(self, p: StableDiffusionProcessing, *args):
        if args[0] and p.width > 0 and p.height > 0:
            width, height, _, _, _ = calc(p.width, p.height)

            logging.info(f"{p.width}x{p.height} -> {width}x{height}")
            p.width = width
            p.height = height
