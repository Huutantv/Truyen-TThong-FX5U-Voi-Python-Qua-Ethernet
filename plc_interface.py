import sys
import rk_mcprotocol as mc
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QGroupBox, QSpinBox, QCheckBox,
                            QGridLayout, QFrame, QRadioButton)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont

class PLCInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLC Communication Interface by Factory Automation")
        self.setGeometry(100, 100, 1000, 800)
        
        # Biến lưu socket kết nối
        self.socket = None
        
        # Thiết lập style
        self.setup_style()
        
        # Tạo giao diện chính
        self.init_ui()
        
    def setup_style(self):
        # Thiết lập style cho cửa sổ
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                color: #2980b9;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
            QLineEdit, QSpinBox {
                padding: 3px;
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 3px;
            }
        """)
        
    def init_ui(self):
        # Widget chính
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        
        # Thêm tiêu đề
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2980b9, stop:1 #3498db);
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel("Factory Automation")
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24pt;
                font-weight: bold;
                font-family: Arial;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle_label = QLabel("PLC Communication Solutions PLC Mitsubishi FX5U")
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ECF0F1;
                font-size: 12pt;
                font-style: italic;
            }
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)
        main_layout.addWidget(header_frame)
        
        # Nhóm kết nối
        connection_group = QGroupBox("Kết nối PLC")
        connection_layout = QHBoxLayout()
        
        self.ip_input = QLineEdit("192.168.0.23")
        self.port_input = QLineEdit("1025")
        self.connect_btn = QPushButton("Kết nối")
        self.connect_btn.clicked.connect(self.toggle_connection)
        
        connection_layout.addWidget(QLabel("IP:"))
        connection_layout.addWidget(self.ip_input)
        connection_layout.addWidget(QLabel("Port:"))
        connection_layout.addWidget(self.port_input)
        connection_layout.addWidget(self.connect_btn)
        connection_layout.addStretch()
        connection_group.setLayout(connection_layout)
        
        # Layout chính cho điều khiển
        control_layout = QHBoxLayout()
        
        # Nhóm điều khiển bit M
        m_bit_group = QGroupBox("Điều khiển Bit M")
        m_bit_layout = QVBoxLayout()
        
        # Điều khiển đơn bit M
        m_single_layout = QGridLayout()
        self.m_address_input = QSpinBox()
        self.m_address_input.setRange(0, 1000)
        self.m_read_btn = QPushButton("Đọc")
        self.m_read_btn.clicked.connect(self.read_m_bit)
        self.m_write_btn = QPushButton("Ghi")
        self.m_write_btn.clicked.connect(self.write_m_bit)
        
        m_single_layout.addWidget(QLabel("Địa chỉ M:"), 0, 0)
        m_single_layout.addWidget(self.m_address_input, 0, 1)
        m_single_layout.addWidget(self.m_read_btn, 0, 2)
        m_single_layout.addWidget(self.m_write_btn, 0, 3)
        
        # Nhóm điều khiển trạng thái M
        m_state_group = QGroupBox("Trạng thái Bit M")
        m_state_layout = QHBoxLayout()
        self.m_value_on = QRadioButton("ON")
        self.m_value_off = QRadioButton("OFF")
        self.m_value_off.setChecked(True)  # Mặc định là OFF
        m_state_layout.addWidget(self.m_value_on)
        m_state_layout.addWidget(self.m_value_off)
        m_state_group.setLayout(m_state_layout)
        
        # Các nút điều khiển nhanh
        quick_control_layout = QGridLayout()
        self.quick_m_buttons = []
        for i in range(8):
            btn = QPushButton(f"M{i}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, x=i: self.quick_write_m(x, checked))
            quick_control_layout.addWidget(btn, i//4, i%4)
            self.quick_m_buttons.append(btn)
            
        m_bit_layout.addLayout(m_single_layout)
        m_bit_layout.addWidget(m_state_group)
        m_bit_layout.addWidget(QLabel("Điều khiển nhanh:"))
        m_bit_layout.addLayout(quick_control_layout)
        m_bit_group.setLayout(m_bit_layout)
        
        # Nhóm điều khiển thanh ghi D
        d_register_group = QGroupBox("Điều khiển Thanh ghi D")
        d_register_layout = QVBoxLayout()
        
        d_control_layout = QGridLayout()
        self.d_address_input = QSpinBox()
        self.d_address_input.setRange(0, 1000)
        self.d_value_input = QSpinBox()
        self.d_value_input.setRange(-32768, 32767)
        self.d_read_btn = QPushButton("Đọc")
        self.d_read_btn.clicked.connect(self.read_d_register)
        self.d_write_btn = QPushButton("Ghi")
        self.d_write_btn.clicked.connect(self.write_d_register)
        
        d_control_layout.addWidget(QLabel("Địa chỉ D:"), 0, 0)
        d_control_layout.addWidget(self.d_address_input, 0, 1)
        d_control_layout.addWidget(QLabel("Giá trị:"), 0, 2)
        d_control_layout.addWidget(self.d_value_input, 0, 3)
        d_control_layout.addWidget(self.d_read_btn, 0, 4)
        d_control_layout.addWidget(self.d_write_btn, 0, 5)
        
        # Thêm một số nút preset cho giá trị D phổ biến
        preset_layout = QGridLayout()
        preset_values = [0, 100, 500, 1000, 5000, 10000]
        for i, value in enumerate(preset_values):
            btn = QPushButton(str(value))
            btn.clicked.connect(lambda _, v=value: self.d_value_input.setValue(v))
            preset_layout.addWidget(btn, i//3, i%3)
            
        d_register_layout.addLayout(d_control_layout)
        d_register_layout.addWidget(QLabel("Giá trị preset:"))
        d_register_layout.addLayout(preset_layout)
        d_register_group.setLayout(d_register_layout)
        
        control_layout.addWidget(m_bit_group)
        control_layout.addWidget(d_register_group)
        
        # Vùng hiển thị log
        log_group = QGroupBox("Nhật ký hoạt động")
        log_layout = QVBoxLayout()
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        clear_log_btn = QPushButton("Xóa nhật ký")
        clear_log_btn.clicked.connect(self.log_display.clear)
        log_layout.addWidget(self.log_display)
        log_layout.addWidget(clear_log_btn)
        log_group.setLayout(log_layout)
        
        # Thêm các nhóm vào layout chính
        main_layout.addWidget(connection_group)
        main_layout.addLayout(control_layout)
        main_layout.addWidget(log_group)
        
       
        # Timer để kiểm tra kết nối và cập nhật trạng thái
        self.connection_timer = QTimer()
        self.connection_timer.timeout.connect(self.check_connection)
        
        # Cập nhật trạng thái ban đầu
        self.update_ui_state(False)
        
    def update_ui_state(self, connected):
        """Cập nhật trạng thái các nút dựa vào tình trạng kết nối"""
        self.m_read_btn.setEnabled(connected)
        self.m_write_btn.setEnabled(connected)
        self.d_read_btn.setEnabled(connected)
        self.d_write_btn.setEnabled(connected)
        for btn in self.quick_m_buttons:
            btn.setEnabled(connected)
            
    def quick_write_m(self, address, state):
        """Ghi nhanh giá trị bit M"""
        if self.socket is None:
            self.log_message("Chưa kết nối với PLC")
            return
            
        try:
            value = 1 if state else 0
            mc.write_bit(self.socket, headdevice=f'm{address}', data_list=[value])
            self.log_message(f"Đã ghi bit M{address} = {value}")
        except Exception as e:
            self.log_message(f"Lỗi ghi bit M: {str(e)}")
            self.quick_m_buttons[address].setChecked(not state)
            
    def read_m_bit(self):
        """Đọc giá trị bit M"""
        if self.socket is None:
            self.log_message("Chưa kết nối với PLC")
            return
            
        try:
            address = self.m_address_input.value()
            value = mc.read_bit(self.socket, headdevice=f'm{address}', length=1)[0]
            if value == 1:
                self.m_value_on.setChecked(True)
            else:
                self.m_value_off.setChecked(True)
            self.log_message(f"Đã đọc bit M{address} = {value}")
        except Exception as e:
            self.log_message(f"Lỗi đọc bit M: {str(e)}")
            
    def read_d_register(self):
        """Đọc giá trị thanh ghi D"""
        if self.socket is None:
            self.log_message("Chưa kết nối với PLC")
            return
            
        try:
            address = self.d_address_input.value()
            value = mc.read_sign_word(self.socket, headdevice=f'd{address}', length=1, signed_type=True)[0]
            self.d_value_input.setValue(value)
            self.log_message(f"Đã đọc thanh ghi D{address} = {value}")
        except Exception as e:
            self.log_message(f"Lỗi đọc thanh ghi D: {str(e)}")
            
    def toggle_connection(self):
        if self.socket is None:
            try:
                self.socket = mc.open_socket(self.ip_input.text(), int(self.port_input.text()))
                self.log_message("Đã kết nối thành công với PLC")
                self.connect_btn.setText("Ngắt kết nối")
                self.connection_timer.start(1000)
                self.update_ui_state(True)
            except Exception as e:
                self.log_message(f"Lỗi kết nối: {str(e)}")
        else:
            self.socket.close()
            self.socket = None
            self.log_message("Đã ngắt kết nối với PLC")
            self.connect_btn.setText("Kết nối")
            self.connection_timer.stop()
            self.update_ui_state(False)
            
    def check_connection(self):
        if self.socket is not None:
            try:
                mc.read_sign_word(self.socket, headdevice='d0', length=1, signed_type=False)
            except Exception as e:
                self.log_message(f"Mất kết nối: {str(e)}")
                self.socket.close()
                self.socket = None
                self.connect_btn.setText("Kết nối")
                self.connection_timer.stop()
                self.update_ui_state(False)
                
    def write_m_bit(self):
        if self.socket is None:
            self.log_message("Chưa kết nối với PLC")
            return
            
        try:
            address = self.m_address_input.value()
            value = 1 if self.m_value_on.isChecked() else 0
            mc.write_bit(self.socket, headdevice=f'm{address}', data_list=[value])
            self.log_message(f"Đã ghi bit M{address} = {value}")
        except Exception as e:
            self.log_message(f"Lỗi ghi bit M: {str(e)}")
            
    def write_d_register(self):
        if self.socket is None:
            self.log_message("Chưa kết nối với PLC")
            return
            
        try:
            address = self.d_address_input.value()
            value = self.d_value_input.value()
            mc.write_sign_word(self.socket, headdevice=f'd{address}', data_list=[value], signed_type=True)
            self.log_message(f"Đã ghi thanh ghi D{address} = {value}")
        except Exception as e:
            self.log_message(f"Lỗi ghi thanh ghi D: {str(e)}")
            
    def log_message(self, message):
        self.log_display.append(message)
        
    def closeEvent(self, event):
        if self.socket is not None:
            self.socket.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PLCInterface()
    window.show()
    sys.exit(app.exec_()) 