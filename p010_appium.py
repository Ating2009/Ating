# coding=utf-8

from appium import webdriver

desired_caps = {
  'platformName': 'Android',
  'deviceName': '37b62766',
  'platformVersion': '7.0',
  'appPackage': 'com.tencent.mm',
  'appActivity': 'com.tencent.mm.ui.LauncherUI'
 }

driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)