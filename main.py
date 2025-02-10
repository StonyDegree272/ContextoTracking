#imports

from Scripts.activate_this import prev_length
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep

from selenium.webdriver.common.by import By
import requests
import random
from selenium.webdriver.support.wait import WebDriverWait


#initialize global variables
WORDS = requests.get("https://www.mit.edu/~ecprice/wordlist.10000").content.splitlines()

driver = webdriver.Chrome()
driver.get('https://contexto.me/')
word_box = driver.find_element(By.NAME,"word")

guesses = []


def main():
    numHints = 0
    print("done loading")

    while True:
# wait until a first answer is provided
        if not firstWordPlayed():
            continue

#only happen once per guess
        if len(guesses)>0:
            try:
                if type(guesses[len(guesses)-1]) == str and guesses[len(guesses)-1] == getAnswer():
                    continue
                else:
                    if guesses[len(guesses)-1][0] == getAnswer().split("\n")[0]:
                        continue
            except:
                continue

#check if Hint is used
        if hint(numHints):
            guesses.append("hint:")
            numHints = int(driver.find_element(By.XPATH, "//div[@class='info-bar']//span[position()=6]").text)
            print("hint:")

#record answer
        takeCareOfAnswer()
        print(getAnswer())

#check for win
        if(done()):
            return

def firstWordPlayed():
    try:
        getAnswer()
        return True
    except:
        return False

    return False

def hint(hints):
    try:
        if int(driver.find_element(By.XPATH, "//div[@class='info-bar']//span[position()=6]").text) != hints:
            return True
    except:
        return False

    return False

def getAnswer():
    sleep(0.05)
    try:
        answer = driver.find_element(By.XPATH,"//div[@class='message']//div[@class='message-text']")
        if answer.text == "Calculating...":
            getAnswer()

        return answer.text
    except:
        answer = driver.find_elements(By.XPATH,"//div[@class='message']//div//div//div[@class='row']//span")
        return answer[0].text + "\n" + answer[1].text

def done():
    try:
        if(guesses[len(guesses)-1][1]=='1'):
            return True
    except:
        return False

    return False

def takeCareOfAnswer():
    if getAnswer() == "This word doesn't count, it's too common" or "The word " in getAnswer():
        guesses.append(getAnswer())
    else:
        guess = getAnswer().split('\n')
        guesses.append(guess)

def writeAnswer():
    file = open("trackingData\\"+str(int(random.random()*100000000000))+".txt", "w")
    for i in range(len(guesses)):
        if type(guesses[i]) == str:
            file.write(guesses[i]+' \n')
            continue
        else:
            file.write(guesses[i][0]+"\t"+guesses[i][1]+'\n')

    file.close()
    print("doneWriting")



#run
main()
writeAnswer()
print ("Done")