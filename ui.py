# ============================================================================
#                           COLOR EXTRACTION GUI APPLICATION
# ============================================================================
# This application provides a GUI for:
# 1. Extracting specific colors (Green, Purple, Blue) from images
# 2. Applying color filters (Red, Yellow, Grayscale) to images  
# 3. Working with multiple images and switching between them
# ============================================================================

import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class ColorExtractionUI:
    """
    Main GUI class for Color Extraction Program
    
    Features:
    - Multi-image support (switch between 2 images)
    - Color extraction (isolate specific colors, make rest gray)
    - Color filtering (apply color tints and effects)
    - Save processed results
    """
    def __init__(self):
        """Initialize the Color Extraction GUI application"""
        
        # ==================== IMAGE DATA VARIABLES ====================
        self.current_image = None           # Currently displayed image (BGR format)
        self.original_image = None          # Original loaded image (BGR format)  
        self.hsv_image = None              # HSV version for color extraction
        self.result_image = None           # Processed result image
        self.image_paths = []              # List of available image paths
        self.current_image_index = 0       # Index of currently active image
        
        # ==================== COLOR EXTRACTION SETTINGS ====================
        # HSV color ranges for extracting specific colors from images
        self.extraction_colors = {
            'green': {
                'display_name': 'Green',
                'button_color': '#4CAF50',
                'hsv_lower_bound': np.array([40, 50, 50]),   # Lower HSV threshold
                'hsv_upper_bound': np.array([80, 255, 255])  # Upper HSV threshold
            },
            'purple': {
                'display_name': 'Purple',
                'button_color': '#9C27B0', 
                'hsv_lower_bound': np.array([120, 50, 50]),
                'hsv_upper_bound': np.array([160, 255, 255])
            },
            'blue': {
                'display_name': 'Blue',
                'button_color': '#2196F3',
                'hsv_lower_bound': np.array([100, 50, 50]),
                'hsv_upper_bound': np.array([130, 255, 255])
            }
        }
        
        # ==================== COLOR FILTER SETTINGS ====================
        # Color filters for applying tints and effects to entire image  
        self.color_filters = {
            'red': {
                'display_name': 'Red Filter',
                'button_color': '#f44336'
            },
            'yellow': {
                'display_name': 'Yellow Filter', 
                'button_color': '#FFEB3B'
            },
            'gray': {
                'display_name': 'Grayscale Filter',
                'button_color': '#9E9E9E'
            }
        }
        
        # ==================== GUI SETUP ====================
        self.setup_main_window()
        self.create_user_interface()
        
    # ============================================================================
    #                           GUI SETUP AND INITIALIZATION
    # ============================================================================
    
    def setup_main_window(self):
        """Configure the main application window"""
        self.root = tk.Tk()
        self.root.title("Color Extraction Program")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        self.root.resizable(True, True)
        
        # Configure visual style
        style = ttk.Style()
        style.theme_use('clam')
    
    def create_user_interface(self):
        """Build all GUI components in order"""
        self.create_title_section()
        self.create_image_selection_section()
        self.create_main_action_buttons()
        self.create_extraction_controls()
        self.create_filter_controls()
        self.create_results_display_area()
        self.create_status_and_progress_indicators()
    
    def create_title_section(self):
        """Create the main title at the top of the window"""
        title_container = tk.Frame(self.root, bg='#f0f0f0')
        title_container.pack(pady=20)
        
        main_title = tk.Label(title_container, text="🎨 Color Extraction Program", 
                             font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#333')
        main_title.pack()
    
    def create_image_selection_section(self):
        """Create image selection buttons and current image indicator"""
        # Container for image selection controls
        self.image_selection_container = tk.Frame(self.root, bg='#f0f0f0')
        self.image_selection_container.pack(pady=10)
        
        # Current image indicator label
        self.current_image_indicator = tk.Label(
            self.image_selection_container, 
            text="Current Image: Image 1", 
            font=('Arial', 14, 'bold'), 
            bg='#f0f0f0', 
            fg='#333'
        )
        self.current_image_indicator.pack()
        
        # Container for image switching buttons
        image_button_container = tk.Frame(self.image_selection_container, bg='#f0f0f0')
        image_button_container.pack(pady=5)
        
        # Image 1 button - starts active (blue)
        self.image1_button = tk.Button(
            image_button_container, 
            text="📷 Image 1",
            font=('Arial', 12, 'bold'), 
            bg='#2196F3',  # Active color 
            fg='white',
            width=10, 
            height=1, 
            relief='flat', 
            cursor='hand2',
            command=lambda: self.switch_to_image(0)
        )
        self.image1_button.pack(side=tk.LEFT, padx=5)
        
        # Image 2 button - starts inactive (gray)
        self.image2_button = tk.Button(
            image_button_container, 
            text="📷 Image 2",
            font=('Arial', 12, 'bold'), 
            bg='#757575',  # Inactive color
            fg='white',
            width=10, 
            height=1, 
            relief='flat', 
            cursor='hand2',
            command=lambda: self.switch_to_image(1)
        )
        self.image2_button.pack(side=tk.LEFT, padx=5)
    
    def create_main_action_buttons(self):
        """Create the main Extract Color and Change Color action buttons"""
        main_button_container = tk.Frame(self.root, bg='#f0f0f0')
        main_button_container.pack(pady=20)
        
        # Extract Color Button - Green color scheme
        self.extract_color_button = tk.Button(
            main_button_container, 
            text="🎯 Extract Color",
            font=('Arial', 16, 'bold'), 
            bg='#4CAF50',  # Green
            fg='white',
            width=15, 
            height=2, 
            relief='flat', 
            cursor='hand2',
            command=self.show_extraction_options
        )
        self.extract_color_button.pack(side=tk.LEFT, padx=10)
        
        # Change Color Button - Orange color scheme  
        self.change_color_button = tk.Button(
            main_button_container, 
            text="🔄 Change Color",
            font=('Arial', 16, 'bold'), 
            bg='#FF9800',  # Orange
            fg='white',
            width=15, 
            height=2, 
            relief='flat', 
            cursor='hand2',
            command=self.show_filter_options
        )
        self.change_color_button.pack(side=tk.LEFT, padx=10)
        
    def create_extraction_controls(self):
        """Create color extraction selection interface (initially hidden)"""
        # Main container for extraction controls
        self.extraction_controls_container = tk.Frame(self.root, bg='#f0f0f0')
        
        # Section title
        extraction_title = tk.Label(
            self.extraction_controls_container, 
            text="Select a Color to Extract:", 
            font=('Arial', 16, 'bold'), 
            bg='#f0f0f0', 
            fg='#333'
        )
        extraction_title.pack(pady=10)
        
        # Container for extraction option buttons
        extraction_buttons_container = tk.Frame(self.extraction_controls_container, bg='#f0f0f0')
        extraction_buttons_container.pack()
        
        # Create a button for each extractable color
        for color_key, color_info in self.extraction_colors.items():
            extraction_button = tk.Button(
                extraction_buttons_container, 
                text=f"● {color_info['display_name']}", 
                font=('Arial', 14, 'bold'), 
                bg=color_info['button_color'], 
                fg='white',
                width=12, 
                height=2, 
                relief='flat', 
                cursor='hand2',
                command=lambda ck=color_key: self.perform_color_extraction(ck)
            )
            extraction_button.pack(side=tk.LEFT, padx=10)
        
        # Back button to return to main menu
        extraction_back_button = tk.Button(
            extraction_buttons_container, 
            text="← Back", 
            font=('Arial', 14, 'bold'), 
            bg='#757575', 
            fg='white',
            width=8, 
            height=2, 
            relief='flat', 
            cursor='hand2',
            command=self.hide_extraction_options
        )
        extraction_back_button.pack(side=tk.LEFT, padx=10)
    
    def create_filter_controls(self):
        """Create color filter selection interface (initially hidden)"""
        # Main container for filter controls
        self.filter_controls_container = tk.Frame(self.root, bg='#f0f0f0')
        
        # Section title
        filter_title = tk.Label(
            self.filter_controls_container, 
            text="Select a Color Filter:", 
            font=('Arial', 16, 'bold'), 
            bg='#f0f0f0', 
            fg='#333'
        )
        filter_title.pack(pady=10)
        
        # Container for filter option buttons
        filter_buttons_container = tk.Frame(self.filter_controls_container, bg='#f0f0f0')
        filter_buttons_container.pack()
        
        # Create a button for each available filter
        for filter_key, filter_info in self.color_filters.items():
            filter_button = tk.Button(
                filter_buttons_container, 
                text=f"🎨 {filter_info['display_name']}", 
                font=('Arial', 14, 'bold'), 
                bg=filter_info['button_color'], 
                fg='white',
                width=12, 
                height=2, 
                relief='flat', 
                cursor='hand2',
                command=lambda fk=filter_key: self.apply_color_filter(fk)
            )
            filter_button.pack(side=tk.LEFT, padx=10)
        
        # Back button to return to main menu
        filter_back_button = tk.Button(
            filter_buttons_container, 
            text="← Back", 
            font=('Arial', 14, 'bold'), 
            bg='#757575', 
            fg='white',
            width=8, 
            height=2, 
            relief='flat', 
            cursor='hand2',
            command=self.hide_filter_options
        )
        filter_back_button.pack(side=tk.LEFT, padx=10)
    
    def create_results_display_area(self):
        """Create the area where processed images will be displayed"""
        # This container will hold before/after image comparisons
        # It gets populated dynamically when processing is complete
        self.results_display_container = tk.Frame(self.root, bg='#f0f0f0')
    
    def create_status_and_progress_indicators(self):
        """Create status label and progress bar for user feedback"""
        # Status label - shows current operation status and results
        self.status_label = tk.Label(
            self.root, 
            text="Load an image to get started!", 
            font=('Arial', 12), 
            bg='#f0f0f0', 
            fg='#666'
        )
        self.status_label.pack(pady=10)
        
        # Progress bar - shown during processing operations
        self.progress_bar = ttk.Progressbar(
            self.root, 
            mode='indeterminate', 
            length=300
        )
    
    
    # ============================================================================
    #                           USER INTERFACE INTERACTIONS
    # ============================================================================
    
    def switch_to_image(self, image_index):
        """
        Switch between available images
        
        Args:
            image_index (int): Index of image to switch to (0 for Image 1, 1 for Image 2)
        """
        if image_index < len(self.image_paths):
            self.current_image_index = image_index
            self.load_current_image()
            
            # Update the current image indicator text
            self.current_image_indicator.config(text=f"Current Image: Image {image_index + 1}")
            
            # Update button appearance (active = blue, inactive = gray)
            if image_index == 0:
                self.image1_button.config(bg='#2196F3')  # Active - blue
                self.image2_button.config(bg='#757575')  # Inactive - gray
            else:
                self.image1_button.config(bg='#757575')  # Inactive - gray 
                self.image2_button.config(bg='#2196F3')  # Active - blue
            
            # Hide any open option panels and previous results
            self.hide_extraction_options()
            self.hide_filter_options()
    
    def show_extraction_options(self):
        """Display the color extraction option buttons"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Hide filter options if currently shown
        self.hide_filter_options()
        
        # Show extraction options
        self.extraction_controls_container.pack(pady=20)
    
    def hide_extraction_options(self):
        """Hide the color extraction option buttons"""
        self.extraction_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def show_filter_options(self):
        """Display the color filter option buttons"""
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return
            
        # Hide extraction options if currently shown
        self.hide_extraction_options()
        
        # Show filter options
        self.filter_controls_container.pack(pady=20)
    
    def hide_filter_options(self):
        """Hide the color filter option buttons"""
        self.filter_controls_container.pack_forget()
        self.results_display_container.pack_forget()
    
    def cv2_to_tk_image(self, cv2_image, max_width=400, max_height=300):
        """Convert OpenCV image to Tkinter PhotoImage for display in GUI"""
        # Convert BGR (OpenCV) to RGB (Tkinter/PIL)
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # Resize if image is too large for GUI display
        height, width = rgb_image.shape[:2]
        if width > max_width or height > max_height:
            scale = min(max_width/width, max_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Convert to PIL Image then to Tkinter PhotoImage
        pil_image = Image.fromarray(rgb_image)
        return ImageTk.PhotoImage(pil_image)
    
    def display_results(self, operation_name, is_filter=False):
        """Display the original and processed images in GUI"""
        self.results_display_container.pack_forget()  # Remove previous results
        self.results_display_container = tk.Frame(self.root, bg='#f0f0f0')
        self.results_display_container.pack(pady=20, fill='both', expand=True)
        
        # Results title
        operation_type = "Filter" if is_filter else "Extraction"
        results_title = tk.Label(self.results_display_container, 
                                text=f"✨ {operation_name} {operation_type} Results (Image {self.current_image_index + 1})", 
                                font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333')
        results_title.pack(pady=10)
        
        # Images container
        images_container = tk.Frame(self.results_display_container, bg='#f0f0f0')
        images_container.pack()
        
        # Original image
        original_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        original_frame.pack(side=tk.LEFT, padx=20)
        
        original_label = tk.Label(original_frame, text="Original Image", 
                                 font=('Arial', 12, 'bold'), bg='white', fg='#333')
        original_label.pack(pady=5)
        
        original_tk_image = self.cv2_to_tk_image(self.original_image)
        original_image_label = tk.Label(original_frame, image=original_tk_image, bg='white')
        original_image_label.image = original_tk_image  # Keep reference
        original_image_label.pack(padx=10, pady=10)
        
        # Result image
        result_frame = tk.Frame(images_container, bg='white', relief='solid', bd=2)
        result_frame.pack(side=tk.LEFT, padx=20)
        
        operation_type = "Filter Applied" if is_filter else "Extracted"
        result_label = tk.Label(result_frame, text=f"{operation_name} {operation_type}", 
                               font=('Arial', 12, 'bold'), bg='white', fg='#333')
        result_label.pack(pady=5)
        
        result_tk_image = self.cv2_to_tk_image(self.result_image)
        result_image_label = tk.Label(result_frame, image=result_tk_image, bg='white')
        result_image_label.image = result_tk_image  # Keep reference
        result_image_label.pack(padx=10, pady=10)
        
        # Action buttons
        action_frame = tk.Frame(self.results_display_container, bg='#f0f0f0')
        action_frame.pack(pady=20)
        
        save_btn = tk.Button(action_frame, text="💾 Save Result", 
                            font=('Arial', 12, 'bold'), bg='#2196F3', fg='white',
                            relief='flat', cursor='hand2', command=self.save_result)
        save_btn.pack(side=tk.LEFT, padx=10)
        
        new_operation_btn = tk.Button(action_frame, text="🔄 New Operation", 
                                      font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                                      relief='flat', cursor='hand2', 
                                      command=self.reset_for_new_operation)
        new_operation_btn.pack(side=tk.LEFT, padx=10)
        
        # Add image switching buttons in results
        if len(self.image_paths) > 1:
            switch_image_btn = tk.Button(action_frame, text=f"📷 Switch to Image {2 if self.current_image_index == 0 else 1}", 
                                        font=('Arial', 12, 'bold'), bg='#9C27B0', fg='white',
                                        relief='flat', cursor='hand2', 
                                        command=lambda: self.switch_to_image(1 - self.current_image_index))
            switch_image_btn.pack(side=tk.LEFT, padx=10)
        
        operation_type = "filter" if is_filter else "extraction"
        self.status_label.config(text=f"✅ {operation_name} {operation_type} completed successfully!", fg='#4CAF50')
    
    def apply_color_filter(self, filter_key):
        """Apply color filter to the image"""
        if filter_key not in self.color_filters:
            messagebox.showerror("Error", "Invalid filter selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        filter_info = self.color_filters[filter_key]
        self.show_progress(f"Applying {filter_info['display_name']}...")
        
        try:
            if filter_key == 'gray':
                # Convert to complete grayscale
                gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
                self.result_image = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            elif filter_key == 'red':
                # Apply red filter - enhance red channel, reduce green/blue
                self.result_image = self.current_image.astype(np.float32)
                self.result_image[:, :, 0] *= 0.6   # Blue channel - reduce
                self.result_image[:, :, 1] *= 0.6   # Green channel - reduce  
                self.result_image[:, :, 2] *= 1.5   # Red channel - enhance
                self.result_image = np.clip(self.result_image, 0, 255).astype(np.uint8)
            elif filter_key == 'yellow':
                # Apply yellow filter - enhance red/green channels, reduce blue
                self.result_image = self.current_image.astype(np.float32)
                self.result_image[:, :, 0] *= 0.5   # Blue channel - reduce significantly
                self.result_image[:, :, 1] *= 1.3   # Green channel - enhance  
                self.result_image[:, :, 2] *= 1.3   # Red channel - enhance
                self.result_image = np.clip(self.result_image, 0, 255).astype(np.uint8)
            else:
                # Fallback - just copy the current image
                self.result_image = self.current_image.copy()
            
            self.hide_progress()
            self.display_results(filter_info['display_name'], is_filter=True)
            return True
            
        except Exception as e:
            self.hide_progress()
            self.status_label.config(text=f"❌ Filter failed: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Color filter failed:\n{str(e)}")
            return False
    
    # ============================================================================
    #                           UTILITY AND HELPER METHODS
    # ============================================================================
    
    def update_status(self, message, success=True):
        """
        Update the status label with a message
        
        Args:
            message (str): Status message to display
            success (bool): True for success (green), False for error (red)
        """
        color = '#4CAF50' if success else '#f44336'
        self.status_label.config(text=message, fg=color)
    
    def save_result(self):
        """
        Save the processed result image to the same folder as the original
        
        The saved file will have a descriptive name with timestamp to avoid overwrites.
        """
        if self.result_image is not None:
            try:
                # Generate descriptive filename with timestamp
                current_image_path = self.image_paths[self.current_image_index]
                original_name = os.path.splitext(os.path.basename(current_image_path))[0]
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{original_name}_processed_{timestamp}.jpg"
                
                # Save to same directory as original image
                filepath = os.path.join(os.path.dirname(current_image_path), filename)
                cv2.imwrite(filepath, self.result_image)
                
                messagebox.showinfo("Success", f"Image saved as:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")
        else:
            messagebox.showwarning("Warning", "No result image to save!")
    
    def show_progress(self, message="Processing..."):
        """Show progress indicator with custom message"""
        self.status_label.config(text=message, fg='#FF9800')
        self.progress_bar.pack(pady=10)
        self.progress_bar.start(10)
        self.root.update()
    
    def hide_progress(self):
        """Hide progress indicator"""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
    
    def load_current_image(self):
        """
        Load and preprocess the currently selected image
        
        Returns:
            bool: True if image loaded successfully, False otherwise
        """
        if self.current_image_index < len(self.image_paths):
            return self.load_image(self.image_paths[self.current_image_index])
        return False
    
    # ============================================================================
    #                           COLOR PROCESSING OPERATIONS
    # ============================================================================
    
    def load_image(self, image_path):
        """
        Load and preprocess an image from file path
        
        This method loads an image, resizes it if needed for performance,
        and creates the different versions needed for processing.
        
        Args:
            image_path (str): Full path to the image file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.original_image = cv2.imread(image_path)
            if self.original_image is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Resize image if too large for processing
            height, width = self.original_image.shape[:2]
            if width > 1200 or height > 900:
                scale = min(1200/width, 900/height)
                new_width = int(width * scale)
                new_height = int(height * scale)
                self.original_image = cv2.resize(self.original_image, (new_width, new_height))
            
            self.current_image = self.original_image.copy()
            self.hsv_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2HSV)
            
            image_name = os.path.basename(image_path)
            self.status_label.config(text=f"✅ Image loaded: {image_name} (Image {self.current_image_index + 1})", fg='#4CAF50')
            return True
        except Exception as e:
            self.status_label.config(text=f"❌ Failed to load image: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            return False
    
    def perform_color_extraction(self, color_key):
        """
        Extract specified color from image and make everything else gray
        
        This method:
        1. Creates a mask for the selected color in HSV space
        2. Keeps the original color where mask matches
        3. Makes everything else a neutral gray
        
        Args:
            color_key (str): Key identifying which color to extract ('green', 'purple', 'blue')
            
        Returns:
            bool: True if successful, False otherwise
        """
        if color_key not in self.extraction_colors:
            messagebox.showerror("Error", "Invalid color selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        color_info = self.extraction_colors[color_key]
        self.show_progress(f"Extracting {color_info['display_name']} color...")
        
        try:
            # Create mask for the selected color using HSV thresholds
            lower_hsv = color_info['hsv_lower_bound']
            upper_hsv = color_info['hsv_upper_bound']
            
            mask = cv2.inRange(self.hsv_image, lower_hsv, upper_hsv)
            
            # Apply morphological operations to clean up the mask
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Create neutral gray background
            gray_background = np.full_like(self.current_image, (128, 128, 128), dtype=np.uint8)
            
            # Create the result image: keep original color where mask matches, gray elsewhere
            self.result_image = self.current_image.copy()
            
            # Convert mask to 3-channel
            mask_3channel = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            mask_normalized = mask_3channel.astype(float) / 255
            
            # Apply the effect: keep original where mask is white, use gray where mask is black
            self.result_image = (self.result_image * mask_normalized + 
                               gray_background * (1 - mask_normalized)).astype(np.uint8)
            
            self.hide_progress()
            self.display_results(color_info['display_name'])
            return True
            
        except Exception as e:
            self.hide_progress()
            self.status_label.config(text=f"❌ Extraction failed: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Color extraction failed:\n{str(e)}")
            return False
    
    def reset_for_new_operation(self):
        """Reset UI state for starting a new operation"""
        self.hide_extraction_options()
        self.hide_filter_options()
    
    # ============================================================================
    #                           MAIN APPLICATION ENTRY POINT
    # ============================================================================
    
    def run(self, image_paths):
        """Start the GUI application with the provided images"""
        try:
            self.image_paths = image_paths
            if self.load_current_image():
                # Center the window
                self.root.update_idletasks()
                width = self.root.winfo_width()
                height = self.root.winfo_height()
                x = (self.root.winfo_screenwidth() // 2) - (width // 2)
                y = (self.root.winfo_screenheight() // 2) - (height // 2)
                self.root.geometry(f'{width}x{height}+{x}+{y}')
                
                # Start the GUI
                self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Application error:\n{str(e)}")
