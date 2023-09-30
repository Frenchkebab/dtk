from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait as wait
import datetime

# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.by import By
# import time
# import openpyxl

# import pyautogui
# import clipboard

from inputFunctions import *
from common import *
from timer import *


# 사용자 정의
import inputFunctions
import dtk
import common
# import timer

########################## main.py #########################################

# setting.txt 읽기
id, password, work_type, file_name, start_idx, last_idx, minSecond, maxSecond = inputFunctions.userInput()

# 로그 작성 파일
now = datetime.datetime.now()
nowDateTime = str(now.strftime('%Y%m%d_%H-%M-%S'))
logFile = open(f"./UserFiles/result/{nowDateTime}.txt", "w", encoding="utf-8")

# 파일이름, 시작NO., 마지막NO. 입력
inputFunctions.printUserInput(id, password, work_type, file_name, start_idx, last_idx, minSecond, maxSecond)

# 속성값 덮어쓰기
inputFunctions.attributeWrite(file_name)

# 읽은 데이터프레임 받아옴
df = inputFunctions.readXslx(file_name)
dataArr = []
for i in range(start_idx, last_idx + 1):
    df.loc[i].to_dict()
    

# 사전 리스트를 저장
dataArr = inputFunctions.dfToDictArr(df, start_idx, last_idx)


# 크롬 창 켜기
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# claimx.com 으로 이동
common.toClaimX(driver)


# 로그인
input("Login and press enter: ")
# common.login(driver, id, password)

# Archive 업로드 중 문제가 생기는 경우 True
archiveError = False

# 작업 종류 선택
if work_type == "dtk":
    for row in dataArr:
        try:
            logFile.write(f"========================{row['No.']}번째 줄========================\n")
            print(f"========================{row['No.']}번째 줄========================")
            logFile.write(f"{row}\n\n")
            print(f"{row}\n")

            # 업로드 에러 flag 초기화
            archiveError = False

            #* claim 버튼 클릭
            common.clickClaim(driver)

            #! CID가 없는 경우 (입력되지 않은 자료)
            if common.checkCID(row) == False:

                result = dtk.VehicleLogistics(driver, file_name, row)
                if result:
                    # 정상적으로 완료되면 CID를 저장
                    common.getCid(file_name, driver, row)
                    common.memo(file_name, row, "Vehicle-Logistics done")
                    print(row)   
                    logFile.write("Vehicle-Logistics 완료\n")
                    print("Vehicle-Logistics 완료")
                else:
                    continue

                # Archive
                archiveError = dtk.archive(driver, logFile, row)
                common.memo(file_name, row, "Archive done", archiveError)
                logFile.write("Archive 완료\n")
                print("Archive 완료")

                # Claim
                dtk.claim(driver)
                memo(file_name, row, "Claim done")
                logFile.write("Claim 완료\n")
                print("Claim 완료")

                # Receipts
                dtk.receipts(driver, row)
                common.memo(file_name, row, "Receipts done")
                logFile.write("Receipts 완료\n")
                print("Receipts 완료")

                # Status
                dtk.status(driver)
                common.memo(file_name, row, "finished")
                logFile.write(f"{row['No.']}번 라인 입력 완료\n")
                print(f"{row['No.']}번 라인 입력 완료")
                sleep_timer_second(minSecond, maxSecond)

            #! CID칸이 있는 경우 (입력된 자료)
            else:
                print('here')
                if str(row["Memo"]) == "Vehicle-Logistics done":
                    logFile.write("Archive부터 입력 시작\n")
                    print("Archive부터 입력 시작")
                    dtk.query(driver, row)

                    dtk.archive(driver,logFile, row)
                    common.memo(file_name, row, "Archive done")
                    logFile.write("Archive 완료\n")
                    print("Archive 완료")

                    dtk.claim(driver)
                    common.memo(file_name, row, "Claim done")
                    logFile.write("Claim 완료\n")
                    print("Claim 완료")

                    dtk.receipts(driver, row)
                    common.memo(file_name, row, "Receipts done")
                    logFile.write("Receipts 완료\n")
                    print("Receipts 완료")

                    dtk.status(driver)
                    memo(file_name, row, "finished")
                    logFile.write(f"{row['No.']}번 라인 입력 완료\n")
                    print(f"{row['No.']}번 라인 입력 완료")

                    logFile.write("============================================================\n\n")
                    print("============================================================\n")


                elif str(row["Memo"]) == "Archive done":
                    logFile.write("Claim 입력부터 시작\n")
                    print("Claim 입력부터 시작")
                    dtk.query(driver, row)

                    dtk.claim(driver)
                    common.memo(file_name, row, "Claim done")
                    logFile.write("Claim 완료\n")
                    print("Claim 완료")

                    dtk.receipts(driver, row)
                    common.memo(file_name, row, "Receipts done")
                    logFile.write("Receipts 완료\n")
                    print("Receipts 완료")

                    status(driver)
                    memo(file_name, row, "finished")
                    logFile.write(f"{row['No.']}번 라인 입력 완료\n")
                    print(f"{row['No.']}번 라인 입력 완료")

                elif str(row["Memo"]) == "Claim done":
                    "Receipts 입력부터 시작"
                    query(driver, row)

                    receipts(driver, row)
                    memo(file_name, row, "Receipts done")
                    logFile.write("Receipts 완료\n")
                    print("Receipts 완료")

                    status(driver)
                    memo(file_name, row, "finished")
                    logFile.write(f"{row['No.']}번 라인 입력 완료\n")
                    print(f"{row['No.']}번 라인 입력 완료")

                elif str(row["Memo"]) == "Receipts done":
                    logFile.write("status 입력부터 시작\n")
                    print("status 입력부터 시작")
                    query(driver, row)

                    status(driver)
                    memo(file_name, row, "finished")
                    logFile.write(f"{row['No.']}번 라인 입력 완료\n")
                    print(f"{row['No.']}번 라인 입력 완료")

                elif str(row["Memo"]) == "finished":
                    logFile.write("이미 완료된 작업\n")
                    print("이미 완료된 작업")
                    logFile.write("============================================================\n\n")
                    print("============================================================\n")
                    continue

                else:
                    logFile.write("memo 예외\n")
                    print("memo 예외")
                    logFile.write("============================================================\n\n")
                    print("============================================================\n")
                    continue
            
                sleep_timer_second(minSecond, maxSecond)
            logFile.write("============================================================\n\n")
            print("============================================================\n")
        
        except Exception as e:
            logFile.write(f"{row['No.']} 번째 줄 eror:\n")
            print(f"{row['No.']} 번째 줄 eror:")
            logFile.write(f"{e}\n")
            print(f"{e}")
            logFile.write("============================================================\n\n")
            print("============================================================\n")
            continue

print("프로그램 종료")
logFile.write("프로그램 종료")
logFile.close()