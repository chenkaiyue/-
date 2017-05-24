#coding:utf-8
import math

#先进行一个转发表项的迁移，然后调用rerange优化各个链路的流表排布

class Policy:
    def __init__(self,sip,dip,sp,dp,action,redunt=False):
        self.sip = sip   #sip[5]  ip地址
        self.dip = dip
        self.sp = sp   #sp[2]  端口
        self.dp = dp
        self.action = action  #int     -1代表转发
        self.redunt = redunt
    def __str__(self):
        return  ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%r") % (self.sip[0],self.sip[1],self.sip[2],self.sip[3],self.sip[4],\
                                                                       self.dip[0],self.dip[1],self.dip[2],self.dip[3],self.dip[4],\
                                                                       self.sp[0],self.sp[1],self.dp[0],self.dp[1],\
                                                                       self.action,self.redunt)


class Switch:
    def __init__(self,policy_list):
        self.policy_list = policy_list




def conflict(p1,p2): #两个表项是否冲突
    p1_sip_start = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3]
    p1_sip_end = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3] + pow(2,(32-p1.sip[4]))-1
    p1_dip_start = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3]
    p1_dip_end = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3] + pow(2,(32-p1.dip[4]))-1
    p1_sp_start = p1.sp[0]
    p1_sp_end = p1.sp[1]
    p1_dp_start = p1.dp[0]
    p1_dp_end = p1.dp[1]

    p2_sip_start = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3]
    p2_sip_end = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3] + pow(2,(32-p2.sip[4]))-1
    p2_dip_start = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3]
    p2_dip_end = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3] + pow(2,(32-p2.dip[4]))-1
    p2_sp_start = p2.sp[0]
    p2_sp_end = p2.sp[1]
    p2_dp_start = p2.dp[0]
    p2_dp_end = p2.dp[1]


    if  (p1_sip_start <=p2_sip_end and p1_sip_end >= p2_sip_start) or  (p2_sip_start <= p1_sip_end and p2_sip_end >= p1_sip_start):
        if (p1_dip_start <=p2_dip_end and p1_dip_end >= p2_dip_start) or  (p2_dip_start <= p1_dip_end and p2_dip_end >= p1_dip_start):
            if (p1_dp_start <=p2_dp_end and p1_dp_end >= p2_dp_start) or  (p2_dp_start <= p1_dp_end and p2_dp_end >= p1_dp_start):
                if (p1_sp_start <=p2_sp_end and p1_sp_end >= p2_sp_start) or  (p2_sp_start <= p1_sp_end and p2_sp_end >= p1_sp_start):
                    return True
    return False


def findConflictMost_only_forwarding(route):
    # conflict_max_num = 0
    conflict_max_num = 0
    conflict_switch = -1
    conflict_policy = -1
    switch_num = len(route)
    for i in range(switch_num):
        for j in range(len(route[i])):
            if route[i][j].action != 1:
                continue
            else:
                conflict_num = conflict_with_same_switch(route[i][j],route[i])
            if conflict_num > conflict_max_num:
                conflict_max_num = conflict_num
                conflict_switch = i
                conflict_policy = j
    return [conflict_switch,conflict_policy,conflict_max_num]


# def findConflictMost_only_forwarding(route):
#     count = 0
#     conflict_max_num = 0
#     conflict_switch = 0
#     conflict_policy = 0
#     for i in range(len(route)):
#         for j in range(len(route[i])):
#             if route[i][j].action != 1:
#                 continue
#             else:
#                 print "`````````"
#                 for k in range(len(route[i])):
#                     if conflict(route[i][j],route[i][k]):
#                         count += 1
#                 count -= 1
#                     # print "111111111111111111111111"
#                     # print count
#                 if count > conflict_max_num:
#                     conflict_max_num = count
#                     conflict_switch = i
#                     conflict_policy = j
#                     print "i,j,conflict_max_num",i,j,conflict_max_num
#                 count = 0
#     print "conflict_switch,conflict_policy,conflict_max_num",conflict_switch,conflict_policy,conflict_max_num
#
#     return [conflict_switch,conflict_policy,conflict_max_num]

