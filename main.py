# from monitor_agent import MonitorAgent
# from solution_agent import SolutionAgent
# from fix_agent import FixAgent
# import threading, time

# def start_monitor_agent():
#     try:
#         monitor = MonitorAgent(watch_folder="Hotel-demo")
#         monitor.run()
#     except Exception as e:
#         print(f"❌ Monitor Agent failed to start: {e}")

# def start_solution_agent():
#     try:
#         time.sleep(2)
#         solution = SolutionAgent()
#         solution.run()
#     except Exception as e:
#         print(f"❌ Solution Agent failed to start: {e}")

# def start_fix_agent():
#     try:
#         time.sleep(5)
#         fix = FixAgent()
#         fix.run()
#     except Exception as e:
#         print(f"❌ Fix Agent failed to start: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting Self-Healing AI System")
#     print("🛠️  Components: MonitorAgent, SolutionAgent, FixAgent\n")

#     # Start each agent in a separate thread
#     monitor_thread = threading.Thread(target=start_monitor_agent)
#     solution_thread = threading.Thread(target=start_solution_agent)
#     fix_thread = threading.Thread(target=start_fix_agent)

#     # Start the threads
#     monitor_thread.start()
#     solution_thread.start()
#     fix_thread.start()

#     # Optional: Wait for all threads to finish (they won't unless interrupted)
#     monitor_thread.join()
#     solution_thread.join()
#     fix_thread.join()


# from monitor_agent import MonitorAgent
# from solution_agent import SolutionAgent
# from fix_agent import FixAgent
# import time

# def run_monitor_agent():
#     try:
#         print("🔍 Running MonitorAgent...")
#         monitor = MonitorAgent(watch_folder="Hotel-demo")
#         monitor.scan_files()  # One-time scan
#         print("✅ MonitorAgent completed\n")
#     except Exception as e:
#         print(f"❌ MonitorAgent failed: {e}")

# def run_solution_agent():
#     try:
#         print("🧠 Running SolutionAgent...")
#         solution = SolutionAgent()
#         solution.run()
#         print("✅ SolutionAgent completed\n")
#     except Exception as e:
#         print(f"❌ SolutionAgent failed: {e}")

# def run_fix_agent():
#     try:
#         print("🔧 Running FixAgent...")
#         fix = FixAgent()
#         fix.run()
#         print("✅ FixAgent completed\n")
#     except Exception as e:
#         print(f"❌ FixAgent failed: {e}")

# if __name__ == "__main__":
#     print("🚀 Starting Self-Healing AI System (Continuous Mode)")
#     print("📋 Loop: MonitorAgent ➝ SolutionAgent ➝ FixAgent ➝ Repeat\n")

#     try:
#         while True:
#             run_monitor_agent()
#             time.sleep(2)

#             run_solution_agent()
#             time.sleep(2)

#             run_fix_agent()
#             time.sleep(2)

#             print("🔁 Cycle complete. Waiting before next round...\n")
#             time.sleep(5)  # wait before starting the next cycle

#     except KeyboardInterrupt:
#         print("\n🛑 Self-Healing loop stopped by user")



from monitor_agent import MonitorAgent
from solution_agent import SolutionAgent
from fix_agent import FixAgent

def run_monitor_agent():
    try:
        print("🔍 Running MonitorAgent...")
        monitor = MonitorAgent(watch_folder="Hotel-demo")
        monitor.scan_files()  # One-time scan
        print("✅ MonitorAgent completed\n")
    except Exception as e:
        print(f"❌ MonitorAgent failed: {e}")
        raise

def run_solution_agent():
    try:
        print("🧠 Running SolutionAgent...")
        solution = SolutionAgent()
        solution.run()
        print("✅ SolutionAgent completed\n")
    except Exception as e:
        print(f"❌ SolutionAgent failed: {e}")
        raise

def run_fix_agent():
    try:
        print("🔧 Running FixAgent...")
        fix = FixAgent()
        fix.run()
        print("✅ FixAgent completed\n")
    except Exception as e:
        print(f"❌ FixAgent failed: {e}")
        raise

if __name__ == "__main__":
    print("🚀 Starting Self-Healing AI System (One-time CI Mode)")
    print("📋 Running: Monitor ➝ Solution ➝ Fix ➝ Exit\n")

    try:
        run_monitor_agent()
        run_solution_agent()
        run_fix_agent()
        print("✅ Self-Healing AI run completed successfully.")
    except Exception as e:
        print("🛑 Self-Healing pipeline failed.")
        exit(1)
