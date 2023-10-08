import cv2
import numpy as np
import random


class ImageProcessor:
    def __init__(self) -> None:
        self.images = dict()
        self.INTENSITY_COEFFICIENT_MATRIX = np.array([[0.114], [0.587], [0.299]])
        for i in range(1, 100):
            filepath = f".\\images\\png\\{i}.png"
            image = cv2.imread(filepath, cv2.IMREAD_COLOR)
            self.images[i] = {
                "representation": image,
                'size': len(image) * (len(image[0])),
                # "intensity_representation": cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
                "intensity_representation": np.transpose(np.dot(image, self.INTENSITY_COEFFICIENT_MATRIX))[0],
                "path": filepath,
            }
        
        self.process_intensity_histograms()


    def randomize_order(self):
        # print(cv2.calcHist(self.images[1]['intensity_representation'],[1],None,[25],[0,255]))

        im = self.images[1]['intensity_representation']
        # im = self.images[1]['intensity_representation2']
        t = self.calculate_intensity_histogram(im)
        # print(t)
        
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
        return np.array(hist)

    def process_intensity_histograms(self):
        for image in self.images:
            self.images[image]['intensity_histogram'] = self.calculate_intensity_histogram(self.images[image]['intensity_representation'])
        
    def caclulate_distance(self, image1, image2):
        im1  = image1['intensity_histogram'] / image1['size']
        im2  = image2['intensity_histogram'] / image2['size']
        return np.sum(np.abs(im1 - im2))
    
    def process_image_distances(self, chosen_image):
        image_distances = []
        for image in self.images:
            if chosen_image != image:
                distance_info = {
                    'name': image,
                    'path': self.images[image]['path'],
                    'distance': self.caclulate_distance(self.images[chosen_image], self.images[image])
                }
                image_distances.append(distance_info)
        image_distances.sort(key = lambda x: x['distance'])
        
        # for i in image_distances[:21]:
        #     print(i['name'])
        return image_distances



# X = ImageProcessor()
# X.process_intensity_histograms()
# X.process_image_distances(1)