def findConflictMost(route):
    count = 0
    conflict_max_num = 0
    # conflict_switch = -1
    # conflict_policy = -1
    switch_num = len(route)
    for i in range(switch_num):
        for j in range(len(route[i])-1):
            for k in range(j+1,len(route[i])):
                if conflict(route[i][j],route[i][k]):
                    count += 1
            if count > conflict_max_num:
                conflict_max_num = count
                conflict_switch = i
                conflict_policy = j
            count = 0
    return [conflict_switch,conflict_policy,conflict_max_num]

def findConflictMost_notForwarding(route):
    # conflict_max_num = 0
    conflict_max_num = 0
    conflict_switch = -1
    conflict_policy = -1
    switch_num = len(route)
    for i in range(switch_num):
        for j in range(len(route[i])):
            conflict_num = conflict_with_same_switch(route[i][j],route[i])
            if conflict_num > conflict_max_num:
                conflict_max_num = conflict_num
                conflict_switch = i
                conflict_policy = j
            # count = 0
    return [conflict_switch,conflict_policy,conflict_max_num]

def addPolicy(route,policy,switch_id):
    route[switch_id].append(policy)

def delPolicy(route,conflict_switch_num,conflict_policy_num):
    del route[conflict_switch_num][conflict_policy_num]

def findIntersectionPart(p1,p2):
    p1_sip_start = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3]
    p1_sip_end = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3] + pow(2,(32-p1.sip[4]))-1
    p1_dip_start = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3]
    p1_dip_end = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3] + pow(2,(32-p1.dip[4]))-1
    p1_sp_start = p1.sp[0]
    p1_sp_end = p1.sp[1]
    p1_dp_start = p1.dp[0]
    p1_dp_end = p1.dp[1]

    p2_sip_start = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3]
    p2_sip_end = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3] + pow(2,(32-p2.sip[4]))-1
    p2_dip_start = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3]
    p2_dip_end = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3] + pow(2,(32-p2.dip[4]))-1
    p2_sp_start = p2.sp[0]
    p2_sp_end = p2.sp[1]
    p2_dp_start = p2.dp[0]
    p2_dp_end = p2.dp[1]


    new_sip = [0]*5
    new_dip = [0]*5
    new_sp = [0]*2
    new_dp = [0]*2


    if p1.sip[4] >= p2.sip[4]:
        new_sip[4] = p1.sip[4]
        new_sip[3] = p1.sip[3]
        new_sip[2] = p1.sip[2]
        new_sip[1] = p1.sip[1]
        new_sip[0] = p1.sip[0]
    else:
        new_sip[4] = p2.sip[4]
        new_sip[3] = p2.sip[3]
        new_sip[2] = p2.sip[2]
        new_sip[1] = p2.sip[1]
        new_sip[0] = p2.sip[0]


    if p1.dip[4] >= p2.dip[4]:
        new_dip[4] = p1.dip[4]
        new_dip[3] = p1.dip[3]
        new_dip[2] = p1.dip[2]
        new_dip[1] = p1.dip[1]
        new_dip[0] = p1.dip[0]
    else:
        new_dip[4] = p2.dip[4]
        new_dip[3] = p2.dip[3]
        new_dip[2] = p2.dip[2]
        new_dip[1] = p2.dip[1]
        new_dip[0] = p2.dip[0]


    if p1.sp[0] > p2.sp[0]:
        new_sp[0] = p1.sp[0]
    else:
        new_sp[0] = p2.sp[0]
    if p1.sp[1] > p2.sp[1]:
        new_sp[1] = p2.sp[1]
    else:
        new_sp[1] = p1.sp[1]

    if p1.dp[0] > p2.dp[0]:
        new_dp[0] = p1.dp[0]
    else:
        new_dp[0] = p2.dp[0]
    if p1.dp[1] > p2.dp[1]:
        new_dp[1] = p2.dp[1]
    else:
        new_dp[1] = p1.dp[1]

    action = p2.action
    new_policy = Policy(new_sip,new_dip,new_sp,new_dp,action,False)
    return new_policy

