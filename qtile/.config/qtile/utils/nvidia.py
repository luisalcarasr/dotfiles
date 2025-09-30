import subprocess

# (($(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | awk '{ print $1}') * 100 / $(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | awk '{ print $1}')))

def nvidia_smi(query):
    nvidia_smi = subprocess.Popen(
        ["nvidia-smi", f"--query-gpu={query}", "--format=csv,noheader,nounits"],
        stdout = subprocess.PIPE
    ) 
    output, errors = nvidia_smi.communicate();
    return output.decode('UTF-8').strip();

def get_used_memory():
    return int(nvidia_smi("memory.used")) * 100 / int(nvidia_smi("memory.total"))

def get_used_gpu(): 
    return int(nvidia_smi("utilization.gpu"));
