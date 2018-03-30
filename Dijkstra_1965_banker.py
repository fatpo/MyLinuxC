# -*- coding: UTF-8 -*-


# 初始化各数据结构
resource_cnt = 3
Available = [3, 3, 2]  # 可利用各资源总数
Max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]  # 各进程最大需求资源数
Allocation = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]  # 已分配各进程的资源数
Need = [[7, 4, 3], [1, 2, 2], [6, 0, 0], [0, 1, 1], [4, 3, 1]]  # 各进程尚需的资源数
Finish = [False, False, False, False, False]
p = [5, 3, 2, 1, 9]


def compare(Available, Process_Need, resource_cnt):
    """
    比较a 和 b 的 resource_item项目，是否都符合资源 a > b
    :param Available: 当前系统拥有的资源列表，[1,2, 3]
    :param Process_Need: 当前进程需要的资源列表， [4,5,6]
    :param resource_cnt: 资源的种类，比如3
    :return:
    """
    for x in range(0, resource_cnt):  # 进行列表对应元素的比较
        if (int(Available[x]) < int(Process_Need[x])):  # 一旦出现供不应求的情况即返回False
            return False
    return True  # 如果符合条件即返回True


already_done_cnt = 0
flag = False
good_order_lst = []

while already_done_cnt < len(p):
    """
        算法：
        1、如果找一圈，没一个能打的，就放弃，说明死锁；
        2、如果找到一个能到的一个满足资源的进程p，那么顺水推舟，能满足多少是多少，反正本轮有收获了，True，满足继续下一轮的条件。
        3、while 不断重复1、2步骤直到不满足步骤1 或者 already_done_cnt == len(p) 为止。

    """
    flag = False
    for i in range(len(p)):
        if not Finish[i]:
            print "比较，need=%s, Available=%s" % (Need[i], Available)
            if not compare(Available, Need[i], resource_cnt):
                print "比较不通过，跳过..."
            else:
                print "比较通过，资源回归.."
                for j in range(resource_cnt):
                    Available[j] += Allocation[i][j]
                print "回归后, Available=%s" % Available
                Finish[i] = True
                already_done_cnt += 1
                flag = True
                good_order_lst.append(i)
    if not flag:
        print "哎，找了一圈，都没一个符合的...说明被死锁了..."
        break

if flag:
    print "检查通过"
    print "正确的任务顺序：", good_order_lst
else:
    print "检查不通过"
