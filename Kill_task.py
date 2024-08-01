def kill_task(name):
    pid = get_pid(name)
    if pid:
        os.kill(pid, 9)
        print(f"Task '{name}' (PID: {pid}) has been killed.")
    else:
        print(f"Task '{name}' not found.")
