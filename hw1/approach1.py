import datetime
import time


def bubble_sort(data):
    """對一個 list 進行 BubbleSort"""
    n = len(data)
    for i in range(n):
        for j in range(n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return data

def sort_approach1(input_file_name, k):
    with open(input_file_name, 'r') as f:
        data = [int(line) for line in f.readlines()]

    # 使用多進程進行排序和合併
    start_time = time.time()
    result = bubble_sort(data)
    end_time = time.time()

    return result, end_time-start_time

if __name__ == '__main__':
    k = 10
    input_file_name = 'input/input_1w.txt'
    output_file_name = 'input_1w_output1.txt'
    result, cpu_time = sort_approach1(input_file_name, k)

    with open(output_file_name, 'w') as f:
        f.write('Sort : \n')
        f.write('\n'.join([str(x) for x in result]))
        f.write('\nCPU Time : ' + str(cpu_time))
        f.write('\nOutput Time : ')
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        offset = now.strftime("%z")
        offset_with_colon = offset[:3] + ":" + offset[3:]
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S.%f") + offset_with_colon
        f.write(formatted_time)