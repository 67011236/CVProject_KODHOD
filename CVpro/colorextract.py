# ============================================================================
#                           COLOR EXTRACTION MODULE
# ============================================================================
# This module contains all color processing functions for the GUI application
# Easy to modify color ranges, filters, and processing parameters
# ============================================================================

import cv2
import numpy as np

# ============================================================================
#                           COLOR CONFIGURATION
# ============================================================================

class ColorConfig:
    """Configuration class for all color processing parameters"""
    
    # HSV color ranges for extraction (easy to modify)
    EXTRACTION_COLORS = {
        'green': {
            'display_name': 'Green',
            'button_color': '#4CAF50',
            'hsv_lower_bound': np.array([35, 20, 20]),   # ขยายช่วงเพื่อจับสีเขียวทุกเฉด (อ่อน-เข้ม)
            'hsv_upper_bound': np.array([85, 255, 255])  # รวมเขียวเหลือง เขียวน้ำเงิน
        },
        'purple': {
            'display_name': 'Purple',
            'button_color': '#673AB7', 
            'hsv_lower_bound': np.array([120, 15, 30]),  # Broader range to include background purple tones
            'hsv_upper_bound': np.array([180, 255, 255]) # Extended to capture all purple/violet background areas
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
            'hsv_lower_bound': np.array([15, 30, 40]),     # Broader range for golden background areas
            'hsv_upper_bound': np.array([45, 255, 255])    # Extended to capture all gold/yellow background tones
        },
        'red': {
            'display_name': 'Red',
            'button_color': '#f44336',
            'hsv_lower_bound': np.array([0, 80, 80]),      # Higher saturation/value for bright flames only
            'hsv_upper_bound': np.array([12, 255, 255]),   # Narrower hue range for fire/candles
            'hsv_lower_bound_2': np.array([168, 80, 80]),  # Higher threshold to avoid ground reds
            'hsv_upper_bound_2': np.array([180, 255, 255]) # Upper red range end
        },
        'white': {
            'display_name': 'White/Cream',
            'button_color': '#FAFAFA',
            'hsv_lower_bound': np.array([0, 0, 180]),      # Lower brightness to catch cream tones in clothes
            'hsv_upper_bound': np.array([180, 40, 255])    # Slightly higher saturation for fabric textures
        }
    }
    
    # Color filter settings for image tinting
    COLOR_FILTERS = {
        'red': {
            'display_name': 'Red Filter',
            'button_color': '#f44336',
            'blue_multiplier': 0.6,    # Reduce blue channel
            'green_multiplier': 0.6,   # Reduce green channel  
            'red_multiplier': 1.5      # Enhance red channel
        },
        'yellow': {
            'display_name': 'Yellow Filter', 
            'button_color': '#FFEB3B',
            'blue_multiplier': 0.5,    # Reduce blue significantly
            'green_multiplier': 1.3,   # Enhance green
            'red_multiplier': 1.3      # Enhance red
        },
        'gray': {
            'display_name': 'Grayscale Filter',
            'button_color': '#9E9E9E',
            'type': 'grayscale'        # Special grayscale conversion
        },
        'blue': {
            'display_name': 'Blue Filter',
            'button_color': '#1565C0',
            'blue_multiplier': 1.8,    # Enhance blue channel
            'green_multiplier': 0.6,   # Reduce green
            'red_multiplier': 0.5      # Reduce red
        },
        'purple': {
            'display_name': 'Purple Filter',
            'button_color': '#673AB7',
            'blue_multiplier': 1.5,    # Enhance blue channel
            'green_multiplier': 0.6,   # Reduce green
            'red_multiplier': 1.4      # Enhance red to create purple
        }
    }
    
    # Morphological operation settings
    MORPH_KERNEL_SIZE = (3, 3)  # Kernel size for noise reduction
    GRAY_BACKGROUND_COLOR = (128, 128, 128)  # RGB values for gray background

# ============================================================================
#                           EXTRACTION FUNCTIONS  
# ============================================================================

def extract_color(image, hsv_image, color_key):
    """
    Extract a specific color from image and make everything else gray
    
    Args:
        image (numpy.ndarray): Original BGR image
        hsv_image (numpy.ndarray): HSV version of the image
        color_key (str): Color to extract ('green', 'purple', 'blue')
    
    Returns:
        numpy.ndarray: Processed image with extracted color, rest gray
        str: Display name of the extracted color
    
    Raises:
        ValueError: If color_key is not valid
    """
    if color_key not in ColorConfig.EXTRACTION_COLORS:
        raise ValueError(f"Invalid color key: {color_key}")
    
    color_info = ColorConfig.EXTRACTION_COLORS[color_key]
    
    # Create mask for the selected color using HSV thresholds
    lower_hsv = color_info['hsv_lower_bound']
    upper_hsv = color_info['hsv_upper_bound']
    
    # Generate color mask
    mask = cv2.inRange(hsv_image, lower_hsv, upper_hsv)
    
    # Special handling for red color (which wraps around HSV hue spectrum)
    if 'hsv_lower_bound_2' in color_info and 'hsv_upper_bound_2' in color_info:
        lower_hsv_2 = color_info['hsv_lower_bound_2']
        upper_hsv_2 = color_info['hsv_upper_bound_2']
        mask2 = cv2.inRange(hsv_image, lower_hsv_2, upper_hsv_2)
        mask = cv2.bitwise_or(mask, mask2)
    
    # Clean up the mask using morphological operations
    mask = clean_mask(mask)
    
    # Create result image with gray background
    result_image = apply_color_extraction_effect(image, mask)
    
    return result_image, color_info['display_name']

