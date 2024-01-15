'''
Created on 21 Tem 2023

@author: yusuf
'''

import pytest
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium. common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import json

def test_productFollowTestCase():

    f = open ('data.json', "r") 
    # Reading from file
    data = json.loads(f.read())

    #Open LogIn Page
    driver = webdriver.Chrome()
    driver.get(f'{data["mainUrl"]}/akakcem/giris/')
    
    #Enter email
    driver.find_element(By.ID, "life").send_keys(data['email'])
    sleep(1)
    
    #Enter password
    driver.find_element(By.ID, "lifp").send_keys(data['password'])
    sleep(1)
    
    #Click Giriş button
    driver.find_element(By.ID, "lfb").click()
    sleep(1)
    
    #Check Success of Login process
    mainPageLoaded = False
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/header/div[2]/div/a')))
        mainPageLoaded = True
    except TimeoutException as e:
        assert mainPageLoaded, f"Verify That Main Page could not be loaded! : FAILED : {e}"
              
    assert mainPageLoaded, "Verify That user Logged in successfully!"
    
    #Type iphone to searchBox
    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[3]/form/span/input').send_keys("iphone")
    
    #Press Enter
    driver.find_element(By.XPATH, '/html/body/div[1]/header/div[3]/form/span/input').send_keys(Keys.RETURN)
    
    #Check searching process is successful
    searchSuccess = False
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/h1')))
        searchSuccess = True
    except Exception as e:
        assert searchSuccess, f"Verify That related searching is successful : FAILED : {e}" 
        
    assert searchSuccess, "Verify That related searching is successful"
    
    #Check that related products are listed
    searchResultSuccess = False
    try:
        element = driver.find_element(By.XPATH, '/html/body/h2')
        if element != None:
            searchResultSuccess = True
    except Exception as e:
        assert searchResultSuccess, f"Verify That related search result are displayed successfully : FAILED : {e}"
    
    assert searchResultSuccess, "Verify That related search result are displayed successfully"
    
    #Open product Page
    parent_element = driver.find_element(By.XPATH, '/html/body/div[2]/ul')
    products = parent_element.find_elements(By.TAG_NAME, 'a')
    
    for element in products:
        firstElement = element
        buttons = parent_element.find_elements(By.CLASS_NAME, 'bt_v8')
        for button in buttons:
            button.click()
            break
        break
    
    try:
        firstElement.click()
    except Exception as e:
        print(e)
    
    productPageOpened = False
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/nav/ol/li[5]/a/span')))
        productPageOpened = True
    except Exception as e:
        assert productPageOpened, f"Verify That related page of product is displayed successfully : FAILED {e}"
    
    assert productPageOpened, "Verify That related page of product is displayed successfully"
    
    #Click Takip Et Button
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[1]/div/div[3]/div/div/span'))).click()
    except Exception as e:
        print(e) 
    successfullyFollowed = False
    
    #Check product is followed
    element = driver.find_element(By.XPATH, '/html/body/main/div[1]/div/div[3]/div/div/span')
    if "Takibi Bırak" in element.get_attribute('innerHTML'):
        successfullyFollowed = True
    assert successfullyFollowed, "Verify That product is followed successfully"
    
   
    #Get product Title
    productTitle = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[1]/h1").get_attribute("innerHTML")
    
    #Open "Takip Ettiklerim Page
    driver.get(f'{data["mainUrl"]}/akakcem/takip-listem/')
    sleep(2)
    
    parent_element = driver.find_element(By.XPATH, '/html/body/div[2]/div/form/ul')
    products = parent_element.find_elements(By.TAG_NAME, 'a')
    
    #Verify product is in Takip Listem
    successfullyFollowed = False
    for product in products:
        if product.get_attribute("title") == productTitle:
            successfullyFollowed = True
            break
    assert successfullyFollowed, "Verify that followed product is in Following Item List"