from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd


chrome_driver_path = "path_of_driver" #Enter the filepath where your chrome driver executable is saved
driver = webdriver.Chrome(executable_path=chrome_driver_path)

data = []
failed_NPIs = []


def loopNPIs(npi):
    """
    Uses a Chrome Webdriver instance to query the eMedNY OPRA site to verify provider enrollment data for inputted NPI numbers.
    :param npi: takes a provider's NPI
    :return: nothing is directly returned by the function, but it saves the query results as dictionaries into the list called data. If the NPI doesn't return results, then that NPI will be saved into the list called failed_NPIs.
    """
    driver.get("https://www.emedny.org/info/opra.aspx")
    driver.find_element(By.XPATH, '//*[@id="Main_txtvalue"]').send_keys(str(npi) + Keys.ENTER)
    try:
        WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CLASS_NAME, "crosswalksTableStyle")))
    except TimeoutException:
        failed_NPIs.append(npi)
        pass

    rows = len(driver.find_elements(By.XPATH, '//*[@id="Main_grdvTable"]/tbody/tr'))
    cols = len(driver.find_elements(By.XPATH, '//*[@id="Main_grdvTable"]/tbody/tr[1]/th'))

    for i in range(2, rows+1):
        row = []
        for j in range(1, cols+1):
            row_data = driver.find_element(By.XPATH, f'//*[@id="Main_grdvTable"]/tbody/tr[{str(i)}]/td[{str(j)}]')
            row.append(row_data.text)
        data.append({
            "NPI": row[0],
            "License Number": row[1],
            "Profession Code": row[2],
            "Name": row[3]
            })


def save_data():
    df = pd.DataFrame.from_dict(data)
    df.drop_duplicates(subset="NPI", keep="first", inplace=True)
    df.to_csv("passed_NPIs.csv", index=False)

    with open('failed_NPIs.txt', 'w') as f:
        for item in failed_NPIs:
            f.write(f"{item}\n")


file = pd.read_csv("NPIs.csv")
raw_NPIs = file['Attend Prov NPI'].tolist()

for each in raw_NPIs:
    loopNPIs(each)

save_data()

driver.close()
