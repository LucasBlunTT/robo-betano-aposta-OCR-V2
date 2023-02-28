import mss
import mss.tools
import pyperclip
import pyautogui
import re
import pytesseract
import cv2
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
entrada = 'Entrada'
green = 'GREEN'
red = 'Red'

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
            "top": 650,
            "left": 3250,
            "width": 572,
            "height": 376,
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
  
def lerConteudoImagem():
    imagem = cv2.imread("entrada.png")
    # Converte a imagem para o formato de texto usando o pytesseract
    texto = pytesseract.image_to_string(imagem, lang="por")

    valorOdd = re.findall(r'\d+\.\d+', texto)    
    valorOdd = float(valorOdd[1])
    
    if(valorOdd == None or valorOdd == ''):
        valorOdd = ''
    
    palavraEntrada = re.findall(r'Entrada', texto)
    palavraEntrada = palavraEntrada[0]
    
    if(palavraEntrada == None or palavraEntrada == ''):
        palavraEntrada = ''
    
    palavraGreen = re.findall(r'GREEN', texto)
    palavraGreen = palavraGreen[0]

    if(palavraGreen == None or palavraGreen == ''):
     palavraGreen = ''
    

    data = {"odd": valorOdd, "entrada": palavraEntrada, "green": palavraGreen}
    print(data)
    return data

def verificarGreen():
    while (True):
        extrairImagem()
        lerConteudoImagem()
        if(data['green'] == green):
            break           
        else:
              print('VERIFICANDO GREEN PARA CONTINUAR')
    
while (True):
    extrairImagem()    
    data = lerConteudoImagem()
    if(data['entrada'] == entrada):   
        jogar()
        verificarGreen()
    else:    
        print('Esperando ENTRADA ')
    