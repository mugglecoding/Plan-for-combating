from bs4 import BeautifulSoup
import requests
import time

link_host = '''


    http://bj.ganji.com/zibubaojian/z2/
    http://bj.ganji.com/anmobaojian/z1/
    http://bj.ganji.com/bawanwujian/
    http://bj.ganji.com/xuniwupin/
    http://bj.ganji.com/qitawupin/
    http://bj.ganji.com/ershoufree/
    http://bj.ganji.com/wupinjiaohuan/
    http://bj.ganji.com/zhuanqu_anjia/all/
    http://bj.ganji.com/zhuanqu_jiaren/all/
    http://bj.ganji.com/zhuanqu_shenghuo/all/


'''
#最大43
# for x in link_host.split():
#     print(x)
#     print(len(x))
'''
 http://bj.ganji.com/jiaju/
    http://bj.ganji.com/rirongbaihuo/
    http://bj.ganji.com/chuangdian/
    http://bj.ganji.com/guizi/
    http://bj.ganji.com/zhuoyi/
    http://bj.ganji.com/shafachaji/
    http://bj.ganji.com/zixingchemaimai/
    http://bj.ganji.com/diandongche/
    http://bj.ganji.com/motuoche/
    http://bj.ganji.com/shouji/
    http://bj.ganji.com/iphone/
    http://bj.ganji.com/nokia/
    http://bj.ganji.com/htc/
    http://bj.ganji.com/sanxingshouji/
    http://bj.ganji.com/motorola/
    http://bj.ganji.com/tongxuntaocan/
    http://bj.ganji.com/bangong/
    http://bj.ganji.com/nongyongpin/
    http://bj.ganji.com/bangongjiaju/
    http://bj.ganji.com/jiguangyitiji/
    http://bj.ganji.com/dayinji/z1/
    http://bj.ganji.com/shipinjiagongshebei/
    http://bj.ganji.com/shengchanjiamengshebei/
    http://bj.ganji.com/jichuang/
    http://bj.ganji.com/tuolaji/
    http://bj.ganji.com/jiadian/
    http://bj.ganji.com/dianshi/
    http://bj.ganji.com/bingxiang/
    http://bj.ganji.com/kongtiao/
    http://bj.ganji.com/reshuiqi/
    http://bj.ganji.com/xiyiji/
    http://bj.ganji.com/diancilu/
    http://bj.ganji.com/weibolu/
    http://bj.ganji.com/yueqiyinxiang/
    http://bj.ganji.com/ershoubijibendiannao/
    http://bj.ganji.com/pingbandiannao/z1/
    http://bj.ganji.com/ruanjiantushu/
    http://bj.ganji.com/yueqi/
    http://bj.ganji.com/yinxiang/
    http://bj.ganji.com/yundongqicai/
    http://bj.ganji.com/yingyouyunfu/
    http://bj.ganji.com/tongche/
    http://bj.ganji.com/tongzhuang/
    http://bj.ganji.com/hufupin/
    http://bj.ganji.com/shuma/
    http://bj.ganji.com/shumaxiangji/
    http://bj.ganji.com/shumashexiangji/
    http://bj.ganji.com/youxiji/
    http://bj.ganji.com/suishenting/
    http://bj.ganji.com/yidongcunchu/
    http://bj.ganji.com/laonianyongpin/
'''