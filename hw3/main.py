import copy
import os
import sys

class Process:
    def __init__(self, pid, burst_time, arrival_time, priority,life_time):
        self.pid = pid
        self.estimated_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority
        self.burst_time = burst_time
        self.life_time = life_time
        self.waiting_time = 0
        self.turnaround_time = 0

class Scheduler:
    def __init__(self, process_queue, algorithm='FCFS', time_slice=1):
        self.current_time = 0
        self.running_process = None
        self.process_queue = process_queue
        self.ready_queue = []
        self.finished_queue = []
        self.gantt_chart = []
        self.algorithm = algorithm

        self.process_queue.sort(key=lambda x: x.pid)
        self.process_queue.sort(key=lambda x: x.arrival_time)

        self.scheduled_algorithm = {
            # method: [key, isPreemptive, reverse, time_slice]
            'FCFS': [(lambda x: x.arrival_time), False, False, 1],
            'RR': [(lambda x: 0), True, False, time_slice],
            'SJF': [(lambda x: x.burst_time), False, False, 1],
            'SRTF': [(lambda x: x.burst_time), True, False, sys.maxsize],
            'HRRN': [(lambda x: (x.burst_time + self.current_time - x.arrival_time) / x.burst_time), False, True, 1],
            'PPRR': [(lambda x: x.priority), True, False, time_slice]
        }

        self.key, self.isPreemptive, self.reverse, self.time_slice = self.scheduled_algorithm[algorithm]

    # 將已到達的進程加入就緒隊列
    def add_to_ready_queue(self):
        while len(self.process_queue) > 0:
            if self.process_queue[0].arrival_time <= self.current_time:
                self.ready_queue.append(self.process_queue.pop(0))
            else:
                break

    # 取得就緒隊列中進程
    def get_next_process(self):
        if len(self.ready_queue) > 0:
            self.ready_queue.sort(key=self.key, reverse=self.reverse)
            if self.running_process == None:
                self.running_process = self.ready_queue.pop(0)
                self.running_process.life_time = self.time_slice
            elif self.isPreemptive:
                next = self.ready_queue[0]
                if self.key(next) < self.key(self.running_process) or \
                    (self.key(next) == self.key(self.running_process) and self.running_process.life_time <= 0):
                    self.ready_queue.append(self.running_process)
                    self.running_process = self.ready_queue.pop(0)
                    self.running_process.life_time = self.time_slice
                
    # 執行進程
    def run_process(self):
        if self.running_process == None:
            self.gantt_chart.append('-')
        else:
            self.gantt_chart.append(chr(self.running_process.pid - 10 + 65) if self.running_process.pid > 9 else str(self.running_process.pid))
            self.running_process.burst_time -= 1
            self.running_process.life_time -= 1
            if self.running_process.burst_time == 0:
                self.running_process.turnaround_time = self.current_time + 1 - self.running_process.arrival_time
                self.running_process.waiting_time = self.running_process.turnaround_time - self.running_process.estimated_time
                self.finished_queue.append(self.running_process)
                self.running_process = None
    
    def run(self):
        while len(self.process_queue) > 0 or len(self.ready_queue) > 0 or self.running_process != None:
            self.add_to_ready_queue()
            self.get_next_process()
            self.run_process()
            self.current_time += 1

    def get_finished_processes(self):
        return self.finished_queue
    
    def get_gantt_chart(self):
        return self.gantt_chart
    
def execute(input_file, output_file, folder="./", methods=[], time_slice=1, title=''):
    # 讀取進程資訊
    process_queue = []
    with open(os.path.join(folder, input_file), 'r') as f:
        f.readline()
        f.readline()
        while True:
            line = f.readline()
            if not line:
                break
            process_info = line.strip().split()
            if len(process_info) != 4:
                continue
            process = {
                'id': int(process_info[0]),
                'burst_time': int(process_info[1]),
                'arrival_time': int(process_info[2]),
                'priority': int(process_info[3])
            }
            process_queue.append(Process(process['id'], process['burst_time'], process['arrival_time'], process['priority'], time_slice))

    # 建立並執行排程
    scheduler_list = []
    for method in methods:
        processes = copy.deepcopy(process_queue)
        scheduler = Scheduler(processes, method, time_slice)
        scheduler.run()
        scheduler.finished_queue.sort(key=lambda x: x.pid)
        scheduler_list.append(scheduler)

    # 輸出結果
    process_queue.sort(key=lambda x: x.pid)
    with open(os.path.join(folder, output_file), 'w') as f:      
        f.write(title + "\n")
        
        # Gantt Chart
        for method, scheduler in zip(methods, scheduler_list):
            f.write("=={:>12}==".format(method) + "\n")
            f.write("".join(scheduler.get_gantt_chart()) + "\n")
        f.write("="*59 + "\n\n")

        # Waiting Time
        f.write("Waiting Time\n")
        f.write("ID\t" + "\t".join(methods) + "\n")
        f.write("="*59 + "\n")
        for i in range(len(process_queue)):
            f.write("{}\t".format(process_queue[i].pid))
            for j, scheduler in enumerate(scheduler_list):
                f.write("{}".format(scheduler.get_finished_processes()[i].waiting_time))
                if j != len(scheduler_list) - 1:
                    f.write("\t")
            f.write("\n")
        f.write("="*59 + "\n\n")

        # Turnaround Time
        f.write("Turnaround Time\n")
        f.write("ID\t" + "\t".join(methods) + "\n")
        f.write("="*59 + "\n")
        for i in range(len(process_queue)):
            f.write("{}\t".format(process_queue[i].pid))
            for j, scheduler in enumerate(scheduler_list):
                f.write("{}".format(scheduler.get_finished_processes()[i].turnaround_time))
                if j != len(scheduler_list) - 1:
                    f.write("\t")
            f.write("\n")
        f.write("="*59 + "\n\n")


if __name__ == '__main__':
    print("Please enter the File name (eg. input1、input1.txt): ")
    path, file = os.path.split(input())
    input_file = file.split(".")[0] + ".txt"
    output_file = "out_" + input_file

    TITLE = ['','FCFS', 'RR', 'SJF', 'SRTF', 'HRRN', 'Priority RR', 'All']
    METHODS = ['','FCFS', 'RR', 'SJF', 'SRTF', 'HRRN', 'PPRR']
    method = []
    time_slice = 1
    title = ''
    with open(os.path.join(path, input_file), 'r') as f:
        line = f.readline().strip().split()
        method = int(line[0])
        title = TITLE[method]
        if method == 7:
            method = METHODS[1:]
        else:
            method = [METHODS[method]]
        time_slice = int(line[1])

    execute(input_file, output_file, path, method, time_slice, title)