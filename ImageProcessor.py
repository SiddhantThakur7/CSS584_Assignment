import cv2
import numpy as np
import multiprocessing as mp
import json
import os

N = mp.cpu_count()


def binary_of(x, bits=8):
    return format(x, f"0{bits}b")


def int_of(x):
    return int(x, 2)


COLOR_CODE = "color_code"
INTENSITY = "intensity"
CACHE_PATH = ".\\cache\\representations.json"


class ImageProcessor:
    def __init__(self) -> None:
        self.images = {}
        self.methods = {"Color": COLOR_CODE, "Intensity": INTENSITY}
        self.INTENSITY_COEFFICIENT_MATRIX = np.array([[0.114], [0.587], [0.299]])
        self.default_image_list = []

        self.initialize()

    def initialize(self):
        cache_data = self.load_cache_data()
        if cache_data:
            self.images = cache_data
        else:
            with mp.Pool(processes=N) as p:
                results = p.map(self.intialize_image_data, [x for x in range(1, 101)])
            for idx, val in enumerate(results):
                self.images[idx + 1] = val[idx + 1]
            self.process_histograms("intensity")
            self.process_histograms("color_code")
            self.write_to_cache(self.images)

        self.default_image_list = list(self.images.values())

    def intialize_image_data(self, i):
        image_info = {}
        filepath = f".\\images\\png\\{i}.png"
        image = cv2.imread(filepath, cv2.IMREAD_COLOR)
        resolution_x = len(image)
        resolution_y = len(image[0])
        image_info[i] = {
            "name": i,
            "representation": image,
            "resolution_x": resolution_x,
            "resolution_y": resolution_y,
            "resolution": resolution_x * resolution_y,
            "color_code_representation": self.get_color_code_representaion(
                image, resolution_x, resolution_y
            ),
            "intensity_representation": np.transpose(
                np.dot(image, self.INTENSITY_COEFFICIENT_MATRIX)
            )[0],
            "path": filepath,
        }
        return image_info

    def load_cache_data(self):
        if not os.path.exists(CACHE_PATH):
            return

        cache_data = json.load(open(CACHE_PATH, "r"))
        return self.deserialize_image_data(cache_data)

    def write_to_cache(self, data):
        json.dump(self.serialize_image_data(data), open(CACHE_PATH, "w+"))

    def serialize_image_data(self, images):
        data = {}
        for image in images:
            data[image] = {}
            data[image]["name"] = images[image]["name"]
            data[image]["resolution"] = images[image]["resolution"]
            data[image]["path"] = images[image]["path"]
            data[image]["intensity_histogram"] = images[image][
                "intensity_histogram"
            ].tolist()
            data[image]["color_code_histogram"] = images[image][
                "color_code_histogram"
            ].tolist()
        return data

    def deserialize_image_data(self, images):
        data = images
        for image in images:
            data[image]["intensity_histogram"] = np.array(
                images[image]["intensity_histogram"]
            )
            data[image]["color_code_histogram"] = np.array(
                images[image]["color_code_histogram"]
            )
        return data

    def get_color_code_representaion(self, image, m, n):
        color_code_array = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                significant_bits = ""
                for k in reversed(range(3)):
                    significant_bits += binary_of(image[i][j][k])[:2]
                color_code_array[i][j] = int_of(significant_bits)
        return color_code_array

    def calculate_histogram(self, representation, type="intensity"):
        hist = [0] * (25 if type == "intensity" else 64)
        for i in range(len(representation)):
            for j in range(len(representation[0])):
                x = (
                    int(representation[i][j] // 10)
                    if type == "intensity"
                    else representation[i][j]
                )
                if type == "intensity" and x > 24.0:
                    x = 24
                hist[x] += 1
        return np.array(hist)

    def process_histograms(self, type="intensity"):
        for image in self.images:
            self.images[image][f"{type}_histogram"] = self.calculate_histogram(
                self.images[image][f"{type}_representation"], type
            )

    def caclulate_distance(self, image1, image2, type="intensity"):
        im1 = image1[f"{type}_histogram"] / image1["resolution"]
        im2 = image2[f"{type}_histogram"] / image2["resolution"]
        return np.sum(np.abs(im1 - im2))

    def process_image_distances(self, chosen_image, type="intensity"):
        image_distances = []
        for image in self.images:
            if chosen_image != image:
                distance_info = {
                    "name": image,
                    "path": self.images[image]["path"],
                    "distance": self.caclulate_distance(
                        self.images[chosen_image], self.images[image], type
                    ),
                }
                image_distances.append(distance_info)
        return image_distances

    def retrieve_similar_images(self, chosen_image, method_label):
        method = self.methods[method_label]
        distances = self.process_image_distances(chosen_image, method)
        distances.sort(key=lambda x: x["distance"])
        return distances
