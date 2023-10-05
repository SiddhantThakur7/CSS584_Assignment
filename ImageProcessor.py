import cv2
import numpy as np
import random


class ImageProcessor:
    def __init__(self) -> None:
        self.images = dict()
        self.INTENSITY_COEFFICIENT_MATRIX = np.array([[0.114], [0.587], [0.299]])
        self.resolution_x = 384
        self.resolution_y = 256
        for i in range(1, 2):
            filepath = f".\\images\\png\\{i}.png"
            image = cv2.imread(filepath, cv2.IMREAD_COLOR)
            self.images[i] = {
                "representation": image,
                # "intensity_representation": cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
                "intensity_representation": np.transpose(np.dot(image, self.INTENSITY_COEFFICIENT_MATRIX))[0],
                "path": filepath,
            }
            # print(self.images)

    def randomize_order(self):
        # print(cv2.calcHist(self.images[1]['intensity_representation'],[1],None,[25],[0,255]))

        im = self.images[1]['intensity_representation']
        # im = self.images[1]['intensity_representation2']
        t = self.calculate_intensity_histogram(im)
        print(t)
        
        # arr = list(self.images.values())
        # random.shuffle(arr)
        # return arr
    
    def calculate_intensity_histogram(self, representation):
        hist = [0]*25
        for i in range(len(representation)):
            for j in range(len(representation[0])):
                x = int(representation[i][j] // 10)
                if x > 24.0:
                    x = 24
                hist[x] += 1
        return hist



X = ImageProcessor()
X.randomize_order()