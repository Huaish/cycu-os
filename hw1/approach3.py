import multiprocessing
import time
import datetime


def bubble_sort(data):
    """對一個 list 進行 BubbleSort"""
    n = len(data)
    for i in range(n):
        for j in range(n-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
    return data


def merge(left, right):
    """合併兩個已經排序好的 list"""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def sort_worker(data):
    """將一個 chunk 的數據進行 BubbleSort"""
    return bubble_sort(data)


def merge_worker(results):
    """將多個已經排序好的 chunk 合併成一個排序好的序列"""
    while len(results) > 1:
        left = results.pop(0)
        right = results.pop(0)
        merged = merge(left, right)
        results.append(merged)
    return results[0]


def multi_process_sort(data, k):
    """將數據切分成 k 個 chunks，並使用 k-1 個 processes 進行排序和合併"""
    chunk_size = len(data) // k
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # 使用 k 個 processes 進行 BubbleSort
    with multiprocessing.Pool(processes=k) as pool:
        bubble_sorted_chunks = pool.map(sort_worker, chunks)

    # 使用 k-1 個 processes 進行 MergeSort
    while len(bubble_sorted_chunks) > 1:
        with multiprocessing.Pool(k-1) as pool:
            merged_chunks = pool.map(merge_worker, [
                                     bubble_sorted_chunks[i:i+2] for i in range(0, len(bubble_sorted_chunks), 2)])
        bubble_sorted_chunks = merged_chunks

    return bubble_sorted_chunks[0]


def sort_approach3(input_file_name, k):
    with open(input_file_name, 'r') as f:
        data = [int(line) for line in f.readlines()]

    # 使用多進程進行排序和合併
    start_time = time.time()
    result = multi_process_sort(data, k)
    end_time = time.time()

    return result, end_time-start_time


if __name__ == '__main__':
    k = 10
    input_file_name = 'input/input_1w.txt'
    output_file_name = 'input_1w_output3.txt'
    result, cpu_time = sort_approach3(input_file_name, k)

    with open(output_file_name, 'w') as f:
        f.write('Sort : \n')
        f.write('\n'.join([str(x) for x in result]))
        f.write('\nCPU Time : ' + str(cpu_time))
        f.write('\nOutput Time : ')
        now = datetime.datetime.now(
            datetime.timezone(datetime.timedelta(hours=8)))
        offset = now.strftime("%z")
        offset_with_colon = offset[:3] + ":" + offset[3:]
        formatted_time = now.strftime(
            "%Y-%m-%d %H:%M:%S.%f") + offset_with_colon
        f.write(formatted_time)
