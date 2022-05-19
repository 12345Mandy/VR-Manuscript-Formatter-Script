import numpy as np
import cv2 as cv
import os


# overlay helpful -> https://stackoverflow.com/questions/14063070/overlay-a-smaller-image-on-a-larger-image-python-opencv
# load images ->https://stackoverflow.com/questions/30230592/loading-all-images-using-imread-from-a-given-folder
# path to folder. By default, os.listdir takes the present directory as a path.


# assumes recto1-verso1 recto2-verso2 pattern -> 0 increment so even indices are recto, odd indices are verso


def load_images_from_folder(path_to_folder):
    images = []
    for filename in os.listdir(path_to_folder):
        img = cv.imread(os.path.join(path_to_folder, filename))
        if img is not None:
            print("not none")
            images.append(img)
    return images


def flip_horz_verso(images):
    for i in range(1, len(images), 2):
        images[i] = cv.flip(images[i], 1)
    return images


def crop(images):
    crop_amt = 200
    for i in range(0, len(images)):
        images[i] = np.asarray(images[i])
        print(images[i].shape)
        images[i] = images[i][:, crop_amt:, :]
    return images

#3821 5692
def format_images():
    # this assumes the template is in the current directory
    template_filename = "Page_Template.png"
    template = cv.imread(template_filename)
    path_to_folder = "images-orig"  # note that we are saving formated pages to this folder too
    images = load_images_from_folder(path_to_folder)
    images = flip_horz_verso(images)
    images = crop(images)
    t_height, t_width = template.shape[0], template.shape[1]
    IMAGE_HEIGHT = 5692
    IMAGE_WIDTH = 3821
    for i in range(0, len(images), 2):
        # resize -> https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
        # recto = cv.resize(np.asarray(images[i]), (IMAGE_WIDTH, IMAGE_HEIGHT))
        dim = (IMAGE_WIDTH, IMAGE_HEIGHT)
        print(dim)
        print(images[i])
        recto = cv.resize(
            images[i], dim, interpolation=cv.INTER_AREA)
        # note that this is already horz flipped
        if i+1>len(images):
            basic_page = cv.imread("base.png")
            verso = cv.resize(basic_page, (IMAGE_WIDTH, IMAGE_HEIGHT))
        else:
            verso = cv.resize(images[i+1], (IMAGE_WIDTH, IMAGE_HEIGHT))
        print(recto.shape)
        print(verso.shape)
        page = cv.hconcat([recto, verso])
        print(page.shape)
        page_formatted = template
        page_formatted[t_height-IMAGE_HEIGHT:, 0:IMAGE_WIDTH*2, :] = page
        path = "formatted-pages"
        cv.imwrite(os.path.join(path, str(i/2)+".png"), page_formatted)
        # print(filename)
        # cv.imwrite(filename, page_formated)
        print("After saving")
        print(os.listdir(path_to_folder))


format_images()
