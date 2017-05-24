# -*- encoding:utf-8 -*-

# 在一个交换年级中进行order的升序的存贮
import math
import random

class Policy:
    def __init__(self,sip,dip,sp,dp,action,redunt=False):
        self.sip = sip   #sip[5]  ip地址
        self.dip = dip
        self.sp = sp   #sp[2]  端口
        self.dp = dp
        self.action = action  #int     -1代表转发
        self.redunt = redunt
    def __str__(self):
        return  ("%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%d,%s,%r") % (self.sip[0],self.sip[1],self.sip[2],self.sip[3],self.sip[4],\
                                                                       self.dip[0],self.dip[1],self.dip[2],self.dip[3],self.dip[4],\
                                                                       self.sp[0],self.sp[1],self.dp[0],self.dp[1], \
                                                                       "+".join(map(str,self.action)),self.redunt)


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
        and p1_dp_start >= p2_dp_start and p1_dp_end <= p2_dp_end:# and p1.action == p2.action:
        return 1
        #第一个范围小一些
    elif p2_sip_start >= p1_sip_start and p2_sip_end <= p1_sip_end and  p2_dip_start >= p1_dip_start and p2_dip_end <= p1_dip_end and p2_sp_start >= p1_sp_start and p2_sp_end <= p1_sp_end \
        and p2_dp_start >= p1_dp_start and p2_dp_end <= p1_dp_end: #and p1.action == p2.action:
        return 2
        #第二个范围小一些
    else:
        return 0


def findIntersectionPart(p1,p2):
    # count_inter = 0
    # count_
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


def ip1():
    t = []
    pt = []
    j=0
    while (j < 200):
        s = "0000000000000000000000001"
        for i in range(7):
            s += str(random.randint(0,1))
        pos = s[::-1].find("1")
        mask = 32-pos
        l=[]
        l.append(int(s[0:8],2))
        l.append(int(s[8:16],2))
        l.append(int(s[16:24],2))
        l.append(int(s[24:32],2))
        l.append(mask)
        if l in t:
            pass
        else:
            t.append(l)
            dip=[192,168,1,1,32]
            sp=[1,10]
            dp=[1,10]
            action = random.randint(10,30)
            p = Policy(l,dip,sp,dp,action,False)
            pt.append(p)
        j += 1
        # print l
    # print len(t)
    # print len(pt)
    return  pt


if __name__ == "__main__":
    # p1 = Policy([58,80,0,5,32],[68,80,0,5,32],[10,20],[10,20],1)
    # p2 = Policy([58,80,0,4,30],[68,80,0,4,30],[5,30],[5,30],2)
    # policy_list=[p1,p2]
    policy_list=[]
    with open(r"C:\Users\chen\Desktop\EntryMigration2017-5-12 172423\shiyanshuju\forwarding_rerange\r3_8rerange.txt","r+") as f1:
        for line in f1:
            l=[]
            line=line.strip('\n')
            l = line.split(",")
            sip,dip,sp,dp,action=[],[],[],[],[]
            for i in range(0,5):
                sip.append(int(l[i]))
            for i in range(5,10):
                dip.append(int(l[i]))
            for i in range(10,12):
                sp.append(int(l[i]))
            for i in range(12,14):
                dp.append(int(l[i]))
            for i in range(14,15):
                action.append(int(l[i]))
            redunt = (str(l[15])  == "True")
            # print type(redunt)
            p = Policy(sip,dip,sp,dp,action,redunt)
            policy_list.append(p)
    f1.close()
    print len(policy_list)
    # for i in range(len(policy_list)):
    #     print policy_list[i]


    # policy_list=ip1()
    # print"*****************"
    # print len(policy_list)
    policy_order_list= [[]*10000 for i in range(25)]

