import subprocess
import socket
import time
import re

def get_ssid_linux():
    try:
        result = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
        return result if result else "Unknown"
    except subprocess.CalledProcessError:
        return "Unknown"

def get_latency(host="8.8.8.8"):
    try:
        output = subprocess.check_output(["ping", "-c", "1", host], stderr=subprocess.STDOUT, text=True)
        match = re.search(r'time=(\d+\.\d+)', output)
        if match:
            return float(match.group(1))
    except subprocess.CalledProcessError:
        return None

def is_reachable(host, port=80, timeout=2):
    try:
        socket.setdefaulttimeout(timeout)
        with socket.create_connection((host, port)):
            return True
    except:
        return False

def print_wifi_status():
    ssid = get_ssid_linux()
    latency = get_latency()

    print(f"📶 Connected Wi-Fi: {ssid}")
    if latency is not None:
        print(f"📡 Latency: {latency:.2f} ms")
    else:
        print("📡 Latency: ❌ Ping failed")

    google_status = "✅ Reachable" if is_reachable("google.com") else "❌ Not Reachable"
    github_status = "✅ Reachable" if is_reachable("github.com") else "❌ Not Reachable"

    print(f"🌍 Google: {google_status}")
    print(f"🐙 GitHub: {github_status}")


# Example: Run once every 2 seconds
if __name__ == "__main__":
    try:
        while True:
            print("\033c", end="")  # Clear terminal
            print_wifi_status()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopped.")
