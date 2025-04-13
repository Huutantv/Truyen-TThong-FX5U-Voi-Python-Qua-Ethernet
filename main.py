import rk_mcprotocol as mc
import time

def main():
    HOST = '192.168.0.23'  # Địa chỉ IP của PLC
    PORT = 1025
    
    try:
        # Mở kết nối socket
        s = mc.open_socket(HOST, PORT)
        print(f"Đã kết nối thành công với PLC tại địa chỉ {HOST}")
        
        while True:
            try:
                # Ghi bit M0-M100 ON
                print("\nGhi bit M0-M100 ON:")
                print(mc.write_bit(s, headdevice='m0', data_list=[1]*101))
                
                # Đợi 1 giây
                time.sleep(1)
                
                # Ghi bit M0-M100 OFF
                print("\nGhi bit M0-M100 OFF:")
                print(mc.write_bit(s, headdevice='m0', data_list=[0]*101))
                
                # Ghi giá trị 0 vào D0
                print("\nGhi giá trị 0 vào D0:")
                print(mc.write_sign_word(s, headdevice='d1', data_list=[45], signed_type=False))
                
                # Đọc giá trị từ D20
                print("\nĐọc giá trị từ D20:")
                value = mc.read_sign_word(s, headdevice='d15', length=1, signed_type=False)
                print(f"Giá trị của D20: {value}")
                
                # Đợi 1 giây trước khi lặp lại
                time.sleep(1)
                
            except Exception as e:
                print(f"Lỗi trong vòng lặp: {str(e)}")
                time.sleep(1)  # Đợi 1 giây trước khi thử lại
                continue
            
    except Exception as e:
        print(f"Lỗi kết nối: {str(e)}")
    finally:
        if 's' in locals():
            s.close()
            print("Đã đóng kết nối với PLC")

if __name__ == "__main__":
    main()

