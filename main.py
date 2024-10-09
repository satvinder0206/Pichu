import torch
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("OnomaAIResearch/Illustrious-xl-early-release-v0")



def generate_image(prompt,steps):
    image = pipe(prompt).images[0]
    return image
