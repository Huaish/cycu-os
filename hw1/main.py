import datetime
from approach1 import sort_approach1
from approach2 import sort_approach2
from approach3 import sort_approach3
from approach4 import sort_approach4
import time

medthods = [sort_approach1, sort_approach2, sort_approach3, sort_approach4]
def main():
    print('請輸入檔案名稱：')
    input_file_name = input()
    print('請輸入要切成幾份：')
    k = int(input())
    print('請輸入方法編號：(方法1, 方法2, 方法3, 方法4)')
    method = input()
    output_file_name = 'output/' + input_file_name + '_output' + method + '.txt'
    input_file_name = 'input/' + input_file_name + '.txt'
    result, cpu_time = medthods[int(method) - 1](input_file_name, k)

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

if __name__ == '__main__':
    main()