#初始化order0
    order = 0
    for i in range(len(policy_list)):
        policy_order_list[order].append(policy_list[i])

    print"*****************"
    print len(policy_order_list[0])
    flag_conflict = True
    count_1 = 0
    #[0,1,2] order<2
    count_inter,count_include1,count_include2 = 0,0,0
    while (flag_conflict==True and order<3):
        flag_conflict = False
        for i in range(len(policy_order_list[order])-1):
            if policy_order_list[order][i].redunt == True:
                continue
            for j in range(i+1,len(policy_order_list[order])):
                if policy_order_list[order][j].redunt == True or policy_order_list[order][i].redunt == True:
                    continue
                if conflict(policy_order_list[order][i],policy_order_list[order][j]):
                    flag_conflict = True
                    sip,dip,sp,dp,action=[],[],[],[],[]
                    if policy_order_list[order][i].sip[4] > policy_order_list[order][j].sip[4]:
                        sip = policy_order_list[order][i].sip
                    else:
                        sip = policy_order_list[order][j].sip

                    if policy_order_list[order][i].dip[4] > policy_order_list[order][j].dip[4]:
                        dip = policy_order_list[order][i].dip
                    else:
                        dip = policy_order_list[order][j].dip

                    if policy_order_list[order][i].sp[0] > policy_order_list[order][j].sp[0]:
                        sp.append(policy_order_list[order][i].sp[0])
                    else:
                        sp.append(policy_order_list[order][j].sp[0])

                    if policy_order_list[order][i].dp[0] > policy_order_list[order][j].dp[0]:
                        dp.append(policy_order_list[order][i].dp[0])
                    else:
                        dp.append(policy_order_list[order][j].dp[0])

                    if policy_order_list[order][i].sp[1] < policy_order_list[order][j].sp[1]:
                        sp.append(policy_order_list[order][i].sp[1])
                    else:
                        sp.append(policy_order_list[order][j].sp[1])

                    if policy_order_list[order][i].dp[1] < policy_order_list[order][j].dp[1]:
                        dp.append(policy_order_list[order][i].dp[1])
                    else:
                        dp.append(policy_order_list[order][j].dp[1])

                    action = list(set(policy_order_list[order][i].action+policy_order_list[order][j].action))
                    new_policy = Policy(sip,dip,sp,dp,action,False)
                    policy_order_list[order+1].append(new_policy)
                    #判断是否redunt
                    if new_policy.sip[4] == policy_order_list[order][i].sip[4] and new_policy.dip[4] == policy_order_list[order][i].dip[4] and \
                        new_policy.sp == policy_order_list[order][i].sp and new_policy.dp == policy_order_list[order][i].dp and \
                            new_policy.action == policy_order_list[order][i].action:
                        policy_order_list[order][i].redunt = True

                    if new_policy.sip[4] == policy_order_list[order][j].sip[4] and new_policy.dip[4] == policy_order_list[order][j].dip[4] and \
                        new_policy.sp == policy_order_list[order][j].sp and new_policy.dp == policy_order_list[order][j].dp and \
                            new_policy.action == policy_order_list[order][j].action:
                        policy_order_list[order][j].redunt = True
        order += 1
        print order
        print len(policy_order_list[order])
    print order
    total_num = 0
    print "----------------------"
    for i in range(order+1):
        order_total_num = 0
        for j in range(len(policy_order_list[i])):
            if policy_order_list[i][j].redunt == False:
                total_num += 1
                order_total_num += 1
        print i,order_total_num
    for i in range(len(policy_order_list[0])):
        if policy_order_list[0][i].redunt == False:
            print policy_order_list[0][i]
    print "total_num"
    print total_num
    print "----------------------"
    # print policy_order_list[2]



    print"*****************"
    print len(policy_order_list[0])
    print "*************total num"
    print total_num
    print "*************count_1"
    print count_1
    print "count_include1"
    print count_include1
    print "count_include2"
    print count_include2
    print "count_inter"
    print count_inter
    # print policy_order_list[0][0]
    # print policy_order_list[1][0]


'''
                    if order == 0:
                        count_1 += 1
                        # print i,j
                    # print "chongtu"
                    if isInclude(policy_order_list[order][i],policy_order_list[order][j]) == 1:
                        count_include1 += 1
                        # new_policy = Policy(policy_order_list[order][i].sip,policy_order_list[order][i].dip,\
                        #                     policy_order_list[order][i].sp,policy_order_list[order][i].dp,\
                        #                     policy_order_list[order][i].action,False)
                        # policy_order_list[order+1].append(new_policy)
                        # if policy_order_list[order][i].action == policy_order_list[order][j].action:
                        #     policy_order_list[order][i].redunt = True
                        #     new_policy = Policy(policy_order_list[order][i].sip,policy_order_list[order][i].dip,\
                        #                     policy_order_list[order][i].sp,policy_order_list[order][i].dp,\
                        #                     policy_order_list[order][i].action,False)
                        #     policy_order_list[order+1].append(new_policy)
                        # else:
                        policy_order_list[order][i].redunt = True
                        new_policy = Policy(policy_order_list[order][i].sip,policy_order_list[order][i].dip,\
                                        policy_order_list[order][i].sp,policy_order_list[order][i].dp,\
                                        policy_order_list[order][i].action,False)
                        policy_order_list[order+1].append(new_policy)
                    elif isInclude(policy_order_list[order][i],policy_order_list[order][j]) == 2:
                        count_include2 += 1
                        # new_policy = Policy(policy_order_list[order][j].sip,policy_order_list[order][j].dip,\
                        #                     policy_order_list[order][j].sp,policy_order_list[order][j].dp,\
                        #                     policy_order_list[order][j].action,False)
                        # policy_order_list[order+1].append(new_policy)
                        # if policy_order_list[order][i].action == policy_order_list[order][j].action:
                        #     policy_order_list[order][j].redunt = True
                        #     new_policy = Policy(policy_order_list[order][j].sip,policy_order_list[order][j].dip,\
                        #                     policy_order_list[order][j].sp,policy_order_list[order][j].dp,\
                        #                     policy_order_list[order][j].action,False)
                        #     policy_order_list[order+1].append(new_policy)
                        # else:
                        policy_order_list[order][j].redunt = True
                        new_policy = Policy(policy_order_list[order][j].sip,policy_order_list[order][j].dip,\
                                        policy_order_list[order][j].sp,policy_order_list[order][j].dp,\
                                        policy_order_list[order][j].action,False)
                        policy_order_list[order+1].append(new_policy)
                    else:
                        count_inter += 1
                        new_policy = findIntersectionPart(policy_order_list[order][i],policy_order_list[order][j])
                        policy_order_list[order+1].append(new_policy)
        order += 1
        print order
        print len(policy_order_list[order])
        '''