def findAllConflictPolicy(route,conflict_switch_num,conflict_policy_num):  #同一个route上与指定policy冲突的
    AllConflictPolicy = []
    conflict_policy = route[conflict_switch_num][conflict_policy_num]
    for i in range(len(route)):
        for j in range(len(route[i])):
            if conflict(conflict_policy,route[i][j]):
                #找出冲突的相交部分
                intersection_policy = findIntersectionPart(conflict_policy,route[i][j])
                AllConflictPolicy.append(intersection_policy)
    return AllConflictPolicy



def isInclude(p1,p2):
    p1_sip_start = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3]
    p1_sip_end = p1.sip[0]*pow(256,3)+p1.sip[1]*pow(256,2)+p1.sip[2]*256+ \
        p1.sip[3] + pow(2,(32-p1.sip[4]))-1
    p1_dip_start = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3]
    p1_dip_end = p1.dip[0]*pow(256,3)+p1.dip[1]*pow(256,2)+p1.dip[2]*256+ \
        p1.dip[3] + pow(2,(32-p1.dip[4]))-1
    p1_sp_start = p1.sp[0]
    p1_sp_end = p1.sp[1]
    p1_dp_start = p1.dp[0]
    p1_dp_end = p1.dp[1]

    p2_sip_start = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3]
    p2_sip_end = p2.sip[0]*pow(256,3)+p2.sip[1]*pow(256,2)+p2.sip[2]*256+ \
        p2.sip[3] + pow(2,(32-p2.sip[4]))-1
    p2_dip_start = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3]
    p2_dip_end = p2.dip[0]*pow(256,3)+p2.dip[1]*pow(256,2)+p2.dip[2]*256+ \
        p2.dip[3] + pow(2,(32-p2.dip[4]))-1
    p2_sp_start = p2.sp[0]
    p2_sp_end = p2.sp[1]
    p2_dp_start = p2.dp[0]
    p2_dp_end = p2.dp[1]

    if p1_sip_start >= p2_sip_start and p1_sip_end <= p2_sip_end and  p1_dip_start >= p2_dip_start and p1_dip_end <= p2_dip_end and p1_sp_start >= p2_sp_start and p1_sp_end <= p2_sp_end \
        and p1_dp_start >= p2_dp_start and p1_dp_end <= p2_dp_end and p1.action == p2.action:
        return 1
        #第一个范围小一些
    elif p2_sip_start >= p1_sip_start and p2_sip_end <= p1_sip_end and  p2_dip_start >= p1_dip_start and p2_dip_end <= p1_dip_end and p2_sp_start >= p1_sp_start and p2_sp_end <= p1_sp_end \
        and p2_dp_start >= p1_dp_start and p2_dp_end <= p1_dp_end and p1.action == p2.action:
        return 2
        #第二个范围小一些
    else:
        return 0