def clean_mask(mask):
    """
    Apply morphological operations to clean up the color mask
    
    Args:
        mask (numpy.ndarray): Binary mask from color range detection
        
    Returns:
        numpy.ndarray: Cleaned binary mask
    """
    # Create morphological kernel
    kernel = np.ones(ColorConfig.MORPH_KERNEL_SIZE, np.uint8)
    
    # Close gaps in the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Remove small noise
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    return mask

def apply_color_extraction_effect(image, mask):
    """
    Apply the color extraction effect: keep original where mask is white, gray elsewhere
    
    Args:
        image (numpy.ndarray): Original BGR image
        mask (numpy.ndarray): Binary mask indicating where to keep color
        
    Returns:
        numpy.ndarray: Result image with color extraction applied
    """
    # Create gray background
    gray_background = np.full_like(image, ColorConfig.GRAY_BACKGROUND_COLOR, dtype=np.uint8)
    
    # Create the result image
    result_image = image.copy()
    
    # Convert mask to 3-channel for blending
    mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_normalized = mask_3channel.astype(float) / 255
    
    # Apply the effect: keep original where mask is white, use gray where mask is black
    result_image = (result_image * mask_normalized + 
                   gray_background * (1 - mask_normalized)).astype(np.uint8)
    
    return result_image

# ============================================================================
#                           FILTER FUNCTIONS
# ============================================================================

def apply_color_filter(image, filter_key):
    """
    Apply a color filter to the entire image
    
    Args:
        image (numpy.ndarray): Original BGR image
        filter_key (str): Filter to apply ('red', 'yellow', 'gray')
    
    Returns:
        numpy.ndarray: Filtered image
        str: Display name of the applied filter
    
    Raises:
        ValueError: If filter_key is not valid
    """
    if filter_key not in ColorConfig.COLOR_FILTERS:
        raise ValueError(f"Invalid filter key: {filter_key}")
    
    filter_info = ColorConfig.COLOR_FILTERS[filter_key]
    
    if filter_key == 'gray':
        # Special case: grayscale conversion
        result_image = apply_grayscale_filter(image)
    else:
        # Apply color channel adjustments
        result_image = apply_color_channel_filter(image, filter_info)
    
    return result_image, filter_info['display_name']

def apply_grayscale_filter(image):
    """
    Convert image to grayscale
    
    Args:
        image (numpy.ndarray): Original BGR image
        
    Returns:
        numpy.ndarray: Grayscale image converted back to 3-channel BGR
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Convert back to 3-channel for consistency
    result_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    
    return result_image

def apply_color_channel_filter(image, filter_info):
    """
    Apply color channel multipliers to create color tints
    
    Args:
        image (numpy.ndarray): Original BGR image
        filter_info (dict): Filter configuration with channel multipliers
        
    Returns:
        numpy.ndarray: Color-filtered image
    """
    # Work with float32 for precision during calculations
    result_image = image.astype(np.float32)
    
    # Apply channel-specific multipliers (OpenCV uses BGR format)
    result_image[:, :, 0] *= filter_info['blue_multiplier']   # Blue channel
    result_image[:, :, 1] *= filter_info['green_multiplier']  # Green channel  
    result_image[:, :, 2] *= filter_info['red_multiplier']    # Red channel
    
    # Clip values to valid range and convert back to uint8
    result_image = np.clip(result_image, 0, 255).astype(np.uint8)
    
    return result_image

# ============================================================================
#                           UTILITY FUNCTIONS
# ============================================================================

def get_extraction_colors():
    """
    Get the available color extraction options
    
    Returns:
        dict: Dictionary of extraction color configurations
    """
    return ColorConfig.EXTRACTION_COLORS

def get_color_filters():
    """
    Get the available color filter options
    
    Returns:
        dict: Dictionary of color filter configurations  
    """
    return ColorConfig.COLOR_FILTERS

def validate_color_key(color_key, color_type='extraction'):
    """
    Validate if a color key exists in the configuration
    
    Args:
        color_key (str): Key to validate
        color_type (str): Type of color operation ('extraction' or 'filter')
        
    Returns:
        bool: True if valid, False otherwise
    """
    if color_type == 'extraction':
        return color_key in ColorConfig.EXTRACTION_COLORS
    elif color_type == 'filter':
        return color_key in ColorConfig.COLOR_FILTERS
    else:
        return False

# ============================================================================
#                           EASY CONFIGURATION MODIFICATION
# ============================================================================
"""
TO MODIFY COLOR EXTRACTION RANGES:

1. Adjust HSV values in ColorConfig.EXTRACTION_COLORS
   - hsv_lower_bound: Lower threshold [Hue, Saturation, Value]
   - hsv_upper_bound: Upper threshold [Hue, Saturation, Value]
   
2. HSV ranges:
   - Hue: 0-179 (color)
   - Saturation: 0-255 (color intensity) 
   - Value: 0-255 (brightness)

TO MODIFY COLOR FILTERS:

1. Adjust multipliers in ColorConfig.COLOR_FILTERS
   - Values > 1.0: Enhance that color channel
   - Values < 1.0: Reduce that color channel
   
2. Add new filters by adding entries to COLOR_FILTERS dictionary

TO MODIFY PROCESSING PARAMETERS:

1. MORPH_KERNEL_SIZE: Change (3,3) to larger values for more aggressive noise removal
2. GRAY_BACKGROUND_COLOR: Change (128,128,128) for different gray shade
"""
