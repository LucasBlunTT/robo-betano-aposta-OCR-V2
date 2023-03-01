import mss
import mss.tools
import pyautogui
import re
import pytesseract
import cv2
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

def extrairImagemVela():    
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2

        # The screen part to capture
        monitor = {
            "top": 300,
            "left": 2100,
            "width": 558,
            "height": 230,
            "mon": monitor_number,
        }
        
        output = "vela.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        print(output)
        sleep(1)

def analisaVela():   
    
    extrairImagemVela()            
    
    imagemVela = cv2.imread("vela.png")
    # Converte a imagem para o formato de texto usando o pytesseract
    conteudoVela = pytesseract.image_to_string(imagemVela, lang="por")
    
    print(conteudoVela)

    vooLonge = re.findall(r'\bVOOU PARA LONGE\b', conteudoVela) 
    valorVela = re.findall(r'\d+\.\d+', conteudoVela) 
    
    print(vooLonge)
    print(valorVela)
    
analisaVela()