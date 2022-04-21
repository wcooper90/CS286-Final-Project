import glob
from PIL import Image


# animation code pulled from
# https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python


# filepaths
fp_in = "/mnt/c/Users/wcoop/Desktop/Code/CS286/FinalProject/data/*.png"
fp_out = "image.gif"

# https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
imgs = (Image.open(f) for f in sorted(glob.glob(fp_in)))
img = next(imgs)  # extract first image from iterator
img.save(fp=fp_out, format='GIF', append_images=imgs,
         save_all=True, duration=1400, loop=0)
