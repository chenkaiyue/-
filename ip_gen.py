#coding:utf-8
import random
# i,count0,count1 = 0,0,0
#
# while i<10000:
#     co = random.randint(0,1)
#     if co == 0:
#         count0 += 1
#     else:
#         count1 += 1
#     i += 1
# print count0,count1
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

# 不包含1.192.0.0的(1.128-1.255)的表项

# 1.128-1.192
def num_2_1():
    t = []
    j=0
    while (j < 50):
        s = "0000000110"
        for i in range(22):
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
        # print s
        # print mask
        # print l
        j += 1
        # print l
    print t
    print len(t)

def num_2_2():
    t = []
    j=0
    while (j < 50):
        s = "0000000111"
        for i in range(22):
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
        # print s
        # print mask
        # print l
        j += 1
        # print l
    print t
    print len(t)

#包含1.192的1.128-1.255的表项
def num_1():
    t=[]
    t.append([1,128,0,0,9])
    for i in range(1,23):
        l=[1,192,0,0]
        l.append(i+9)
        t.append(l)
    print t

# 1.0-1.64
def num_3_1():
    t = []
    j=0
    while (j < 50):
        s = "0000000100"
        for i in range(22):
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
        # print s
        # print mask
        # print l
        j += 1
        # print l
    print t
    print len(t)

def num_3_2():
    t = []
    j=0
    while (j < 50):
        s = "0000000101"
        for i in range(22):
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
        # print s
        # print mask
        # print l
        j += 1
        # print l
    print t
    print len(t)

def num_4():
    t=[]
    t.append([1,0,0,0,9])
    for i in range(1,23):
        l=[1,64,0,0]
        l.append(i+9)
        t.append(l)
    print t

def num_5():
    t=[]
    # t.append([1,128,0,0,9])
    for i in range(1,23):
        l=[1,64,0,0]
        l.append(i+9)
        t.append(l)
    print t

# l1,l2=[],[]
# p1,p2=[1,2,3],[3,4,5]
# l1.append(p1)
# l1.append(p2)
# l2.append(p1)
# l2.append(p2)


def ip1():
    #产生128-255段的表项
    t = []
    pt = []
    j=0
    # m = map()
    while (j < 55):
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
        action = random.randint(15,20)
        if (l,action) in t:
            pass
        else:
            t.append((l,action))
            dip=[192,168,1,1,32]
            sp=[1,10]
            dp=[1,10]
            p = Policy(l,dip,sp,dp,action,False)
            pt.append(p)
        j += 1
        # print l
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r1_5.txt",'w+')
    for i in range(len(pt)):
        s=""
        s = s + str(pt[i])+"\n"
        f.write(s)
    f.close()
    # print len(t)
    # print len(pt)
    # return  pt

def ip2():
    #产生0-128段的表项
    t = []
    pt = []
    j=0
    # m = map()
    while (j < 55):
        s = "0000000000000000000000000"
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
        action = random.randint(15,20)
        if (l,action) in t:
            pass
        else:
            t.append((l,action))
            dip=[192,168,1,1,32]
            sp=[1,10]
            dp=[1,10]
            p = Policy(l,dip,sp,dp,action,False)
            pt.append(p)
        j += 1
        # print l
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\r2_10.txt",'w+')
    for i in range(len(pt)):
        s=""
        s = s + str(pt[i])+"\n"
        f.write(s)
    f.close()

# 在route2中产生三个用于合并迁移过来的流表项的128-255范围的表项
def ip3():
    dip=[192,168,1,1,32]
    sp=[1,10]
    dp=[1,10]
    pt = []
    for i in range(15,18):
        pt.append(Policy([0,0,0,128,7],dip,sp,dp,i,False))
    # p1 = Policy([0,0,0,128,7],dip,sp,dp,15,False)
    f=open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test_w.txt",'w+')
    for i in range(len(pt)):
        s=""
        s = s + str(pt[i])+"\n"
        f.write(s)
    f.close()
    with open(r"C:\Users\chenkaiyue\Desktop\EntryMigration2017-5-12 172423\test_w.txt","r+") as f1:
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

            print sip,dip,sp,dp,action,redunt
    f1.close()



if __name__ == "__main__":
    # num_2_1()
    # num_2_2()
    # num_4()
    # num_5()
    # num_3_1()
    # num_3_2()
    # del l1[0][0]
    # print l2
    ip2()
    # print"pt-------------------"
    # print len(pt)
    # print pt


    # count1,count2 = 0,0
    # fp = Policy([0,0,0,128,25],[192,168,1,1,32],[1,10],[1,10],1)
    # for i in range(len(pt)-1):
    #     for j in range(i+1,len(pt)):
    #         if conflict(pt[i],pt[j]):
    #             count1 += 1
    #             print "^^^^",i,j
    # print "*****************",count1


    # for i in range(len(pt)):
    #     if conflict(pt[i],fp):
    #         count2 += 1
    #             # print "^^^^",i,j
    # print "*****************with forwarding",count2



    # fp1 = Policy([1,128,0,0,11],[192,168,1,1,32],[1,10],[1,10],1)
    # fp2 = Policy([1,192,0,0,32],[192,168,1,1,32],[1,10],[1,10],1)
    # print conflict(fp1,fp2)
    print "&&&&&"
    # ip3()