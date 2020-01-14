from ecg_reporter.app.logs import add_to_log
from ecg_reporter.app.configs import get_config
import os

def clear_images_directory():
    images_directory = get_config('images_path')

    for filename in os.listdir(images_directory):
        os.remove(images_directory + '/' + filename)

    add_to_log('Images directory been cleared')