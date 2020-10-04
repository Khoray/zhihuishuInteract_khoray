import requests
import json
import time
import datetime
import re
import os
import random
#powered by khoray
#得到问题id
cookie= ""
questioncnt = 0
answercnt = 0
sleep = 0
with open('cookie.txt') as f:
    text = f.read()
    text_json = json.loads(text)
    cookie = text_json['cookie']
    questioncnt = int(text_json['question_number'])
    answercnt = int(text_json['answer_number'])
    sleep = int(text_json['sleep'])

question_names = []
def get_if_answered(qid):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "13",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie,
        "Host": "creditqa-web.zhihuishu.com",
        "Origin": "https://creditqa-web.zhihuishu.com",
        "Referer": "https://creditqa-web.zhihuishu.com/shareCourse/questionDetailPage?sourceType=2&qid=392420098",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        'qid':qid
    }
    url = "https://creditqa-web.zhihuishu.com/answer/myAnswerByQuestionId"
    r = requests.post(url,data=data,headers=headers).text
    rjson = json.loads(r)
    result = rjson['result']
    if(result==[]):
        return False
    else:
        return True

def get_course():
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    now_propertime = datetime.datetime.now().strftime('%H:%M:%S')
    uuid = re.findall(r'exitRecod_(.*?)=2',cookie)
    #url = f'https://onlineservice.zhihuishu.com/student/message/message/getImportantNoticeList?uuid={uuid[0]}&date={now_time}T{now_propertime}.657Z'
    url = "https://onlineservice.zhihuishu.com/student/course/share/queryShareCourseInfo"
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "76",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,
        "Host": "onlineservice.zhihuishu.com",
        "Origin": "https://onlineh5.zhihuishu.com",
        "Referer": "https://onlineh5.zhihuishu.com/onlineWeb.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63"
    }
    data = {
        "status": "0",
        "pageNo": "1",
        "pageSize": "5",
        "uuid": uuid[0],
        "date": f"{now_time}T{now_propertime}Z"
    }
    
    r = requests.post(url,headers=headers,data=data).text
    rjson = json.loads(r)
    courses = {'courseId':[],'recruitId':[]}
    for i in range(len(rjson['result']['courseOpenDtos'])):
        courses['courseId'].append(rjson['result']['courseOpenDtos'][i]['courseId'])
        courses['recruitId'].append(rjson['result']['courseOpenDtos'][i]['recruitId'])
    print(courses)
    return courses

def get_questions(recruitId,courseId,pageIndex):
    question_names = []
    data_getdata = {
        "recruitId":recruitId,
        "courseId":courseId,
        "pageSize":10,
        "pageIndex":pageIndex
    }
    headers_getdata = {
        "Host": "creditqa-web.zhihuishu.com",
        "Connection": "keep-alive",
        "Content-Length": "56",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://creditqa-web.zhihuishu.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=2110478&recruitId=42488",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie
    }
    url = "https://creditqa-web.zhihuishu.com/shareCourse/getHotQuestionList"
    r = requests.post(url,data=data_getdata,headers=headers_getdata)
    rjson = json.loads(r.text)
    question_list = {'id':[],'content':[]}
    for i in range(0,len(rjson['result']['questionInfoList'])):
        question_list['id'].append(rjson['result']['questionInfoList'][i]['questionId'])
        question_list['content'].append(rjson['result']['questionInfoList'][i]['content'])
    return question_list
#抄作业
def get_answer(questionId,recruitId,courseId):
    url = "https://creditqa-web.zhihuishu.com/answer/getAnswerInInfoOrderByTime"
    data = {
        "pageSize": "20",
        "pageIndex": "0",
        "questionId": questionId,
        "sourceType": "2",
        "recruitId": recruitId,
        "courseId": courseId
    }
    headers = {
        "Host": "creditqa-web.zhihuishu.com",
        "Connection": "keep-alive",
        "Content-Length": "90",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://creditqa-web.zhihuishu.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://creditqa-web.zhihuishu.com/shareCourse/questionDetailPage?sourceType=2&qid=392420098",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookie
    }
    r = requests.post(url,data=data,headers=headers)
    answers_list = json.loads(r.text)['result']['answerInfos']
    ans_contents = []
    for i in range(0,len(answers_list)):
        ans_contents.append(answers_list[i]['answerContent'])
    return ans_contents
#交答案
def postAnswer(answer,questionId):
    url = "https://creditqa-web.zhihuishu.com/answer/saveAnswer"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "64",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": cookie,
        "Host": "creditqa-web.zhihuishu.com",
        "Origin": "https://creditqa-web.zhihuishu.com",
        "Referer": "https://creditqa-web.zhihuishu.com/shareCourse/questionDetailPage?sourceType=2&qid=393076538",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
        "X-Requested-With": "XMLHttpRequest"
    }
    data = {
        "qid": questionId,
        "aContent": answer,
        "source": "2",
        "annexs": "[]"
    }
    r = requests.post(url,data=data,headers=headers)
    return r

def post_question(courseId,recruitId,content):
    data = {
        "annexs": "[]",
        "content": content,
        "courseId": courseId,
        "recruitId": recruitId,
        "sourceType": "2"
    }
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Length": "110",
        "Content-Type": "application/json",
        "Cookie": cookie,
        "Host": "creditqa-web.zhihuishu.com",
        "Origin": "https://creditqa-web.zhihuishu.com",
        "Referer": "https://creditqa-web.zhihuishu.com/shareCourse/qaAnswerIndexPage?sourceType=2&courseId=2096523&recruitId=32601",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = "https://creditqa-web.zhihuishu.com/shareCourse/saveQuestion"
    ddata = json.dumps(data)
    r = requests.post(url,data=ddata,headers=headers).text
    return r


course_list = get_course()

for j in range(0,len(course_list['courseId'])):
    print("当前课程：",course_list['courseId'][j])
    rid = course_list['recruitId'][j]
    cid = course_list['courseId'][j]
    print("现在开始提问：")
    for i in range(0,questioncnt):
        randa=int(random.random()*10)*10
        question_contents = get_questions(rid,cid,randa)['content']
        randb=int(random.random()*10)
        qcontent = question_contents[min(randb,len(question_contents))]
        print("当前问题：",qcontent)
        rtmp = post_question(cid,rid,qcontent)
        print("当前问题提问成功！")
        time.sleep(sleep)
    
    print("现在开始回答：")
    index = 0
    cnt = 0
    while(cnt <= answercnt):
        questions = get_questions(rid,cid,index)['id']
        for i in range(0,len(questions)):
            if(cnt >= answercnt):
                break
            if(get_if_answered(questions[i])==False):
                cnt += 1
                print("当前正在回答:",questions[i],"  now:",cnt)
                answer1 = get_answer(questions[i],rid,cid)
                a = postAnswer(answer1[0],questions[i])
                time.sleep(sleep)
        if(cnt >= answercnt):
            break
        index += 10
    

print("今日互动任务已经完成！")
os.system("shutdown -s -t 0")
