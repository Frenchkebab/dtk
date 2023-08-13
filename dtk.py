from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import datetime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
# import openpyxl

# import pyautogui
# import clipboard

from timer import waitLoading
from inputFunctions import *
from common import *

def VehicleLogistics(driver, file_name, row):
    # vehicle-logistics로 이동
    driver.implicitly_wait(5)
    driver.find_element(by=By.LINK_TEXT, value="vehicle-logistics").click()
    
    # 페이지 로딩 됐는지 검사
    while True:
        try: 
            driver.find_element(by=By.ID, value="meldfn")
            # 있으면 탈출
            break
        except:
            # 없으면
            time.sleep(5)
            

    # client 선택
    select = Select(driver.find_element(by=By.ID, value="meldfn"))      # (T) Daimler Trucks Korea Ltd.
    select.select_by_value("GCI4")
    time.sleep(0.5)

    # product/type of order 선택
    select = Select(driver.find_element(by=By.ID, value="auftrart"))        # day delivery
    select.select_by_value("TAG")
    time.sleep(0.5)

    select = Select(driver.find_element(by=By.NAME, value="field_produktart"))     # transport
    select.select_by_value("TRANS")
    time.sleep(1)
    
    # VIN No. 입력
    isV = False

    first = driver.find_element(by=By.ID, value="sndfzgidwmi")
    first.click()
    time.sleep(0.5)
    first.send_keys(row["VIN No."][0:3])

    ## if iSV, then choose different 'policy/type of insurance'
    # 30109636-06305 Master (Main Run) Primary -> S23ZHMB00001 Core Local Coverage Primary
    # Delivery passenger cars -> Delivery vans
    if(row["VIN No."][2] == 'V'):
        isV = True
    time.sleep(0.5)

    second = driver.find_element(by=By.NAME, value="field_sndfzgidvds")
    second.click()
    time.sleep(0.5)
    second.send_keys(row["VIN No."][3:9])
    time.sleep(0.5)

    third = driver.find_element(by=By.NAME, value="field_sndfzgidjahr")
    third.click()
    time.sleep(0.5)
    third.send_keys(row["VIN No."][9:10])
    time.sleep(0.5)

    fourth = driver.find_element(by=By.NAME, value="field_sndfzgidwerk")
    fourth.click()
    time.sleep(0.5)
    fourth.send_keys(row["VIN No."][10:11])
    time.sleep(0.5)

    fifth = driver.find_element(by=By.NAME, value="field_sndfzgidlfd")
    fifth.click()
    time.sleep(0.5)
    fifth.send_keys(row["VIN No."][11:])
    time.sleep(0.5)

    # reference: Commission No.
    commNo = row["Commission No."] 
    if commNo[0] != "0" or len(commNo) != 10:
        commNo = "0" + commNo # Commission No.가 0으로 시작하지 않거나 길이가 10보다 짧으면 0을 붙임

    reference = driver.find_element(by=By.NAME, value="field_auftrref")
    reference.send_keys(row["Commission No."])
    time.sleep(3)

    # further damage 검사
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="mainpart"]/form/table[2]/tbody/tr[7]/td/div/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td')
        memo(file_name, row, "further damage error")
        return False
    except:
        pass

    # carrier
    # if doesBLContainMolu("BL", row):
    #     carrier = driver.find_element(by=By.NAME, value="field_tuse")
    #     carrier.send_keys("mitsui")
    #     carrier.send_keys(Keys.ENTER)
    #     driver.switch_to.window(driver.window_handles[1])
    #     waitLoading()
    #     driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr/td[1]/input").send_keys(Keys.ENTER) # '+' 버튼 클릭
    #     driver.switch_to.window(driver.window_handles[0])

    # elif isHyundaiGlovis("BL", row):
    #     carrier = driver.find_element(by=By.NAME, value="field_tuse")
    #     carrier.send_keys("HYUNDAI GLOVIS")
    #     carrier.send_keys(Keys.ENTER)
    #     driver.switch_to.window(driver.window_handles[1])
    #     waitLoading()
    #     driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr/td[1]/input").send_keys(Keys.ENTER) # '+' 버튼 클릭
    #     driver.switch_to.window(driver.window_handles[0])

    # else:
    #     carrier = driver.find_element(by=By.NAME, value="field_tuse")
    #     carrier.send_keys("eukor")
    #     carrier.send_keys(Keys.ENTER)
    #     driver.switch_to.window(driver.window_handles[1])
    #     waitLoading()
    #     driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr[2]/td[1]/input").send_keys(Keys.ENTER) # 두 번째 '+' 버튼 클릭
    #     driver.switch_to.window(driver.window_handles[0])
    
    carrier = driver.find_element(by=By.NAME, value="field_tuse")
    carrier.send_keys("eukor")
    carrier.send_keys(Keys.ENTER)
    driver.switch_to.window(driver.window_handles[1])
    waitLoading()
    driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr[2]/td[1]/input").send_keys(Keys.ENTER) # 두 번째 '+' 버튼 클릭
    driver.switch_to.window(driver.window_handles[0])

    # reclamation made on
    rYear = row["Reclamation date"][0:4]
    rMonth = row["Reclamation date"][5:7]
    rDay = row["Reclamation date"][-2:]
    driver.find_element(by=By.NAME, value="subfield_reklzeit_day").send_keys(rDay)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_reklzeit_month").send_keys(rMonth)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_reklzeit_year").send_keys(rYear)

    # incident date
    iYear = row["Incident date"][0:4]
    iMonth = row["Incident date"][5:7]
    iDay = row["Incident date"][-2:]
    driver.find_element(by=By.NAME, value="subfield_schzeit_day").send_keys(iDay)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_schzeit_month").send_keys(iMonth)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_schzeit_year").send_keys(iYear)

    # claim type

    for i in range(1, 11):
        # damage code 마지막 6인지 검사
        if i < 10:
            dCode = str(row[f"Damage Code0{i}"])
        else:
            dCode = str(row[f"Damage Code{i}"])
        
        # 없으면 반복 중지
        if dCode == "nan":
            break

        # 마지막 자리가 6인 경우
        if dCode.strip()[-1] == "6":
            # claim type (normal)
            Select(driver.find_element(by=By.NAME, value="field_sart")).select_by_value("180")
            time.sleep(0.5)
            
            # route section/cause (normmal)
            Select(driver.find_element(by=By.NAME, value="field_sber")).select_by_value("131") # matariel damage
            time.sleep(0.5)
            Select(driver.find_element(by=By.NAME, value="field_surs")).select_by_value("037") # partial theft
            time.sleep(0.5)
            

        # 마지막 자리 6 아닌 경우 (normal case)
        else:
            # claim type (normal)
            Select(driver.find_element(by=By.NAME, value="field_sart")).select_by_value("D01")
            time.sleep(0.5)
            
            # route section/cause (normmal)
            Select(driver.find_element(by=By.NAME, value="field_sber")).select_by_value("131")
            time.sleep(0.5)
            Select(driver.find_element(by=By.NAME, value="field_surs")).select_by_value("C00")
            time.sleep(0.5)


    # claimant's reference
    driver.find_element(by=By.NAME, value="field_ansprref").send_keys(row["Repair No."])
    time.sleep(0.5)

    # policy/type of insurance
    if(isV):
        Select(driver.find_element(by=By.NAME, value="field_police")).select_by_value(f"S23ZHMB00001-{iYear}")
        Select(driver.find_element(by=By.NAME, value="field_kzvers")).select_by_value("CL09")
    else:
        if(iYear == '2022'):
            Select(driver.find_element(by=By.NAME, value="field_police")).select_by_value(f"S-22ZH-DA00001-2022")
        # iYear == 2023
        else:
            Select(driver.find_element(by=By.NAME, value="field_police")).select_by_value(f"S23ZHDA00001-2023")
        
        Select(driver.find_element(by=By.NAME, value="field_kzvers")).select_by_value("CL10")

    # estimated/amount claimed
    total = row["Sub Total"]
    driver.find_element(by=By.NAME, value="field_fordmsw").send_keys(total)
    Select(driver.find_element(by=By.NAME, value="field_qmsts")).select_by_value("034")
    time.sleep(0.5)

    # Q-Dome claim?
    driver.find_element(by=By.NAME, value="field_qdome").click()
    time.sleep(0.5)

    # 5-digit-code
    for i in range(1, 11):

        
        if i < 10:
            dCode = str(row[f"Damage Code0{i}"])
        else:
            dCode = str(row[f"Damage Code{i}"])
            
        print(f"Damage Code{i}: {dCode}")
        
        # 없으면 반복 중지
        if dCode == "nan":
            break
        else:
            driver.find_element(by=By.NAME, value="field_cteilnr").send_keys(dCode)
            waitLoading()
            driver.find_element(by=By.NAME, value="speichern_ccode").click()
            waitLoading()
            driver.implicitly_wait(30)
            
            try:
                driver.find_element(by=By.XPATH, value='//*[@id="mainpart"]/ul/li')
                memo(file_name, row, f"damage code{i} wrong")
                print(f"Damage Code{i} 오류")
                return False
            except:
                pass

    # submit
    driver.find_element(by=By.NAME, value="speichern").click() # submit 버튼 클릭
    driver.implicitly_wait(30)
    waitLoading()

    # return
    return True
    

