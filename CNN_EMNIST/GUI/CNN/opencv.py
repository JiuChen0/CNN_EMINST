
import cv2
import numpy as np

def Images_Processing(base_dir,dst_dir):

    min_val = 10
    min_range = 30
    def extract_peek(array_vals, minimun_val, minimun_range):
        start_i = None
        end_i = None
        peek_ranges = []
        for i, val in enumerate(array_vals):
            if val > minimun_val and start_i is None:
                start_i = i
                print(val)
            elif val > minimun_val and start_i is not None:
                pass
            elif val < minimun_val and start_i is not None:
                if i - start_i >= minimun_range:
                    end_i = i
                    print(end_i - start_i)
                    peek_ranges.append((start_i, end_i))
                    start_i = None
                    end_i = None
            elif val < minimun_val and start_i is None:
                pass
            else:
                raise ValueError("ERROR")
        return peek_ranges

    def cutImage(img, peek_range):
        count = 0
        for i, peek_range in enumerate(peek_ranges):
            for vertical_range in vertical_peek_ranges2d[i]:
                x = vertical_range[0]
                y = peek_range[0]
                w = vertical_range[1] - x
                h = peek_range[1] - y
                pt1 = (x, y)
                pt2 = (x + w, y + h)
                cv2.rectangle(img, pt1, pt2, 255)
                cv2.imshow('fff',img)
                count += 1
                img1 = img[y-8:peek_range[1]+10, x-9:vertical_range[1]+7]
                new_shape = (28, 28)
                img1 = cv2.resize(img1, new_shape)
                cv2.imwrite(dst_dir + str(count) + ".png", img1)

        return count

    if base_dir == 'c:/origin/':
        fileName = '1.png'
        img = cv2.imread(base_dir + fileName)
    else:
        img = cv2.imread(base_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11,2)
    horizontal_sum = np.sum(adaptive_threshold, axis=1)
    peek_ranges = extract_peek(horizontal_sum, min_val, min_range)
    line_seg_adaptive_threshold = np.copy(adaptive_threshold)
    for i, peek_range in enumerate(peek_ranges):
        x = 0
        y = peek_range[0]
        w = line_seg_adaptive_threshold.shape[1]
        h = peek_range[1] - y
        pt1 = (x, y)
        pt2 = (x + w, y + h)
        cv2.rectangle(line_seg_adaptive_threshold, pt1, pt2, 255)
       # cv2.imshow('fff',line_seg_adaptive_threshold)
    vertical_peek_ranges2d = []
    for peek_range in peek_ranges:
        start_y = peek_range[0]
        end_y = peek_range[1]
        line_img = adaptive_threshold[start_y:end_y, :]
       # cv2.imshow('aaa',line_img)
        vertical_sum = np.sum(line_img, axis=0)
        vertical_peek_ranges = extract_peek(vertical_sum, min_val, min_range)
        vertical_peek_ranges2d.append(vertical_peek_ranges)
    count = cutImage(img, peek_range)
    return count




