import numpy as np
import cv2


class Image:

    LOWER_BLUE = np.array([85, 12, 0], np.uint8)
    UPPER_BLUE = np.array([140, 255, 255], np.uint8)
    LOWER_GREY = np.array([0, 0, 178], np.uint8)
    UPPER_GREY = np.array([255, 51, 252], np.uint8)

    def __init__(self, image_path):
        self.image_path = image_path
        self.img = cv2.imread(image_path)
        self.total_pixels = self.img.size / self.img.ndim
        self.hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        self.blue_pixels = cv2.inRange(self.hsv, self.LOWER_BLUE, self.UPPER_BLUE)
        self.blue_pixels_count = cv2.countNonZero(self.blue_pixels)
        self.blue_fraction = self.blue_pixels_count / self.total_pixels
        self.grey_pixels = cv2.inRange(self.hsv, self.LOWER_GREY, self.UPPER_GREY)
        self.grey_pixels_count = cv2.countNonZero(self.grey_pixels)
        self.grey_fraction = self.grey_pixels_count / self.total_pixels
        self.saturation = self.hsv[:, :, 1].ravel().mean() / 255
        self.brightness = self.hsv[:, :, 2].ravel().mean() / 255

    def blue_measure(self):
        masked_image = cv2.bitwise_and(self.hsv[:, :, 2], self.blue_pixels)
        return 1.05 - ((self.blue_pixels_count() + 1) / (self.hsv.size / self.hsv.ndim)) * (masked_image.sum() / 1.5)

    def grey_measure(self):
        masked_image = cv2.bitwise_and(self.hsv[:, :, 2], self.grey_pixels)
        return masked_image.sum()

    def okta(self):
        pass
