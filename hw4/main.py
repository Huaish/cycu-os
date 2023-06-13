# Page Replacement
import os

def list_to_string(list):
    return ''.join([str(elem) for elem in list[::-1]])

def FIFO(frame_size, pages):
    info_list = []
    frames = []
    page_fault,page_replace = 0,0
    for i in range(len(pages)):
        info = str(pages[i]) + "\t"
        if pages[i] not in frames:
            page_fault += 1
            if len(frames) < frame_size:
                frames.append(pages[i])
            else:
                frames.pop(0)
                frames.append(pages[i])
                page_replace += 1
            info += list_to_string(frames) + "\tF"
        else:
            info += list_to_string(frames)
        info_list.append(info)
    return info_list, page_fault, page_replace

def LRU(frame_size, pages):
    info_list = []
    frames = []
    page_fault,page_replace = 0,0
    for i in range(len(pages)):
        info = str(pages[i]) + "\t"
        if pages[i] not in frames:
            page_fault += 1
            if len(frames) < frame_size:
                frames.append(pages[i])
            else:
                frames.pop(0)
                frames.append(pages[i])
                page_replace += 1
            info += list_to_string(frames) + "\tF"
        else:
            frames.remove(pages[i])
            frames.append(pages[i])
            info += list_to_string(frames)
        info_list.append(info)
    return info_list, page_fault, page_replace

def LFU_FIFO(frame_size, pages):
    info_list = []
    frames = []
    page_cnt = {}
    page_fault,page_replace = 0,0
    for i in range(len(pages)):
        info = str(pages[i]) + "\t"
        if pages[i] not in frames:
            page_fault += 1
            if len(frames) < frame_size:
                frames.append(pages[i])
                page_cnt[pages[i]] = 1
            else:
                # remove the least recently used page
                min_page = frames[0]
                for page in frames:
                    if page_cnt[page] < page_cnt[min_page]:
                        min_page = page
                frames.remove(min_page)
                frames.append(pages[i])
                page_replace += 1
                page_cnt[pages[i]] = 1
            info += list_to_string(frames) + "\tF"
        else:
            page_cnt[pages[i]] += 1
            info += list_to_string(frames)
        info_list.append(info)
    return info_list, page_fault, page_replace

def MFU_FIFO(frame_size, pages):
    info_list = []
    frames = []
    page_cnt = {}
    page_fault,page_replace = 0,0
    for i in range(len(pages)):
        info = str(pages[i]) + "\t"
        if pages[i] not in frames:
            page_fault += 1
            if len(frames) < frame_size:
                frames.append(pages[i])
                page_cnt[pages[i]] = 1
            else:
                # remove the most frequently used page
                max_page = frames[0]
                for page in frames:
                    if page_cnt[page] > page_cnt[max_page]:
                        max_page = page
                frames.remove(max_page)
                frames.append(pages[i])
                page_replace += 1
                page_cnt[pages[i]] = 1
            info += list_to_string(frames) + "\tF"
        else:
            page_cnt[pages[i]] += 1
            info += list_to_string(frames)
        info_list.append(info)
    return info_list, page_fault, page_replace

def LFU_LRU(frame_size, pages):
    info_list = []
    frames = []
    page_cnt = {}
    page_fault,page_replace = 0,0
    for i in range(len(pages)):
        info = str(pages[i]) + "\t"
        if pages[i] not in frames:
            page_fault += 1
            if len(frames) < frame_size:
                frames.append(pages[i])
                page_cnt[pages[i]] = 1
            else:
                # remove the least frequently used page
                min_page = frames[0]
                for page in frames:
                    if page_cnt[page] < page_cnt[min_page]:
                        min_page = page
                frames.remove(min_page)
                frames.append(pages[i])
                page_replace += 1
                page_cnt[pages[i]] = 1
            info += list_to_string(frames) + "\tF"
        else:
            frames.remove(pages[i])
            frames.append(pages[i])
            page_cnt[pages[i]] += 1
            info += list_to_string(frames)
        info_list.append(info)
    return info_list, page_fault, page_replace

if __name__ == '__main__':
    print("Please enter the File name (eg. input1、input1.txt): ")
    path, file = os.path.split(input())
    input_file = file.split(".")[0] + ".txt"
    # output_file = "out_" + input_file
    output_file = "output_" + input_file

    TITLE = ['','FIFO','LRU','Least Frequently Used Page Replacement', 'Most Frequently Used Page Replacement ', 'Least Frequently Used LRU Page Replacement']
    METOHDS = [None,FIFO,LRU,LFU_FIFO,MFU_FIFO,LFU_LRU]
    method = 0
    frame_size = 3
    pages = ""

    with open(os.path.join(path, input_file), 'r') as f:
        line = f.readline()
        method = int(line.split(" ")[0])
        frame_size = int(line.split(" ")[1])
        pages = [int(digit) for digit in str(f.readline().strip())]

    if method > 0 and method < 6:
        info_list, page_fault, page_replace = METOHDS[method](frame_size, pages)
        with open(os.path.join(path, output_file), 'w') as f:
            f.write("--------------{}-----------------------\n".format(TITLE[method]))
            for info in info_list:
                f.write(info + "\n")
            f.write("Page Fault = {}  Page Replaces = {}  Page Frames = {}\n".format(page_fault, page_replace, frame_size))
    elif method == 6:
        # all methods
        for i in range(1,6):
            info_list, page_fault, page_replace = METOHDS[i](frame_size, pages)
            with open(os.path.join(path, output_file), 'a') as f:
                f.write("--------------{}-----------------------\n".format(TITLE[i]))
                for info in info_list:
                    f.write(info + "\n")
                f.write("Page Fault = {}  Page Replaces = {}  Page Frames = {}\n".format(page_fault, page_replace, frame_size))
                if i != 5:
                    f.write("\n")

