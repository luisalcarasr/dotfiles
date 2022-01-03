import socket
import subprocess

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def get_essid(interface):
    iwconfig = subprocess.Popen(
        ["iwconfig", interface],
        stdout = subprocess.PIPE
    ) 
    output, errors = iwconfig.communicate();
    return output.decode('UTF-8').split('"')[1];
