import cv2
import numpy as np


def find_lane_lines(img):
    """
    Detecting road markings
    This function will take a color image, in BGR color system,
    Returns a filtered image of road markings
    """

    # Convert to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian filter to remove noise
    # You can experiment with other filters here.
    img_gauss = cv2.GaussianBlur(gray, (11, 11), 0)

    # Apply Canny edge detection
    thresh_low = 100
    thresh_high = 150
    img_canny = cv2.Canny(img_gauss, thresh_low, thresh_high)

    # Return image
    return img_canny


def birdview_transform(img):
    """Apply bird-view transform to the image
    """
    IMAGE_H = 480
    IMAGE_W = 640
    src = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, IMAGE_H // 3], [IMAGE_W, IMAGE_H // 3]])
    # dst = src
    dst = np.float32([[120, IMAGE_H], [IMAGE_W - 120, IMAGE_H], [0, 0], [IMAGE_W , 0]])
    # dst = np.float32([[0, IMAGE_H], [IMAGE_W, IMAGE_H], [0, 0], [IMAGE_W , 0]])
    
    # dst = np.float32([[50, IMAGE_H], [IMAGE_W - 50, IMAGE_H], [200, IMAGE_H // 2], [IMAGE_W - 200, IMAGE_H // 2]])
    M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
    warped_img = cv2.warpPerspective(img, M, (IMAGE_W, IMAGE_H)) # Image warping
    return warped_img
def find_left_right_rotate(image, draw=None):
    im_height, im_width = image.shape[:2]
    # Consider the position 70% from the top of the image
    interested_line_y = int(im_height * 0.1)
    if draw is not None:
        cv2.line(draw, (0, interested_line_y),
                 (im_width, interested_line_y), (0, 0, 255), 2)
    interested_line = image[interested_line_y, :]
    # Detect left/right points
    left_point = -1
    right_point = -1
    lane_width = 1000
    center = im_width // 2 
    # Traverse the two sides, find the first non-zero value pixels, and
    # consider them as the position of the left and right lines
    for x in range(center, 0, -1):

        # print(interested_line[x])
        if interested_line[x] > 0:
            left_point = x
            break
    for x in range(center + 1, im_width):
        # print(interested_line[x])
        if interested_line[x] > 0:
            right_point = x
            break

    # Predict right point when only see the left point
    if left_point != -1 and right_point == -1:
        right_point = left_point + lane_width
    # Predict left point when only see the right point
    if right_point != -1 and left_point == -1:
        left_point = right_point - lane_width
    # Draw two points on the image
    if draw is not None:
        if left_point != -1:
            draw = cv2.circle(
                draw, (left_point, interested_line_y), 6, (255, 255, 0), -1)
        if right_point != -1:
            draw = cv2.circle(
                draw, (right_point, interested_line_y), 6, (0, 255, 0), -1)
        if (left_point != -1 and right_point != -1):
            draw = cv2.circle(draw, (int((right_point + left_point) /2), interested_line_y), 50, (0, 128, 128), -1)
    return left_point, right_point
def find_left_right_points(image, draw=None):
    """Find left and right points of lane
    """

    im_height, im_width = image.shape[:2]
    # Consider the position 70% from the top of the image
    interested_line_y = int(im_height * 0.995)
    if draw is not None:
        cv2.line(draw, (0, interested_line_y),
                 (im_width, interested_line_y), (0, 0, 255), 2)
    interested_line = image[interested_line_y, :]
    # Detect left/right points
    left_point = -1
    right_point = -1
    lane_width = 1000
    center = im_width // 2
    # Traverse the two sides, find the first non-zero value pixels, and
    # consider them as the position of the left and right lines
    for x in range(center, 0, -1):

        # print(interested_line[x])
        if interested_line[x] > 0:
            left_point = x
            break
    for x in range(center + 1, im_width):
        # print(interested_line[x])
        if interested_line[x] > 0:
            right_point = x
            break

    # Predict right point when only see the left point
    if left_point != -1 and right_point == -1:
        right_point = left_point + lane_width
    # Predict left point when only see the right point
    if right_point != -1 and left_point == -1:
        left_point = right_point - lane_width
    # Draw two points on the image
    if draw is not None:
        cv2.line(draw,(center,interested_line_y),(center,im_height),(0, 255, 0),2)
        cv2.line(draw,(int((right_point + left_point) /2), interested_line_y),(center,im_height),(0, 255, 0),2)
        if left_point != -1:
            draw = cv2.circle(
                draw, (left_point, interested_line_y), 8, (255, 255, 0), -1)
        if right_point != -1:
            draw = cv2.circle(
                draw, (right_point, interested_line_y), 8, (0, 255, 0), -1)
        if (left_point != -1 and right_point != -1):
            draw = cv2.circle(draw, (int((right_point + left_point) /2), interested_line_y), 10, (0, 128, 128), -1)

    return left_point, right_point

def calculate_control_signal(img, draw=None):
    """Calculate speed and steering angle
    """
    steering_angle = 0
    # Find left/right points
    img_lines = find_lane_lines(img)
    img_birdview = birdview_transform(img_lines)
    draw[:, :] = birdview_transform(draw)
    left_point, right_point = find_left_right_points(img_birdview, draw=draw)
    # left_point_rotate, right_point_rotate = find_left_right_rotate(img_birdview,draw=draw)

    # Calculate speed and steering angle
    # The speed is fixed to 50% of the max speed
    # You can try to calculate speed from turning angle
    array = [[0.7,0.009],[0.9,0.008]]

    throttle = array[1][0] # Tốc độ của xe
    
    im_center = img.shape[1] // 2

    if left_point != -1 and right_point != -1:

        # Calculate the deviation
        center_point = (right_point + left_point) // 2
        center_diff =  im_center - center_point

        # Calculate steering angle
        # You can apply some advanced control algorithm here
        # For examples, PID
        # print(center_diff)
        steering_angle = - float(center_diff * array[1][1])

    # Nếu rẽ thì giảm tốc độ
    # print(steering_angle)
    center_interested_line_two = (left_point+right_point)/2
    # center_interested_line_one = (left_point_rotate+right_point_rotate)/2
    # print("a")
    # print(abs(center_interested_line_one)-5)
    # print(center_interested_line_two)
    # print("b")
    # if (abs(center_interested_line_one) +5 < center_interested_line_two or abs(center_interested_line_one) -5 > center_interested_line_two):
        # throttle = 0.6
        # print("Sắp rẽ")
    return throttle, steering_angle
