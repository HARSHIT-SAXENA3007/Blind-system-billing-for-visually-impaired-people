def get_pid(name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == name:
            return proc.pid
    return None
