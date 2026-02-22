import cv2
import numpy as np

class ColorConfig:
    
    EXTRACTION_COLORS = {
        'green': {
            'display_name': 'Green',
            'button_color': '#4CAF50',
            'hsv_lower_bound': np.array([35, 20, 20]),
            'hsv_upper_bound': np.array([85, 255, 255])
        },
        'purple': {
            'display_name': 'Purple',
            'button_color': '#673AB7', 
            'hsv_lower_bound': np.array([120, 15, 30]),
            'hsv_upper_bound': np.array([180, 255, 255])
        },
        'blue': {
            'display_name': 'Blue',
            'button_color': '#2196F3',
            'hsv_lower_bound': np.array([100, 50, 50]),
            'hsv_upper_bound': np.array([130, 255, 255])
        },
        'black': {
            'display_name': 'Black',
            'button_color': '#333333',
            'hsv_lower_bound': np.array([0, 0, 0]),
            'hsv_upper_bound': np.array([180, 255, 50])
        },
        'yellow': {
            'display_name': 'Yellow',
            'button_color': '#FFEB3B',
            'hsv_lower_bound': np.array([15, 30, 40]),
            'hsv_upper_bound': np.array([45, 255, 255])
        },
        'red': {
            'display_name': 'Red',
            'button_color': '#f44336',
            'hsv_lower_bound': np.array([0, 80, 80]),
            'hsv_upper_bound': np.array([12, 255, 255]),
            'hsv_lower_bound_2': np.array([168, 80, 80]),
            'hsv_upper_bound_2': np.array([180, 255, 255])
        },
        'white': {
            'display_name': 'White/Cream',
            'button_color': '#FAFAFA',
            'hsv_lower_bound': np.array([0, 0, 180]),
            'hsv_upper_bound': np.array([180, 40, 255])
        }
    }
    
    COLOR_FILTERS = {
        'red': {
            'display_name': 'Red Filter',
            'button_color': '#f44336',
            'blue_multiplier': 0.6,
            'green_multiplier': 0.6,
            'red_multiplier': 1.5
        },
        'yellow': {
            'display_name': 'Yellow Filter', 
            'button_color': '#FFEB3B',
            'blue_multiplier': 0.5,
            'green_multiplier': 1.3,
            'red_multiplier': 1.3
        },
        'gray': {
            'display_name': 'Grayscale Filter',
            'button_color': '#9E9E9E',
            'type': 'grayscale'
        },
        'blue': {
            'display_name': 'Blue Filter',
            'button_color': '#1565C0',
            'blue_multiplier': 1.8,
            'green_multiplier': 0.6,
            'red_multiplier': 0.5
        },
        'purple': {
            'display_name': 'Purple Filter',
            'button_color': '#673AB7',
            'blue_multiplier': 1.5,
            'green_multiplier': 0.6,
            'red_multiplier': 1.4
        }
    }
    
    MORPH_KERNEL_SIZE = (3, 3)
    GRAY_BACKGROUND_COLOR = (128, 128, 128)

def extract_color(image, hsv_image, color_key):
    if color_key not in ColorConfig.EXTRACTION_COLORS:
        raise ValueError(f"Invalid color key: {color_key}")
    
    color_info = ColorConfig.EXTRACTION_COLORS[color_key]
    
    lower_hsv = color_info['hsv_lower_bound']
    upper_hsv = color_info['hsv_upper_bound']
    
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    
    if 'hsv_lower_bound_2' in color_info and 'hsv_upper_bound_2' in color_info:
        lower_hsv_2 = color_info['hsv_lower_bound_2']
        upper_hsv_2 = color_info['hsv_upper_bound_2']
        mask2 = cv2.inRange(hsv_image, lower_hsv_2, upper_hsv_2)
        mask = cv2.bitwise_or(mask, mask2)
    
    mask = clean_mask(mask)
    
    result_image = apply_color_extraction_effect(image, mask)
    
    return result_image, color_info['display_name']

def clean_mask(mask):
    kernel = np.ones(ColorConfig.MORPH_KERNEL_SIZE, np.uint8)
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return mask

def apply_color_extraction_effect(image, mask):
    gray_background = np.full_like(image, ColorConfig.GRAY_BACKGROUND_COLOR, dtype=np.uint8)
    
    result_image = image.copy()
    
    mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_normalized = mask_3channel.astype(float) / 255
    
    result_image = (result_image * mask_normalized + 
                   gray_background * (1 - mask_normalized)).astype(np.uint8)
    
    return result_image
def apply_color_filter(image, filter_key):
    if filter_key not in ColorConfig.COLOR_FILTERS:
        raise ValueError(f"Invalid filter key: {filter_key}")
    
    filter_info = ColorConfig.COLOR_FILTERS[filter_key]
    
    if filter_key == 'gray':
        result_image = apply_grayscale_filter(image)
    else:
        result_image = apply_color_channel_filter(image, filter_info)
    
    return result_image, filter_info['display_name']

def apply_grayscale_filter(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    result_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    return result_image

def apply_color_channel_filter(image, filter_info):
    result_image = image.astype(np.float32)
    
    result_image[:, :, 0] *= filter_info['blue_multiplier']
    result_image[:, :, 1] *= filter_info['green_multiplier']
    result_image[:, :, 2] *= filter_info['red_multiplier']
    
    result_image = np.clip(result_image, 0, 255).astype(np.uint8)
    
    return result_image

def get_extraction_colors():
    return ColorConfig.EXTRACTION_COLORS

def get_color_filters():
    return ColorConfig.COLOR_FILTERS

def validate_color_key(color_key, color_type='extraction'):
    if color_type == 'extraction':
        return color_key in ColorConfig.EXTRACTION_COLORS
    elif color_type == 'filter':
        return color_key in ColorConfig.COLOR_FILTERS
    else:
        return False
