#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from helper.utils import Utils

class Settings:
    def get_settings(filename):
        obj = Utils.from_json_file(filename)
        return(obj)

    def get_moveout():
        return [
            {'name':'格雷斯·威廉姆斯', 'id':'wxid_mg2hf9hzbr1m22'},    # 加朋友
            {'name':'Micheal Chan', 'id':'Engr2212'},       # 加朋友
            {'name':'David', 'id':'wxid_3udfp8zkry6922'},   # 加朋友
            {'name':'stephen huang', 'id':'stephenof2'},    # 加朋友
            {'name':'天道酬勤', 'id':'fd20201124'}, # 海运
            {'name':'心静如茶', 'id':'fd20201155'}, # 海运
            # {'name':'小美', 'id':'Yt-mting'},
            {'name':'讓愛領先','id':'joseph6412ho'},
            {'name':'史蒂文','id':'wxid_ww8nnh6vn3sr12'},
            {'name':'Chun yeung'},  # 加朋友
            {'name':'yeung'},       # 加朋友
            {'name':'美国英语写作课大学申请辅导Susan'},
            {'name':'🎵🎤Dansy好声音YouTube频道', 'id':'dansywu'},
            {'name':'慕康医药Lily', 'id':'yinyinyin2n'},
            {'name':'达美医疗Selena'},
            {'name':'燕献凯 Yan Xiankai'},
            {'name':'相逢一笑', 'id':'XFYXSZ'},
        ]

    def get_blacklist():
        return [
            {'name':'Yoki'},        # AI聘-周末公开课
            {'name':'DAL小仙女'},    # AB Testing！AB测试
            {'name':'张亮'},         # 业办理...★毕业证＋成绩单...
            {'name':'Zhang'},       # 加朋友
            {'name':'good engineer'},
            {'name':'goodengineer27'},
            {'name':'engr20199806'},
            {'name':'Wang'},
            {'name':'奥尔特加'},
            {'name':'程。。'},
            {'name':'缘起缘落'},
            {'name':'Zhang Owen'},
            {'name':'杰弗裡·雲鵬'},
            {'name':'chike wu'},
            {'name':'Zheng'},
            {'name':'Gonzalez'},
            {'name':'Chan Raymond'},
            {'name':'能力強'},
            {'name':'張忠'},
            {'name':'宋仲基'},
            {'name':'Zhang Cruise'},
            {'name':'Frank Chan'},
            {'name':'Lynn 陳'},
            {'name':'太棒了'},
            {'name':'Alin'},
            # {'name':'', 'id':''},
        ]
