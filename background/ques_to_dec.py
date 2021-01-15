import jieba.posseg as posseg
import pandas as pd
import jieba
import re
from Saier.sim_new import get_sim_top10
import csv
from Saier.test import sematic_test
from myweb.commonlog import CommonLog
nega_patterns = [None] * 7
posi_patterns = [None] * 4
share_pat = r'([\u4E00-\u9FA5\u3002\uff1b\uff0c\uff1a\u201c\u201d\u3001\u300a\u300b]+)?'

nega_patterns[0] = share_pat + '(不属于|不符合|不是|没有)' + share_pat + '(的是)?'
nega_patterns[1] = share_pat + '(不包括)' + share_pat + '(的是)?'
nega_patterns[2] = share_pat + '(不能)' + share_pat + '(的是)?'
nega_patterns[3] = share_pat + '(哪种|哪一种|哪项|哪一项|哪个|哪一个)' + share_pat + '(不需要|不必)' + \
                   share_pat + '(的是)?'
nega_patterns[4] = r'^除([\u4E00-\u9FA5]+|（）)?' + '外' + share_pat + '(都|均)' + '(需要|需)' + share_pat + '(的是)?'
nega_patterns[5] = share_pat + '(不正确|错误)' + share_pat + '(的是)?'
nega_patterns[6] = share_pat + '(不会)' + share_pat + '(哪里|（）)?'

posi_patterns[0] = share_pat + '(哪种|哪一种|哪项|哪一项|哪个|哪一个)' + share_pat
posi_patterns[1] = share_pat + '(正确)' + share_pat + '(的是)?'
posi_patterns[2] = share_pat + '(是)' + '(（）)?'
posi_patterns[3] = share_pat + '(什么|（）)' + share_pat + '(的是)?'

ans = ""


def nega_match(text, corr_ans, id):
    print("nega")
    pat = -1
    ret = 0
    for i in range(len(nega_patterns)):
        res = re.match(nega_patterns[i], text)
        if res != None:
            print(nega_patterns[i])
            pat = i
            break
    if pat == -1:
        ret = -1
        return -1

    f = open("Saier/temp/" + str(id) + ".csv", 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["sentence1", "sentence2", "label"])
    if pat == 0:
        ans = corr_ans + '是' + res.group(3).strip('的是')
    elif pat == 1:
        ans = corr_ans + '的' + res.group(1).strip('的是')
    elif pat == 2:
        ans = corr_ans + '能' + res.group(3).strip('的是')
    elif pat == 3:
        ans = res.group(1) + corr_ans + res.group(3) + '需要' + res.group(4)
    elif pat == 4:
        ans = corr_ans + res.group(4) + res.group(5)
    elif pat == 5:
        ans = corr_ans
    elif pat == 6:
        ans = res.group(1) + '会' + res.group(3) + corr_ans
    print("here")
    top10 = get_sim_top10(ans)
    for t in top10:
        csv_writer.writerow([ans, t, "0"])
    f.close()
    res_list = sematic_test("Saier/temp/" + str(id) + ".csv", "Saier/models/best.pth.tar")
    print(res_list)
    if 1 not in res_list:
        print("本题正确")
        ret = 1
    else:
        print("本题错误")
        ret = 0
    return ret

def posi_match(text, corr_ans, id):
    print("1")
    pat = -1
    for i in range(len(posi_patterns)):
        res = re.match(posi_patterns[i], text)
        if res != None:
            print(posi_patterns[i])
            pat = i
            break
    if pat == -1:
        ret = -1
        return -1
    print('aaa')
    CommonLog.error("testtest")
    f = open("Saier/temp/" + str(id) + ".csv", 'w', encoding='utf-8')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["sentence1", "sentence2", "label"])
    print(res.groups())
    if pat == 0:
        ans = res.group(1) + corr_ans + '的' + res.group(3).strip('的是')
    elif pat == 1:
        ans = corr_ans
    elif pat == 2:
        ans = res.group(1) + '是' + corr_ans
    elif pat == 3:
        ans = res.group(1) + corr_ans + '的' + res.group(3)

    top10 = get_sim_top10(ans)
    print(top10)
    for t in top10:
        csv_writer.writerow([ans, t, "0"])
    f.close()
    res_list = sematic_test("Saier/temp/" + str(id) + ".csv", "Saier/models/best.pth.tar")
    print(res_list)
    if 1 in res_list:
        print("本题正确")
        ret = 1
    else:
        print("本题错误")
        ret = 0
    return ret


def get_judgement(ques):
    text = ques['ques_body']
    id = ques['id']
    if ques['corr_ans'] == "1":
        corr_ans = ques['item_a']
    elif ques['corr_ans'] == "2":
        corr_ans = ques['item_b']
    elif ques['corr_ans'] == "3":
        corr_ans = ques['item_c']
    elif ques['corr_ans'] == "4":
        corr_ans = ques['item_d']
    ret = nega_match(text, corr_ans, id)
    if ret != -1:
        if ret == 1:
            return '认证通过'
        elif ret == 0:
            return '认证未通过'
    else:
        re = posi_match(text, corr_ans, id)
        if re != -1:
            if re == 1:
                return '认证通过'
            elif re == 0:
                return '认证未通过'
    if ret == -1 and re == -1:
        return '待人工认证'