def jingJian(AllConflictPolicy):

    print "-------------------------"
    print len(AllConflictPolicy)
    # f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test0.txt",'w+')
    # for i in range(len(AllConflictPolicy)):
    #     s=""
    #     s = s + str(AllConflictPolicy[i])+"\n"
    #     f.write(s)
    # f.close()


    new_total = []
    i = 0
    #首先去除掉其中的转发表项，转发表项最后手动添加
    while (i < len(AllConflictPolicy)):
        if AllConflictPolicy[i].action == 1:
            del AllConflictPolicy[i]
        i += 1


    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test1.txt",'w+')
    for i in range(len(AllConflictPolicy)):
        s=""
        s = s + str(AllConflictPolicy[i])+"\n"
        f.write(s)
    f.close()
    print "1ok"

    return AllConflictPolicy


    '''
    # 将redunt的排除
    j=0
    while j < len(AllConflictPolicy):
    # for j in range(len(AllConflictPolicy)):
    #     for k in range(len(AllConflictPolicy)):
        k = 0
        while k < len(AllConflictPolicy):
            if j == k :
                k += 1
                continue
            if isInclude(AllConflictPolicy[j],AllConflictPolicy[k]) == 1:
                AllConflictPolicy[j].redunt = True
                # new_total.append(AllConflictPolicy[j])
            if isInclude(AllConflictPolicy[j],AllConflictPolicy[k]) == 2:
                AllConflictPolicy[k].redunt = True
                # new_total.append(AllConflictPolicy[i])
            k += 1
        j += 1
    '''

    '''
    for j in range(len(AllConflictPolicy)):
        for k in range(len(AllConflictPolicy)):
        # k = 0
        # while k < len(AllConflictPolicy):
            if j == k :
                continue
            if isInclude(AllConflictPolicy[j],AllConflictPolicy[k]) == 1:
                AllConflictPolicy[j].redunt = True
                # new_total.append(AllConflictPolicy[j])
            if isInclude(AllConflictPolicy[j],AllConflictPolicy[k]) == 2:
                AllConflictPolicy[k].redunt = True
                # new_total.append(AllConflictPolicy[i])

    #去除转发表项，表项已经表明是否redunt
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test2.txt",'w+')
    for i in range(len(AllConflictPolicy)):
        s=""
        s = s + str(AllConflictPolicy[i])+"\n"
        f.write(s)
    f.close()

    for l in range(len(AllConflictPolicy)):
        if AllConflictPolicy[l].redunt == False:
            new_total.append(AllConflictPolicy[l])

    #经过合并之后的只有False的项
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test3.txt",'w+')
    for i in range(len(new_total)):
        s=""
        s = s + str(new_total[i])+"\n"
        f.write(s)
    f.close()
    return new_total
    '''

def find_max_policy_num(route):
        m = 0
        j = -1
        total = 0
        for i in range(len(route)):
            total += len(route[i])
            if len(route[i]) > m:
                m = len(route[i])
                j = i
        return [j,m,total]

#表项和同一个交换机中的冲突的个数
def conflict_with_same_switch(p,policy_list):
    conflict_num = 0
    for i in range(len(policy_list)):
        if conflict(p,policy_list[i]):
            conflict_num += 1
    return conflict_num-1

#表项和其他交换机中的冲突的个数
def conflict_with_other_switch(p,policy_list):
    conflict_num = 0
    for i in range(len(policy_list)):
        if conflict(p,policy_list[i]):
            conflict_num += 1
    return conflict_num

