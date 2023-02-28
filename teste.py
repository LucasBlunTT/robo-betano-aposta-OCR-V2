import mss
import mss.tools
import pyautogui
import re
import pytesseract
import cv2
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

def extrairImagem():    
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2
        mon = sct.monitors[monitor_number]

        # The screen part to capture
        monitor = {
            "top": 770,
            "left": 3250,
            "width": 558,
            "height": 230,
            "mon": monitor_number,
        }
        #output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)
        output = "entrada.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)
        sleep(1)


while(True):
        extrairImagem()            
        imagem = cv2.imread("entrada.png")
        # Converte a imagem para o formato de texto usando o pytesseract
        textoGreen = pytesseract.image_to_string(imagem, lang="por")
        
        confirmacaoGreen = re.findall(r'\bGREEN\b', textoGreen)
        fogueteFinalizado = re.findall(r'\bFoguetinho finalizado\b', textoGreen) 
        
        print(confirmacaoGreen)
        print(fogueteFinalizado)
        
        if len(confirmacaoGreen) != 0 and len(fogueteFinalizado) != 0:
            break
        else:
             print('...::: VERIFICANDO GREEN :::...')