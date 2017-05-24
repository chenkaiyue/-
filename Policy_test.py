
#coding:utf-8
class Policy:
    def __init__(self,sip,dip,sp,dp,action,redunt):
        self.sip = sip   #sip[5]  ip地址
        self.dip = dip
        self.sp = sp   #sp[2]  端口
        self.dp = dp
        self.action = action  #int     -1代表转发
        self.redunt = redunt
    def __str__(self):
        return  ("[%d,%d,%d,%d,%d],[%d,%d,%d,%d,%d]") % (self.sip[0],self.sip[1],self.sip[2],self.sip[3],self.sip[4])
        # return  self.sip
p = Policy([1,1,1,1,1],[1,1,1,1,1],[10,20],[20,30],1,False)

print p