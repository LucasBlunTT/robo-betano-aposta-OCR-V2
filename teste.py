import mss
import mss.tools
import pyautogui
import re
import pytesseract
import cv2
import pyperclip
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

#pyautogui.mouseInfo()

def extrairImagemVelaVoou():
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2

        # The screen part to capture
        monitor = {
            "top": 355,
            "left": 2200,
            "width": 296,
            "height": 140,
            "mon": monitor_number,
        }

        output = "voou.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)
        sleep(1)

def analisaVela():
    while(True):
        extrairImagemVelaVoou()
        
        imagemVoou = cv2.imread("voou.png")
    
        # Converte a imagem para o formato de texto usando o pytesseract
        imagemVoou = pytesseract.image_to_string(imagemVoou, lang="por")

        vooLonge = re.findall(r'\bVOOU PARA LONGE\b', imagemVoou)
        print(vooLonge)
        
        if len(vooLonge) != 0:
            sleep(3)
            pyautogui.moveTo(2473,369,duration=1)
            pyautogui.click()
             
            sleep(1)
            pyautogui.moveTo(2850,350)
           
            pyautogui.doubleClick()
            pyautogui.hotkey('ctrl','c')           
            
            oddCrash = pyperclip.paste()
            oddCrash = re.findall(r'\d+\.\d+', oddCrash)    
            oddCrash = float(oddCrash[0])
            print(oddCrash)
            
            pyautogui.hotkey('enter')
            
            if(oddCrash < 2.00):
                print("JOGANDO GALE")
                break
                #jogarGale()
        else:
            print("VERIFICANDO NECESSIDADE DO GALE")
    
analisaVela()
