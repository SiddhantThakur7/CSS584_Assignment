import cv2
import numpy as np

def binary_of(x, bits = 8):
    return format(x, f'0{bits}b')

def int_of(x):
    return int(x, 2)

class ImageProcessor:
    def __init__(self) -> None:
        self.images = dict()
        self.INTENSITY_COEFFICIENT_MATRIX = np.array([[0.114], [0.587], [0.299]])
        for i in range(1, 101):
            filepath = f".\\images\\png\\{i}.png"
            image = cv2.imread(filepath, cv2.IMREAD_COLOR)
            resolution_x = len(image)
            resolution_y = len(image[0])
            self.images[i] = {
                "representation": image,
                'resolution_x':resolution_x,
                'resolution_y': resolution_y,
                'resolution': resolution_x * resolution_y,
                "color_code_representation": self.get_color_code_representaion(image, resolution_x, resolution_y),
                "intensity_representation": np.transpose(np.dot(image, self.INTENSITY_COEFFICIENT_MATRIX))[0],
                "path": filepath,
            }
        
        self.process_histograms('intensity')
        self.process_histograms('color_code')

    def get_color_code_representaion(self, image, m, n):
        color_code_array = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                significant_bits = ''
                for k in reversed(range(3)):
                    significant_bits += binary_of(image[i][j][k])[:2]
                color_code_array[i][j] = int_of(significant_bits)
        return color_code_array
    
    def calculate_histogram(self, representation, type = 'intensity'):
        hist = [0] * (25 if type == 'intensity' else 64)
        for i in range(len(representation)):
            for j in range(len(representation[0])):
                x = int(representation[i][j] // 10) if type == 'intensity' else representation[i][j]
                if type == 'intensity' and x > 24.0:
                    x = 24
                hist[x] += 1
        return np.array(hist)

    def process_histograms(self, type = 'intensity'):
        for image in self.images:
            self.images[image][f'{type}_histogram'] = self.calculate_histogram(self.images[image][f'{type}_representation'], type)
        
    def caclulate_distance(self, image1, image2, type = 'intensity'):
        im1  = image1[f'{type}_histogram'] / image1['resolution']
        im2  = image2[f'{type}_histogram'] / image2['resolution']
        return np.sum(np.abs(im1 - im2))
    
    def process_image_distances(self, chosen_image, type = 'intensity'):
        image_distances = []
        for image in self.images:
            if chosen_image != image:
                distance_info = {
                    'name': image,
                    'path': self.images[image]['path'],
                    'distance': self.caclulate_distance(self.images[chosen_image], self.images[image], type)
                }
                image_distances.append(distance_info)
        image_distances.sort(key = lambda x: x['distance'])
        
        # for i in image_distances[:21]:
        #     print(i['name'])
        return image_distances



# X = ImageProcessor()
# X.process_image_distances(1, type='color_code')
