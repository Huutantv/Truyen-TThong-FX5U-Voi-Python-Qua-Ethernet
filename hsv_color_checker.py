import cv2
import numpy as np
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QSlider, 
                            QComboBox, QGroupBox, QGridLayout, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

class HSVColorChecker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HSV Color Checker By Factory Automation")
        self.setGeometry(100, 100, 1200, 700)
        
        # Initialize camera
        self.camera = None
        self.camera_index = 0
        
        # HSV range variables
        self.h_min = 0
        self.h_max = 179
        self.s_min = 0
        self.s_max = 255
        self.v_min = 0
        self.v_max = 255
        
        # Save current color range to our list
        self.saved_colors = []
        
        # Initialize UI
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Layout for camera view and control panels
        content_layout = QHBoxLayout()
        
        # Left panel - Camera view
        left_panel = QVBoxLayout()
        
        # Camera view
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(640, 480)
        self.camera_label.setStyleSheet("""
            QLabel {
                border: 2px solid #2196F3;
                background-color: black;
            }
        """)
        
        # Masked view
        self.mask_label = QLabel()
        self.mask_label.setFixedSize(640, 480)
        self.mask_label.setStyleSheet("""
            QLabel {
                border: 2px solid #F44336;
                background-color: black;
            }
        """)
        
        camera_layout = QHBoxLayout()
        camera_layout.addWidget(self.camera_label)
        camera_layout.addWidget(self.mask_label)
        left_panel.addLayout(camera_layout)
        
        # Camera controls
        camera_controls = QHBoxLayout()
        
        camera_label = QLabel("Camera:")
        self.camera_select = QComboBox()
        self.camera_select.addItems([f"Camera {i}" for i in range(5)])
        
        self.start_camera_btn = QPushButton("Start Camera")
        self.start_camera_btn.clicked.connect(self.toggle_camera)
        self.start_camera_btn.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        
        camera_controls.addWidget(camera_label)
        camera_controls.addWidget(self.camera_select)
        camera_controls.addWidget(self.start_camera_btn)
        camera_controls.addStretch()
        
        left_panel.addLayout(camera_controls)
        
        # HSV Color value display
        self.color_value_label = QLabel("Click on the image to get HSV value")
        self.color_value_label.setStyleSheet("""
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                padding: 10px;
                background: white;
                border: 2px solid gray;
                margin-top: 10px;
            }
        """)
        self.color_value_label.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(self.color_value_label)
        
        content_layout.addLayout(left_panel)
        
        # Right panel - HSV controls
        right_panel = QVBoxLayout()
        
        # HSV controls
        hsv_group = QGroupBox("HSV Range Controls")
        hsv_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #2196F3;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        hsv_layout = QGridLayout()
        
        # Hue sliders
        h_min_label = QLabel("H Min:")
        self.h_min_slider = QSlider(Qt.Horizontal)
        self.h_min_slider.setRange(0, 179)
        self.h_min_slider.setValue(self.h_min)
        self.h_min_slider.valueChanged.connect(self.update_h_min)
        self.h_min_value = QLabel(str(self.h_min))
        
        h_max_label = QLabel("H Max:")
        self.h_max_slider = QSlider(Qt.Horizontal)
        self.h_max_slider.setRange(0, 179)
        self.h_max_slider.setValue(self.h_max)
        self.h_max_slider.valueChanged.connect(self.update_h_max)
        self.h_max_value = QLabel(str(self.h_max))
        
        # Saturation sliders
        s_min_label = QLabel("S Min:")
        self.s_min_slider = QSlider(Qt.Horizontal)
        self.s_min_slider.setRange(0, 255)
        self.s_min_slider.setValue(self.s_min)
        self.s_min_slider.valueChanged.connect(self.update_s_min)
        self.s_min_value = QLabel(str(self.s_min))
        
        s_max_label = QLabel("S Max:")
        self.s_max_slider = QSlider(Qt.Horizontal)
        self.s_max_slider.setRange(0, 255)
        self.s_max_slider.setValue(self.s_max)
        self.s_max_slider.valueChanged.connect(self.update_s_max)
        self.s_max_value = QLabel(str(self.s_max))
        
        # Value sliders
        v_min_label = QLabel("V Min:")
        self.v_min_slider = QSlider(Qt.Horizontal)
        self.v_min_slider.setRange(0, 255)
        self.v_min_slider.setValue(self.v_min)
        self.v_min_slider.valueChanged.connect(self.update_v_min)
        self.v_min_value = QLabel(str(self.v_min))
        
        v_max_label = QLabel("V Max:")
        self.v_max_slider = QSlider(Qt.Horizontal)
        self.v_max_slider.setRange(0, 255)
        self.v_max_slider.setValue(self.v_max)
        self.v_max_slider.valueChanged.connect(self.update_v_max)
        self.v_max_value = QLabel(str(self.v_max))
        
        # Add to layout
        hsv_layout.addWidget(h_min_label, 0, 0)
        hsv_layout.addWidget(self.h_min_slider, 0, 1)
        hsv_layout.addWidget(self.h_min_value, 0, 2)
        
        hsv_layout.addWidget(h_max_label, 1, 0)
        hsv_layout.addWidget(self.h_max_slider, 1, 1)
        hsv_layout.addWidget(self.h_max_value, 1, 2)
        
        hsv_layout.addWidget(s_min_label, 2, 0)
        hsv_layout.addWidget(self.s_min_slider, 2, 1)
        hsv_layout.addWidget(self.s_min_value, 2, 2)
        
        hsv_layout.addWidget(s_max_label, 3, 0)
        hsv_layout.addWidget(self.s_max_slider, 3, 1)
        hsv_layout.addWidget(self.s_max_value, 3, 2)
        
        hsv_layout.addWidget(v_min_label, 4, 0)
        hsv_layout.addWidget(self.v_min_slider, 4, 1)
        hsv_layout.addWidget(self.v_min_value, 4, 2)
        
        hsv_layout.addWidget(v_max_label, 5, 0)
        hsv_layout.addWidget(self.v_max_slider, 5, 1)
        hsv_layout.addWidget(self.v_max_value, 5, 2)
        
        hsv_group.setLayout(hsv_layout)
        right_panel.addWidget(hsv_group)
        
        # Save color range button
        self.save_color_btn = QPushButton("Save Current HSV Range")
        self.save_color_btn.clicked.connect(self.save_color_range)
        self.save_color_btn.setStyleSheet("""
            QPushButton {
                background: #2196F3;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #1976D2;
            }
        """)
        right_panel.addWidget(self.save_color_btn)
        
        # Saved colors display
        saved_colors_group = QGroupBox("Saved Color Ranges")
        saved_colors_group.setStyleSheet(hsv_group.styleSheet())
        saved_colors_layout = QVBoxLayout()
        
        self.saved_colors_label = QLabel("No colors saved yet")
        self.saved_colors_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.saved_colors_label.setStyleSheet("""
            QLabel {
                font-family: monospace;
                padding: 10px;
                background: white;
                border: 1px solid #ccc;
            }
        """)
        saved_colors_layout.addWidget(self.saved_colors_label)
        
        saved_colors_group.setLayout(saved_colors_layout)
        right_panel.addWidget(saved_colors_group)
        
        # Need color pickers
        dual_range_group = QGroupBox("Color Range Options")
        dual_range_group.setStyleSheet(hsv_group.styleSheet())
        dual_range_layout = QVBoxLayout()
        
        self.dual_range_cb = QCheckBox("Use dual range (for colors like red)")
        self.dual_range_cb.setChecked(False)
        dual_range_layout.addWidget(self.dual_range_cb)
        
        dual_range_group.setLayout(dual_range_layout)
        right_panel.addWidget(dual_range_group)
        
        # Add reset button
        self.reset_btn = QPushButton("Reset HSV Range")
        self.reset_btn.clicked.connect(self.reset_hsv_range)
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background: #F44336;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 4px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #D32F2F;
            }
        """)
        right_panel.addWidget(self.reset_btn)
        
        # Add stretch to push everything up
        right_panel.addStretch()
        
        content_layout.addLayout(right_panel)
        main_layout.addLayout(content_layout)
        
        # Timer for camera
        self.camera_timer = QTimer()
        self.camera_timer.timeout.connect(self.update_frame)
        
        # Mouse click event
        self.camera_label.mousePressEvent = self.get_color_at_point
        
    def toggle_camera(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(self.camera_select.currentIndex())
            if self.camera.isOpened():
                self.start_camera_btn.setText("Stop Camera")
                self.start_camera_btn.setStyleSheet("""
                    QPushButton {
                        background: #f44336;
                        color: white;
                        padding: 8px 15px;
                        border: none;
                        border-radius: 4px;
                    }
                    QPushButton:hover {
                        background: #d32f2f;
                    }
                """)
                self.camera_timer.start(30)
            else:
                self.camera = None
        else:
            self.camera_timer.stop()
            self.camera.release()
            self.camera = None
            self.start_camera_btn.setText("Start Camera")
            self.start_camera_btn.setStyleSheet("""
                QPushButton {
                    background: #4CAF50;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #45a049;
                }
            """)
            self.camera_label.clear()
            self.mask_label.clear()
            
    def update_frame(self):
        ret, frame = self.camera.read()
        if ret:
            # Store the frame for color picking
            self.current_frame = frame
            
            # Show the regular frame
            self.display_frame(frame, self.camera_label)
            
            # Apply HSV mask and show it
            self.apply_hsv_mask(frame)
            
    def apply_hsv_mask(self, frame):
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask based on current HSV range
        if self.dual_range_cb.isChecked() and self.h_min > self.h_max:
            # For colors like red that wrap around the hue circle
            mask1 = cv2.inRange(hsv, np.array([0, self.s_min, self.v_min]), 
                               np.array([self.h_max, self.s_max, self.v_max]))
            mask2 = cv2.inRange(hsv, np.array([self.h_min, self.s_min, self.v_min]), 
                               np.array([179, self.s_max, self.v_max]))
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            # Normal range
            mask = cv2.inRange(hsv, np.array([self.h_min, self.s_min, self.v_min]), 
                              np.array([self.h_max, self.s_max, self.v_max]))
        
        # Apply the mask to get only the filtered regions
        filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)
        
        # Display the mask
        self.display_frame(filtered_frame, self.mask_label)
        
    def display_frame(self, frame, label):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qt_image).scaled(
            label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            
    def get_color_at_point(self, event):
        if not hasattr(self, 'current_frame'):
            return
            
        # Get click position relative to the image
        x = int(event.x() * self.current_frame.shape[1] / self.camera_label.width())
        y = int(event.y() * self.current_frame.shape[0] / self.camera_label.height())
        
        # Ensure within bounds
        if x >= self.current_frame.shape[1] or y >= self.current_frame.shape[0]:
            return
            
        # Get the BGR color at that point
        bgr_color = self.current_frame[y, x]
        
        # Convert to HSV
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        
        # Update the color value label
        self.color_value_label.setText(f"HSV: {hsv_color[0]}, {hsv_color[1]}, {hsv_color[2]} | BGR: {bgr_color[2]}, {bgr_color[1]}, {bgr_color[0]}")
        
        # Update the sliders to match this color (optional)
        self.h_min_slider.setValue(max(0, hsv_color[0] - 10))
        self.h_max_slider.setValue(min(179, hsv_color[0] + 10))
        self.s_min_slider.setValue(max(0, hsv_color[1] - 50))
        self.s_max_slider.setValue(255)
        self.v_min_slider.setValue(max(0, hsv_color[2] - 50))
        self.v_max_slider.setValue(255)
        
    def update_h_min(self, value):
        self.h_min = value
        self.h_min_value.setText(str(value))
        
    def update_h_max(self, value):
        self.h_max = value
        self.h_max_value.setText(str(value))
        
    def update_s_min(self, value):
        self.s_min = value
        self.s_min_value.setText(str(value))
        
    def update_s_max(self, value):
        self.s_max = value
        self.s_max_value.setText(str(value))
        
    def update_v_min(self, value):
        self.v_min = value
        self.v_min_value.setText(str(value))
        
    def update_v_max(self, value):
        self.v_max = value
        self.v_max_value.setText(str(value))
        
    def save_color_range(self):
        if self.dual_range_cb.isChecked() and self.h_min > self.h_max:
            # For colors that wrap around (like red)
            color_info = {
                'name': f"Color_{len(self.saved_colors)+1}",
                'use_dual_range': True,
                'lower1': np.array([0, self.s_min, self.v_min]),
                'upper1': np.array([self.h_max, self.s_max, self.v_max]),
                'lower2': np.array([self.h_min, self.s_min, self.v_min]),
                'upper2': np.array([179, self.s_max, self.v_max])
            }
        else:
            # Normal range
            color_info = {
                'name': f"Color_{len(self.saved_colors)+1}",
                'use_dual_range': False,
                'lower1': np.array([self.h_min, self.s_min, self.v_min]),
                'upper1': np.array([self.h_max, self.s_max, self.v_max])
            }
            
        self.saved_colors.append(color_info)
        self.update_saved_colors_display()
        
    def update_saved_colors_display(self):
        if not self.saved_colors:
            self.saved_colors_label.setText("No colors saved yet")
            return
            
        text = ""
        for i, color in enumerate(self.saved_colors):
            text += f"Color {i+1}:\n"
            if color['use_dual_range']:
                text += f"  Range 1: H:{color['lower1'][0]}-{color['upper1'][0]}, "
                text += f"S:{color['lower1'][1]}-{color['upper1'][1]}, "
                text += f"V:{color['lower1'][2]}-{color['upper1'][2]}\n"
                text += f"  Range 2: H:{color['lower2'][0]}-{color['upper2'][0]}, "
                text += f"S:{color['lower2'][1]}-{color['upper2'][1]}, "
                text += f"V:{color['lower2'][2]}-{color['upper2'][2]}\n"
            else:
                text += f"  H:{color['lower1'][0]}-{color['upper1'][0]}, "
                text += f"S:{color['lower1'][1]}-{color['upper1'][1]}, "
                text += f"V:{color['lower1'][2]}-{color['upper1'][2]}\n"
            
            # Add code format for easy copying
            text += f"  Code format:\n"
            if color['use_dual_range']:
                text += f"  'lower1': np.array([{color['lower1'][0]}, {color['lower1'][1]}, {color['lower1'][2]}]),\n"
                text += f"  'upper1': np.array([{color['upper1'][0]}, {color['upper1'][1]}, {color['upper1'][2]}]),\n"
                text += f"  'lower2': np.array([{color['lower2'][0]}, {color['lower2'][1]}, {color['lower2'][2]}]),\n"
                text += f"  'upper2': np.array([{color['upper2'][0]}, {color['upper2'][1]}, {color['upper2'][2]}]),\n"
                text += f"  'use_dual_range': True\n"
            else:
                text += f"  'lower1': np.array([{color['lower1'][0]}, {color['lower1'][1]}, {color['lower1'][2]}]),\n"
                text += f"  'upper1': np.array([{color['upper1'][0]}, {color['upper1'][1]}, {color['upper1'][2]}]),\n"
                text += f"  'use_dual_range': False\n"
            
            text += "\n"
            
        self.saved_colors_label.setText(text)
        
    def reset_hsv_range(self):
        # Full range values
        self.h_min_slider.setValue(0)
        self.h_max_slider.setValue(179)
        self.s_min_slider.setValue(0)
        self.s_max_slider.setValue(255)
        self.v_min_slider.setValue(0)
        self.v_max_slider.setValue(255)
        
    def closeEvent(self, event):
        if self.camera is not None:
            self.camera.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HSVColorChecker()
    window.show()
    sys.exit(app.exec_()) 