def archive(driver, logFile, row, archiveError = False):
    # archive 버튼 클릭
    driver.find_element(by=By.LINK_TEXT, value="archive").click()
    waitLoading()

    # 파일 버튼 클릭
    # driver.find_element(by=By.XPATH, value='//*[@id="mainpart"]/table[4]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/img').click()
    wait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mainpart"]/table[5]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/img'))).click()
    waitLoading()

    # 팝업 창으로
    driver.switch_to.window(driver.window_handles[1])
    
    fRO = searchFileName("RO", row)
    sRO = "claim invoice"

    fBL = searchFileName("BL", row)
    sBL = "B/L"

    fPicture = searchFileName("PICTURE", row)
    sPicture = "damage photo"

    fLiabilityNotice = searchFileName("LIABILITY NOTICE", row)
    sLiabilityNotice = "notice of liability, resp. objection to notice of liability"

    ## damage report는 업로드 안함 (폴더가 비어있음)

    fClaimSummary = searchFileName("CLAIM SUMMARY", row)
    sClaimSummary = "Notification of the claim"

    fEmail = searchEmail(row)
    sEmail = "Incoming correspondence from claimant"

    fList = searchFileName("LIST", row) # 얘만 list 아님
    sList = "Incoming correspondence from claimant"

    fileList = [fRO, fBL, fPicture, fLiabilityNotice, fClaimSummary, fEmail, fList]
    selectionList = [sRO, sBL, sPicture, sLiabilityNotice, sClaimSummary, sEmail, sList]

    # 실제 업로드 로직
    uploadArchive(driver, logFile, fileList, selectionList)


    # 파악된 파일 개수
    uploadFileNum = uploadFileNumCheck(fileList)

    # 최종 업로드된 파일 개수
    uploadedFileNum = uploadedFileNumCheck(driver)

    # 업로드 상태 확인

    ## 파일의 개수가 안맞는 경우
    if uploadedFileNum != uploadFileNum + 1:
        print("올라간 파일 수와 올릴 파일 수가 다릅니다")
        return True

    ## 파일의 개수가 9개 이하인 경우
    if uploadedFileNum < 9:
        print("업로드된 파일의 수가 9개보다 작습니다")
        return True      
    

    # Claim summary = notification of the claim
    # E-mail = Incoming correspondence from claimant
    # Liability notice = Liability notice
    # List = Incoming correspondence from claimant
    # Pictures = pictures 
    # RO = claim invoice

