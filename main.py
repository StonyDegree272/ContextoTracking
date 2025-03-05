#imports

from selenium import webdriver
from time import sleep
from datetime import date

from selenium.webdriver.common.by import By
import random



#initialize global variables

driver = webdriver.Chrome()
driver.get('https://contexto.me/')

guesses = []
textString = ""
dev = False

def main():
    numHints = 0
    if dev:
        print("done loading")

    while True:
# wait until a first answer is provided
        if not firstWordPlayed():
            continue

#only happen once per guess
        if len(guesses)>0:
            try:
                if type(guesses[len(guesses)-1]) == str and guesses[len(guesses)-1] == textString:
                    continue
                else:
                    if guesses[len(guesses)-1][0] == textString.split("\n")[0]:
                        continue
            except:
                continue

#check if Hint is used
        if hint(numHints):
            guesses.append("hint:")
            numHints = int(driver.find_element(By.XPATH, "//div[@class='info-bar']//span[position()=6]").text)
            if dev:
                print("hint:")

#record answer
        takeCareOfAnswer()
        if dev:
            print(guesses[len(guesses)-1])

#check for win
        if done():
            return

def firstWordPlayed():
    global textString
    try:
        textString = getAnswer()
        return True
    except:
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
        if guesses[len(guesses) - 1][1]== '1':
            return True
    except:
        return False

    return False

def takeCareOfAnswer():
    if textString == "This word doesn't count, it's too common" or "The word " in textString:
        guesses.append(textString)
    else:
        if dev:
            print("The answer is: "+textString)
        guess = textString.split('\n')
        guesses.append(guess)

def writeAnswer():
    file = open("trackingData\\"+str(date.today())+" - "+str(int(random.random()*1000000))+".txt", "w")
    for i in range(len(guesses)):
        try:
            file.write(guesses[i][0]+"\t"+guesses[i][1]+'\n')
        except IndexError:
            file.write(guesses[i]+' \n')

    file.close()
    if dev:
        print("doneWriting")



#run
main()
writeAnswer()

if dev:
    print ("Done")