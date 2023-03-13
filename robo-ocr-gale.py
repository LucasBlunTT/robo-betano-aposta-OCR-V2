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

contadorGale = 0
    
def jogar():
    pyautogui.moveTo(529,759)  # Entrada betano
    pyautogui.click()
    print("...::: ENTROU COM A APOSTA :::...")

    sleep(3)
    analisaVela()

def jogarGale():
    sleep(1.7)
    global contadorGale
    
    contadorGale +=1
    
    if(contadorGale == 1):
        print("Fez G1")
        pyautogui.click(334,738)
        pyautogui.click(334,738)
        pyautogui.moveTo(529,759)  # Entrada betano
        pyautogui.click()
   # elif(contadorGale == 2):
   #     print("Fez G2")
   #     pyautogui.click(334,738, duration=0.5)
   #     sleep(0.5)
   #     pyautogui.click(334,738, duration=0.5)
   #     pyautogui.moveTo(529,759)  # Entrada betano
   #     pyautogui.click()
            
    
    print("...::: ENTROU COM O GALE :::...")
    sleep(4.5)
    analisaVela()

def extrairImagem():
    sleep(1)
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2

        # The screen part to capture
        monitor = {
            "top": 750,
            "left": 950,
            "width": 558,
            "height": 230,
            "mon": monitor_number,
        }

        output = "entrada.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        # sleep(1)
        
def zeraGale():
    print("Zerando entrada BETANO")
    pyautogui.click(207,739)
    pyautogui.click(207,739)
    
def extrairImagemVelaVoou():
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2

        # The screen part to capture
        monitor = {
            "top": 435,
            "left": 295,
            "width": 296,
            "height": 140,
            "mon": monitor_number,
        }

        output = "voou.png".format(**monitor)

        # Grab the data
        sct_img = sct.grab(monitor)

        # Save to the picture file
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
        # sleep(1)

def analisaVela():
    while True:
        global contadorGale
        if (contadorGale == 1):     
            analisaGale()
            break
        
        extrairImagemVelaVoou()

        imagemVoou = cv2.imread("voou.png")

        # Converte a imagem para o formato de texto usando o pytesseract
        imagemVoou = pytesseract.image_to_string(imagemVoou, lang="por")

        vooLonge = re.findall(r"\bVOOU PARA LONGE\b", imagemVoou)
        print("ESPERANDO A VELA TERMINAR DE SUBIR")

        if len(vooLonge) != 0:
            pyautogui.click(431,512) #Click na tela só para focalizar               
            pyautogui.hotkey("ctrl", "shift", "c") #Hotkey para abrir o DEVTOOLS  
            sleep(2)       
            pyautogui.click(64,451) #Movendo até a odd
            sleep(2)          
            pyautogui.hotkey("ctrl", "c")  #Copia a ODD
            pyautogui.hotkey("f12")
            oddCrash = pyperclip.paste()            
            oddCrash = re.findall(r"\d+\.\d+", oddCrash)
            print("ODD NO ARRAY")
            print(oddCrash)
            if len(oddCrash) == 0:
                oddCrash = None
                print("ERRO AO DETECTAR ODD PARA FAZER GALE, RETORNANDO ANALISAR")
                break
            elif len(oddCrash) != 0:
                oddCrash = float(oddCrash[0])                
                if oddCrash < 1.50:
                    oddCrash = None
                    print("JOGANDO GALE")
                    jogarGale()
                    break
                elif oddCrash > 1.50:
                    contadorGale = 0
                    oddCrash = None              
                    print("SEM NECESSIDADE DO GALE, VOLTANDO ANALISAR O GRUPO")
                    analisaGreen()
                    sleep(7)
                    break
                else:
                    print("VERIFICANDO NECESSIDADE DO GALE")


def analisaGreen():
    global contadorGale
    contadorGale = 0
    while True:
        extrairImagem()
        imagem = cv2.imread("entrada.png")
        # Converte a imagem para o formato de texto usando o pytesseract
        textoGreen = pytesseract.image_to_string(imagem, lang="por")

        fogueteFinalizado = re.findall(r"\bFoguetinho finalizado\b", textoGreen)
        red = re.findall(r"\bRed\b", textoGreen)
        #pipes = re.findall(r"\|", textoGreen)

        if len(fogueteFinalizado) != 0 or len(red) != 0:
            break       
        else:
            print("...::: VERIFICANDO GREEN :::...")
            
def analisaGale():
    global contadorGale
    contadorGale = 0
    while True:
        extrairImagem()
        imagem = cv2.imread("entrada.png")
        # Converte a imagem para o formato de texto usando o pytesseract
        textoGreen = pytesseract.image_to_string(imagem, lang="por")

        fogueteFinalizado = re.findall(r"\bFoguetinho finalizado\b", textoGreen)
        red = re.findall(r"\bRed\b", textoGreen)
        #pipes = re.findall(r"\|", textoGreen)

        if len(fogueteFinalizado) != 0 or len(red) != 0:
            zeraGale()
            break       
        else:
            print("...::: VERIFICANDO GREEN :::...")                          

while True:
    extrairImagem()

    imagem = cv2.imread("entrada.png")
    # Converte a imagem para o formato de texto usando o pytesseract
    texto = pytesseract.image_to_string(imagem, lang="por")
    confirmacaoFoguete = re.findall(r"\bFoguetinho confirmado\b", texto)
    entrada = re.findall(r"\bEntrada\b", texto)
    odd = re.findall(r"\d+\.\d+", texto)

    if len(confirmacaoFoguete) != 0 and len(entrada) != 0 and len(odd) != 0:
        variavelFoguete = confirmacaoFoguete[0]
        variavelEntrada = entrada[0]
        variavelOdd = odd[0]

        jogar()
    else:
        print("ESPERANDO ENTRADA")
        
        
#pyautogui.mouseInfo()
        