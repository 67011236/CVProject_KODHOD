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

# Import our color processing module
from colorextract import extract_color, apply_color_filter, get_extraction_colors, get_color_filters

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
        self.image_buttons = []            # List of image selection buttons
        
        # ==================== COLOR PROCESSING CONFIGURATION ====================
        # Get color configurations from the colorextract module
        self.extraction_colors = get_extraction_colors()
        self.color_filters = get_color_filters()
        
        # ==================== GUI SETUP ====================
        self.setup_main_window()
        self.create_user_interface()
        
    # ============================================================================
    #                           GUI SETUP AND INITIALIZATION
    # ============================================================================
    
    def setup_main_window(self):
        """Configure the main application window"""
        self.root = tk.Tk()
        self.root.title("Color Extraction Program - Multi-Image Support")
        self.root.geometry("1200x800")  # Larger window for multiple images
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
        """Create dynamic image selection interface based on available images"""
        # Container for image selection controls
        self.image_selection_container = tk.Frame(self.root, bg='#f0f0f0')
        self.image_selection_container.pack(pady=10)
        
        # Current image indicator label - will be updated with actual count later
        self.current_image_indicator = tk.Label(
            self.image_selection_container, 
            text="Current Image: Loading...", 
            font=('Arial', 14, 'bold'), 
            bg='#f0f0f0', 
            fg='#333'
        )
        self.current_image_indicator.pack(pady=5)
        
        # Container for navigation controls
        navigation_container = tk.Frame(self.image_selection_container, bg='#f0f0f0')
        navigation_container.pack(pady=5)
        
        # Previous button
        self.prev_button = tk.Button(
            navigation_container,
            text="← Previous",
            font=('Arial', 12, 'bold'),
            bg='#757575',
            fg='white',
            width=12,
            height=1,
            relief='flat',
            cursor='hand2',
            command=self.previous_image
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)
        
        # Next button
        self.next_button = tk.Button(
            navigation_container,
            text="Next →",
            font=('Arial', 12, 'bold'),
            bg='#757575',
            fg='white',
            width=12,
            height=1,
            relief='flat',
            cursor='hand2',
            command=self.next_image
        )
        self.next_button.pack(side=tk.LEFT, padx=5)
        
        # Container for image selection buttons (will be populated when images are loaded)
        self.image_buttons_container = tk.Frame(self.image_selection_container, bg='#f0f0f0')
        self.image_buttons_container.pack(pady=10)
    
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
    def setup_image_buttons(self):
        """Create image selection buttons based on available images"""
        # Clear existing buttons
        for widget in self.image_buttons_container.winfo_children():
            widget.destroy()
        self.image_buttons.clear()
        
        if not self.image_paths:
            return
        
        # Create a button for each image
        total_images = len(self.image_paths)
        
        # Create buttons in rows of 5 for better layout
        current_row = None
        for i, image_path in enumerate(self.image_paths):
            if i % 5 == 0:  # Start a new row every 5 buttons
                current_row = tk.Frame(self.image_buttons_container, bg='#f0f0f0')
                current_row.pack(pady=2)
            
            # Create button with image name
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            button_text = f"{i+1}: {image_name[:8]}..." if len(image_name) > 8 else f"{i+1}: {image_name}"
            
            button = tk.Button(
                current_row,
                text=button_text,
                font=('Arial', 9, 'bold'),
                bg='#757575',  # Inactive color initially
                fg='white',
                width=12,
                height=1,
                relief='flat',
                cursor='hand2',
                command=lambda idx=i: self.switch_to_image(idx)
            )
            button.pack(side=tk.LEFT, padx=2)
            self.image_buttons.append(button)
        
        # Update the current image indicator
        self.update_image_indicator()
    
    def update_image_buttons(self):
        """Update the visual state of image selection buttons"""
        for i, button in enumerate(self.image_buttons):
            if i == self.current_image_index:
                button.config(bg='#2196F3')  # Active - blue
            else:
                button.config(bg='#757575')  # Inactive - gray
    
    def update_image_indicator(self):
        """Update the current image indicator text"""
        total_images = len(self.image_paths)
        if total_images > 0:
            current_name = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
            self.current_image_indicator.config(
                text=f"Image {self.current_image_index + 1} of {total_images}: {current_name}"
            )
    
    def previous_image(self):
        """Switch to the previous image"""
        if len(self.image_paths) > 1:
            previous_index = (self.current_image_index - 1) % len(self.image_paths)
            self.switch_to_image(previous_index)
    
    def next_image(self):
        """Switch to the next image"""
        if len(self.image_paths) > 1:
            next_index = (self.current_image_index + 1) % len(self.image_paths)
            self.switch_to_image(next_index)
        
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
            image_index (int): Index of image to switch to
        """
        if 0 <= image_index < len(self.image_paths):
            self.current_image_index = image_index
            self.load_current_image()
            
            # Update the current image indicator text
            self.update_image_indicator()
            
            # Update button appearances
            self.update_image_buttons()
            
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
        current_image_name = os.path.splitext(os.path.basename(self.image_paths[self.current_image_index]))[0]
        results_title = tk.Label(self.results_display_container, 
                                text=f"✨ {operation_name} {operation_type} Results\nImage {self.current_image_index + 1} of {len(self.image_paths)}: {current_image_name}", 
                                font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
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
        
        # Add navigation buttons in results for easy image switching
        if len(self.image_paths) > 1:
            nav_frame = tk.Frame(action_frame, bg='#f0f0f0')
            nav_frame.pack(side=tk.LEFT, padx=20)
            
            if self.current_image_index > 0:
                prev_btn = tk.Button(nav_frame, text="← Previous Image", 
                                    font=('Arial', 10, 'bold'), bg='#9C27B0', fg='white',
                                    relief='flat', cursor='hand2', 
                                    command=self.previous_image)
                prev_btn.pack(side=tk.TOP, pady=2)
            
            if self.current_image_index < len(self.image_paths) - 1:
                next_btn = tk.Button(nav_frame, text="Next Image →", 
                                    font=('Arial', 10, 'bold'), bg='#9C27B0', fg='white',
                                    relief='flat', cursor='hand2', 
                                    command=self.next_image)
                next_btn.pack(side=tk.TOP, pady=2)
        
        operation_type = "filter" if is_filter else "extraction"
        self.status_label.config(text=f"✅ {operation_name} {operation_type} completed successfully!", fg='#4CAF50')
    
    def apply_color_filter(self, filter_key):
        """Apply color filter using colorextract module"""
        if filter_key not in self.color_filters:
            messagebox.showerror("Error", "Invalid filter selection!")
            return False
        
        if self.original_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return False
        
        filter_info = self.color_filters[filter_key]
        self.show_progress(f"Applying {filter_info['display_name']}...")
        
        try:
            # Use the colorextract module function
            self.result_image, filter_display_name = apply_color_filter(
                self.current_image, 
                filter_key
            )
            
            self.hide_progress()
            self.display_results(filter_display_name, is_filter=True)
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
            total_images = len(self.image_paths)
            self.status_label.config(text=f"✅ Image loaded: {image_name} (Image {self.current_image_index + 1} of {total_images})", fg='#4CAF50')
            return True
        except Exception as e:
            self.status_label.config(text=f"❌ Failed to load image: {str(e)}", fg='#f44336')
            messagebox.showerror("Error", f"Failed to load image:\n{str(e)}")
            return False
    
    def perform_color_extraction(self, color_key):
        """
        Extract specified color from image using colorextract module
        
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
            # Use the colorextract module function
            self.result_image, color_display_name = extract_color(
                self.current_image, 
                self.hsv_image, 
                color_key
            )
            
            self.hide_progress()
            self.display_results(color_display_name)
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
            
            # Set up image selection buttons now that we have the paths
            self.setup_image_buttons()
            
            if self.load_current_image():
                # Update image buttons to show current selection
                self.update_image_buttons()
                
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