def claim(driver):
    # 좌측 cliam 클릭
    driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table[12]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/a").click()
    waitLoading()

    # claimant
    claimant = driver.find_element(by=By.NAME, value="field_ansprse")
    claimant.send_keys("Mercedes-Benz Korea")
    time.sleep(0.5)
    claimant.send_keys(Keys.ENTER)

    # 팝업 창
    driver.switch_to.window(driver.window_handles[1])
    waitLoading()

    # + 버튼 클릭
    driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr[1]/td[1]/input").click()
    driver.implicitly_wait(10)

    # 창 닫혔는지 검사
    while True:
        time.sleep(2)
        try:
            driver.switch_to.window(driver.window_handles[1])
            continue
        except:
            driver.switch_to.window(driver.window_handles[0])
            waitLoading()
            break
    driver.implicitly_wait(30)

    # 창 닫힌 후 submit 버튼 누르기    
    driver.find_element(by=By.NAME, value="speichern").click()
    waitLoading()

    # 완료

def receipts(driver, row):
    # 좌측 receipts 버튼 클릭
    driver.find_element(by=By.XPATH, value='/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table[13]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/a').click()
    waitLoading()

    # new 버튼 클릭
    driver.find_element(by=By.XPATH, value='//*[@id="mainpart"]/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table[1]/tbody/tr/td[2]/a').click()
    waitLoading()

    # type of receipt
    select = Select(driver.find_element(by=By.NAME, value="field_bel"))
    select.select_by_value("RK")
    waitLoading()

    # involved party
    involvedParty = driver.find_element(by=By.NAME, value="field_belansprse")
    involvedParty.send_keys("Mercedes-Benz Korea")
    involvedParty.send_keys(Keys.ENTER)
    
    # 팝업 창 전환
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(5)
    waitLoading()

    # + 버튼 클릭
    driver.implicitly_wait(10)
    driver.find_element(by=By.XPATH, value="/html/body/table[2]/tbody/tr[1]/td[1]/input").click()

    # 창 닫혔는지 검사
    while True:
        time.sleep(2)
        try:
            driver.switch_to.window(driver.window_handles[1])
            continue
        except:
            driver.switch_to.window(driver.window_handles[0])
            break
    time.sleep(2)
    
    # receipt number
    driver.find_element(by=By.NAME, value="field_belref").send_keys(row["Repair No."])
    time.sleep(0.5)

    # date of receipt
    receiptYear = row["Closing Date"][0:4]
    receiptMonth = row["Closing Date"][5:7]
    receiptDay = row["Closing Date"][-2:]

    driver.find_element(by=By.NAME, value="subfield_beldat_day").send_keys(receiptDay)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_beldat_month").send_keys(receiptMonth)
    time.sleep(0.5)
    driver.find_element(by=By.NAME, value="subfield_beldat_year").send_keys(receiptYear)
    time.sleep(0.5)

    # tax key
    taxKey = Select(driver.find_element(by=By.NAME, value="field_belstschl"))
    taxKey.select_by_value("100")
    time.sleep(1)

    # amount on receipt nett KRW -> 한 개만 입력하면 나머지는 자동빵
    driver.find_element(by=By.NAME, value="field_betrag_bwhg").send_keys(row["Sub Total"])
    waitLoading()

    # Submit 버튼 클릭
    driver.implicitly_wait(30)
    driver.find_element(by=By.NAME, value="bt_speichern").click()
    waitLoading()

    # >> 버튼 클릭
    driver.find_element(by=By.XPATH, value='//*[@id="mainpart"]/form/table/tbody/tr[3]/td[6]/a[4]/img').click()

    # type of procedure
    typeOfProcedure = Select(driver.find_element(by=By.NAME, value="field_atyp"))
    typeOfProcedure.select_by_value("VR")
    waitLoading()

    # new claim status broker/ins.
    typeOfProcedure = Select(driver.find_element(by=By.NAME, value="field_sst"))
    typeOfProcedure.select_by_value("G")
    waitLoading()

    # delete reserves
    driver.find_element(by=By.NAME, value="field_reskz").click()
    time.sleep(1)

    # date of booking / cost centre
    bookingYear = row["Date of booking"][0:4]
    bookingMonth = row["Date of booking"][5:7]
    bookingDay = row["Date of booking"][-2:]

    bookingDayInput = driver.find_element(by=By.NAME, value="subfield_budat_day")
    bookingDayInput.clear()
    bookingDayInput.send_keys(bookingDay)
    time.sleep(0.5)

    bookingMonthInput = driver.find_element(by=By.NAME, value="subfield_budat_month")
    bookingMonthInput.clear()
    bookingMonthInput.send_keys(bookingMonth)
    time.sleep(0.5)

    bookingYearInput = driver.find_element(by=By.NAME, value="subfield_budat_year")
    bookingYearInput.clear()
    bookingYearInput.send_keys(bookingYear)
    time.sleep(0.5)


    # submit 버튼 클릭
    driver.find_element(by=By.NAME, value="bt_speichern").click()
    waitLoading()

def status(driver):
    # 좌측 status 버튼 클릭
    driver.find_element(by=By.XPATH, value="/html/body/table/tbody/tr[3]/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table[5]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/table[18]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]/a").click()
    waitLoading()

    # status
    typeOfProcedure = Select(driver.find_element(by=By.NAME, value="field_sst"))
    typeOfProcedure.select_by_value("B")

    # submit
    driver.find_element(by=By.NAME, value="Abschicken").click()
    waitLoading()
