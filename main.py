from colorama import Fore as fore
import datetime
import json
import requests
import urllib.parse as parse

SHARED_HEADER = {"Host": "tjxsfw.chisai.tech",
                 "Connection": "keep-alive",
                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
                 "content-type": "application/x-www-form-urlencoded",
                 "Referer": "https://servicewechat.com/wx427cf6b5481c866a/67/page-frame.html",
                 "Accept-Encoding": "gzip, deflate, br"}


def getReportStatus(authorization: str, studentPid: int):
    header = {"Authorization": authorization}
    header.update(SHARED_HEADER)
    dataDict = {"studentPid": studentPid}
    data = parse.urlencode(dataDict)
    return requests.get("https://tjxsfw.chisai.tech/api/school_tjxsfw_student/yqfkLogDailyreport/hasDoneToday", headers=header, data=data).content


def Report(authorization: str, studentPid: int, studentName: str, studentStudentno: int, studentCollege: str = "土木工程学院", locLat: float = 31.25956, locLng: float = 121.52609, locNation: str = "中国", locProvince: str = "上海市", locCity: str = "上海市", locDistrict: str = "杨浦区", locRiskaddress: str = "不在范围内", locRisklevelGoverment: str = "低风险", studentStatusQuarantine: str = "正常（未隔离）", locStreet: str = "平凉路街道", locStreetno: str = "江浦路"):
    currentTimeStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dataDict = {"studentPid": str(studentPid), "studentName": studentName, "studentStudentno": str(studentStudentno),
                "studentCollege": studentCollege,
                "locLat": str(locLat), "locLng": str(locLng),
                "locNation": locNation, "locProvince": locProvince, "locCity": locCity,  "locDistrict": locDistrict,
                "healthy": 0,
                "source": "weixin,windows", "reportDatetime": currentTimeStr, "hasMoved": "false", "leaveReason": "",
                "locNation1": locNation, "locProvince1": locProvince,  "locCity1": locCity,
                "locRiskaddress": locRiskaddress, "locRisklevelGoverment": locRisklevelGoverment,
                "studentStatusQuarantine": studentStatusQuarantine,
                "locStreet": locStreet, "locStreetno": locStreetno}
    data = parse.urlencode(dataDict).replace("+", "%20")
    header = {"Content-Length": str(len(data)),
              "Authorization": authorization}
    header = header.update(SHARED_HEADER)
    return requests.post("https://tjxsfw.chisai.tech/api/school_tjxsfw_student/yqfkLogDailyreport/v3", data=data, headers=header).content


def main(auth: str, pid: int, name: str, no: int):

    reportStatusResponse = getReportStatus(auth, pid)
    print("Response: ", reportStatusResponse.decode())

    status = json.loads(reportStatusResponse)
    if "code" not in status or status["code"] != 200:
        print(fore.RED + "请求失败。" + fore.RESET)
        return -2
    elif status["message"] == "今日已打卡":
        print(fore.BLUE+"已打卡。" + fore.RESET)
        return 1

    reportResponse = Report(auth, pid, name, no)
    print("Response: ", reportResponse.decode())

    report = json.loads(reportResponse)
    if "code" not in status or report["code"] != 200:
        print(fore.RED + "请求失败。" + fore.RESET)
        return -2
    elif report["status"] == False:
        print(fore.RED + "打卡失败。" + fore.RESET)
        return -1
    print(fore.GREEN+"打卡成功。"+fore.RESET)
    return 0


if __name__ == "__main__":
    from sys import argv
    from getopt import getopt, GetoptError
    HELP = argv[0] + \
        " -a authorization -p studentPid -N studentName -n studentNo"

    auth: str
    pid: int
    name: str
    no: int
    try:
        opts, args = getopt(argv[1:], "ha:p:N:n:")
    except GetoptError:
        print(HELP)
        exit(-1)
    for opt, arg in opts:
        if opt in ["-h"]:
            print(HELP)
        elif opt in ["-a"]:
            auth = arg
        elif opt in ["-p"]:
            pid = int(arg)
        elif opt in ["-N"]:
            name = arg
        elif opt in ["-n"]:
            no = int(arg)
        else:
            print("Unrecognized option", opt, ".")
    if not auth or not pid or not name or not no:
        print(HELP)
    else:
        main(auth=auth, pid=pid, name=name, no=no)
