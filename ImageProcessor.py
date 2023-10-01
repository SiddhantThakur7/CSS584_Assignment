import cv2
import random

class ImageProcessor:
    def __init__(self) -> None:
        self.images = dict()
        self.resolution_x = 384
        self.resolution_y = 256 
        for i in range(1, 101):
            filepath = f'.\\images\\png\\{i}.png'
            self.images[i] = {'representation': cv2.imread(filepath, cv2.IMREAD_COLOR), 'path': filepath}
        
    def randomize_order(self):
        arr = list(self.images.values())
        random.shuffle(arr)
        return arr
