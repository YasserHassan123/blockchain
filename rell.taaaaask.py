import concurrent.futures
import time

class SecurityTask:
    def __init__(self, name, period, execution_time):
        self.name = name
        self.period = period  # تكرار المهمة (بتكرر كل كام ثانية)
        self.execution_time = execution_time
        self.next_start_time = 0
        self.deadline = self.period  # الموعد النهائي الأول للمهمة

    def update_deadline(self):
        self.deadline = self.next_start_time + self.period

    def run(self):
        print(f"[{self.name}] started execution at {time.time() - start_time:.2f}s (Deadline: {self.deadline:.2f}s)")
        time.sleep(self.execution_time)
        print(f"[{self.name}] finished execution at {time.time() - start_time:.2f}s")

# قائمة المهام الأمنية
security_tasks = [
    SecurityTask("Virus Scan", period=4, execution_time=1.5),
    SecurityTask("Network Security Check", period=5, execution_time=2),
    SecurityTask("Encryption Task", period=7, execution_time=2.5),
]

start_time = time.time()

def scheduler():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while time.time() - start_time < 20:
            current_time = time.time() - start_time

            # نجمع المهام الجاهزة حاليًا
            ready_tasks = [
                task for task in security_tasks
                if current_time >= task.next_start_time
            ]

            # نعيد ترتيب المهام بناءً على أقرب موعد نهائي (EDF)
            ready_tasks.sort(key=lambda t: t.deadline)

            for task in ready_tasks:
                executor.submit(task.run)
                task.next_start_time += task.period
                task.update_deadline()

            time.sleep(0.1)

scheduler()
