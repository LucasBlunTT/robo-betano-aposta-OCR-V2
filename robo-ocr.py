import mss
import mss.tools
import pyautogui
import re
import pytesseract
import cv2
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
palavraEntrada = 'Entrada'
palavraGreen = 'GREEN'
palavraFogueteConfirmado = 'Foguetinho confirmado'
palavraRed = 'Red'
palavraPossivelEntrada = 'ATENÇÃO, POSSÍVEL ENTRADA'

pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

def jogar():
    #pyautogui.moveTo(3038,840) # entrada betano
    pyautogui.moveTo(3105,654)
    pyautogui.click()
    print('...::: ENTROU COM A APOSTA :::...')
    
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
    
while (True):
    extrairImagem()    
    
    imagem = cv2.imread("entrada.png")
    # Converte a imagem para o formato de texto usando o pytesseract
    texto = pytesseract.image_to_string(imagem, lang="por")

    confirmacaoFoguete = re.findall(r'\bFoguetinho confirmado\b', texto)    
    entrada = re.findall(r'\bEntrada\b', texto) 
    odd = re.findall(r'\d+\.\d+', texto)   
    
    if  len(confirmacaoFoguete) != 0 and len(entrada) != 0 and len(odd) != 0:
        variavelFoguete = confirmacaoFoguete[0]
        variavelEntrada = entrada[0] 
        variavelOdd = odd[0]
          
        print(variavelFoguete)
        print(variavelEntrada)
        print(variavelOdd)
        
        jogar()
    else:
        print("ESPERANDO ENTRADA")
    
