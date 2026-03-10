"""
Marker Detector — Computer Vision Recruitment Task

Implement the MarkerDetector class and the utility functions below.
See README.md for full task description.
"""

import cv2
import numpy as np

class MarkerDetector:
    def __init__(self):
        
        self.min_area = 100 
        

        self.COLOR_RANGES = {
            "red": [
                (np.array([0, 100, 100]), np.array([10, 255, 255])),
                (np.array([160, 100, 100]), np.array([179, 255, 255]))
            ],
            "green": [
                (np.array([40, 100, 100]), np.array([80, 255, 255]))
            ],
            "blue": [
                (np.array([100, 100, 100]), np.array([140, 255, 255]))
            ],
            "yellow": [
                (np.array([20, 100, 100]), np.array([35, 255, 255]))
            ]
        }

    def detect(self, image: np.ndarray):
    
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        detections = []

        for color_name, ranges in self.COLOR_RANGES.items():
            mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
            
        
            for lower, upper in ranges:
                color_mask = cv2.inRange(hsv, lower, upper)
                mask = cv2.bitwise_or(mask, color_mask)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                area = cv2.contourArea(cnt)

                if area > self.min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    cx = int(x + w / 2)
                    cy = int(y + h / 2)
                    

                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
                    vertices = len(approx)
                    
                    shape = "circle"
                    if vertices == 3:
                        shape = "triangle"
                    elif vertices == 4:
                        shape = "rectangle"
                    
                    detections.append({
                        "color": color_name,
                        "bbox": (x, y, w, h),
                        "center": (cx, cy),
                        "area": area,
                        "shape": shape
                    })
                    
        return detections

def compute_iou(box_a, box_b):
    xa, ya, wa, ha = box_a
    xb, yb, wb, hb = box_b
    
    inter_x1 = max(xa, xb)
    inter_y1 = max(ya, yb)
    inter_x2 = min(xa + wa, xb + wb)
    inter_y2 = min(ya + ha, yb + hb)
    
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    
    if inter_area == 0:
        return 0.0
        
    area_a = wa * ha
    area_b = wb * hb
    
    iou = inter_area / float(area_a + area_b - inter_area)
    return iou

def filter_detections(detections, iou_threshold):
    sorted_detections = sorted(detections, key=lambda d: d['area'], reverse=True)
    kept_detections = []
    
    for current_det in sorted_detections:
        should_keep = True
        
        for kept_det in kept_detections:
            iou = compute_iou(current_det['bbox'], kept_det['bbox'])
            if iou > iou_threshold:
                should_keep = False
                break
                
        if should_keep:
            kept_detections.append(current_det)
            
    return kept_detections