#首先选取冲突最大的进行迁移，之后遍历每一个表项，只要可以减少冲突数，就进行迁移
def reRange(route):
    flag = True
    while flag:
        print"111111111111111111"
        [conflict_switch_num,conflict_policy_num,conflict_max_num] = findConflictMost_notForwarding(route)
        print "conflict_max_num"
        print conflict_max_num
        print "conflict_switch_num"
        print conflict_switch_num
        conflict_policy = route[conflict_switch_num][conflict_policy_num]
        # if route[conflict_switch_num][conflict_policy_num].action == 1:
        #     print "yes"
        if route[conflict_switch_num][conflict_policy_num].action != 1: #不是转发操作，是一般的操作
            print "yesyes"
            available_switch_list = route ## 这里做了简化   迁移到的新交换机上的比原有多的流与迁移过去的action不冲突；\
            # 对于向流的流向方向（向后）移动：需要比较下一个迁移目地交换机上的前一个交换机（除了原本这个迁移表项自己所在的）的所有流是是否和这个表项冲突，如果冲突，则不能移动
            # 应该是对应每条表项都有一个自己的avaliable_switch的列表可供移动,然后在这里移动选择冲突数目最小的，这里应该对应的是选出来的这个最多冲突表项的可移动交换机范围
            min_confict = 10000000000

            # migto_switch_num
            for i in range(len(available_switch_list)):
                confict_if_mig = 0
                for j in range(len(available_switch_list[i])):
                    if conflict(conflict_policy,available_switch_list[i][j]):
                        confict_if_mig += 1
                if confict_if_mig < min_confict:
                    min_confict = confict_if_mig
                    migto_switch_num = i
            print "min_confict"
            print min_confict
            if min_confict < conflict_max_num:
                flag = True
                # addPolicy(available_switch_list,conflict_policy,migto_switch_num)
                # delPolicy(available_switch_list,conflict_switch_num,conflict_policy_num)
                addPolicy(route,conflict_policy,migto_switch_num)
                delPolicy(route,conflict_switch_num,conflict_policy_num)
            else:
                flag = False
    print "1111111111111111111111111"
    print len(route[0])
    print len(route[1])
    print len(route[2])

    [j,m,total]= find_max_policy_num(route)
    # while(count_no_de > 100 or (m-total/len(route)) <30):
    flag = True
    while(flag):
        print "222222222222222222222222"
        flag = False
        count = 0
        i,j=0,0
        route_copy = route
        # for i in xrange(len(route_copy)):
        while i < len(route_copy):
            while j < len(route_copy[i]):
            # for j in xrange(len(route_copy[i])):
                conflict_same = conflict_with_same_switch(route_copy[i][j],route_copy[i])
                min_different = 1000000000
                for k in range(len(route_copy)):
                    conflict_different = conflict_with_other_switch(route_copy[i][j],route_copy[k])
                    if conflict_different < min_different:
                        min_different = conflict_different
                        min_to_switch = k
                if min_different < conflict_same:
                    addPolicy(route,route[i][j],min_to_switch)
                    delPolicy(route,i,j)
                    route_copy = route
                    flag = True
                j += 1
            i += 1

if __name__ == "__main__":
    policy_list3,policy_list4,policy_list5,policy_list8,policy_list9,policy_list10,policy_list8_withoutf,policy_list9_withoutf,policy_list10_withoutf = [],[],[],[],[],[],[],[],[]
    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_3.txt","r+") as f1:
        for line in f1:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list3.append(p)
    f1.close()
    print len(policy_list3)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_4.txt","r+") as f2:
        for line in f2:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list4.append(p)
    f2.close()
    print len(policy_list4)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_5.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list5.append(p)
    f3.close()
    print len(policy_list5)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_8.txt","r+") as f1:
        for line in f1:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list8.append(p)
    f1.close()
    print len(policy_list8)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_9.txt","r+") as f2:
        for line in f2:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list9.append(p)
    f2.close()
    print len(policy_list9)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_10.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list10.append(p)
    f3.close()
    print len(policy_list10)

    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_10.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list10.append(p)
    f3.close()
    print len(policy_list10)

    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_8_nofor.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list8_withoutf.append(p)
    f3.close()
    print len(policy_list8_withoutf)

    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_9_nofor.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list9_withoutf.append(p)
    f3.close()
    print len(policy_list9_withoutf)


    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_10_nofor.txt","r+") as f3:
        for line in f3:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp=[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action = int(l[i])
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list10_withoutf.append(p)
    f3.close()
    print len(policy_list10_withoutf)


    # p1 = Policy([58,80,0,0,30],[58,80,0,3,32],[3,10],[20,30],1)
    # p2 = Policy([58,80,0,3,32],[58,80,0,0,30],[5,15],[10,19],1)
    # print conflict(p1,p2)
    route1,route2,route2_withoutf = [],[],[]
    route1.append(policy_list3)  #存储7个交换机的线路1 蓝色1    Policy policy_list[5000];
    route1.append(policy_list4)
    route1.append(policy_list5)
    route2.append(policy_list8)  #存储7个交换机的线路1 蓝色1    Policy policy_list[5000];
    route2.append(policy_list9)
    route2.append(policy_list10)
    route2_withoutf.append(policy_list8_withoutf)
    route2_withoutf.append(policy_list9_withoutf)
    route2_withoutf.append(policy_list10_withoutf)


    #找出所有和转发表项冲突的
    print "len(route1[0])"
    print len(route1[0])
    [conflict_switch_num,conflict_policy_num,conflict_max_num] = findConflictMost_only_forwarding(route1)
    # conflict_policy = route1[conflict_switch_num][conflict_policy_num]
    # print "conflict_policy.action"
    # print conflict_policy.action
    print "conflict_switch_num"
    print conflict_switch_num
    print "conflict_policy_num"
    print conflict_policy_num
    print "conflict_max_num"
    print conflict_max_num

    # print conflict_with_same_switch(conflict_policy,route1[0])

    AllConflictPolicy = findAllConflictPolicy(route1,conflict_switch_num,conflict_policy_num)
    print "len(AllConflictPolicy)"
    print len(AllConflictPolicy)
    AllConflictPolicy = jingJian(AllConflictPolicy)
    print "xuyaodaizoudebiaoxiangshuliang "
    print len(AllConflictPolicy)



    # 转发表项的迁移
    '''
    for i in range(len(AllConflictPolicy)):
        if AllConflictPolicy[i].redunt == True:
            continue
        for j in range(len(route2)):
            for k in range(len(route2[j])):
                if route2[i][j].redunt == True:
                    continue
                else:
                    if isInclude(AllConflictPolicy[i],route2[j][k]) == 1:
                        AllConflictPolicy[i].redunt = True
                    elif isInclude(AllConflictPolicy[i],route2[j][k]) == 2:
                        del route2[j][k]

    print len(AllConflictPolicy)
    '''


    #将剩下的表项都添加在route2_withoutf中
    print "******************"
    print len(route2_withoutf[0])

    for i in range(len(AllConflictPolicy)):
        addPolicy(route2_withoutf,AllConflictPolicy[i],0)

    print "***********************"
    print len(route2_withoutf[0])



    # reRange(route1)
    reRange(route2_withoutf)

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r3_8rerange.txt",'w+')
    for i in range(len(route2_withoutf[0])):
        s=""
        s = s + str(route2_withoutf[0][i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r3_9rerange.txt",'w+')
    for i in range(len(route2_withoutf[1])):
        s=""
        s = s + str(route2_withoutf[1][i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r3_10rerange.txt",'w+')
    for i in range(len(route2_withoutf[2])):
        s=""
        s = s + str(route2_withoutf[2][i])+"\n"
        f.write(s)
    f.close()


'''



    reRange(route1)
    reRange(route2)



    print "************"
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_8rerange.txt",'w+')
    for i in range(len(policy_list8)):
        s=""
        s = s + str(policy_list8[i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_9rerange.txt",'w+')
    for i in range(len(policy_list9)):
        s=""
        s = s + str(policy_list9[i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_10rerange.txt",'w+')
    for i in range(len(policy_list10)):
        s=""
        s = s + str(policy_list10[i])+"\n"
        f.write(s)
    f.close()



    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_3rerange.txt",'w+')
    for i in range(len(policy_list3)):
        s=""
        s = s + str(policy_list3[i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_4rerange.txt",'w+')
    for i in range(len(policy_list4)):
        s=""
        s = s + str(policy_list4[i])+"\n"
        f.write(s)
    f.close()

    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_5rerange.txt",'w+')
    for i in range(len(policy_list5)):
        s=""
        s = s + str(policy_list5[i])+"\n"
        f.write(s)
    f.close()


    print len(policy_list3)
    print len(policy_list4)
    print len(policy_list5)
    print len(policy_list8)
    print len(policy_list9)
    print len(policy_list10)
    # reRange(route2)

'''



