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

# pyautogui.mouseInfo()

def incrementaRed(numero):
    contadorRed =+ numero
    return contadorRed
    
def jogar():
    pyautogui.moveTo(3025, 855)  # Entrada betano
    pyautogui.click()
    print("...::: ENTROU COM A APOSTA :::...")

    sleep(2.5)
    analisaVela()


def jogarGale():
    pyautogui.moveTo(3025, 855)  # Entrada betano
    pyautogui.click()
    print("...::: ENTROU COM O GALE :::...")
    analisaGreen()


def extrairImagem():
    with mss.mss() as sct:
        # Get information of monitor 2
        monitor_number = 2

        # The screen part to capture
        monitor = {
            "top": 770,
            "left": 3250,
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
        # sleep(1)


def analisaVela():
    while True:
        extrairImagemVelaVoou()

        imagemVoou = cv2.imread("voou.png")

        # Converte a imagem para o formato de texto usando o pytesseract
        imagemVoou = pytesseract.image_to_string(imagemVoou, lang="por")

        vooLonge = re.findall(r"\bVOOU PARA LONGE\b", imagemVoou)
        print("ESPERANDO A VELA TERMINAR DE SUBIR")

        if len(vooLonge) != 0:
            pyautogui.click(2933, 564)
            sleep(1)
            pyautogui.hotkey("f12")
            sleep(2)
            pyautogui.click(3306, 166)
            sleep(1)
            pyautogui.click(2470, 450)
            sleep(1)
            pyautogui.click(3479, 465)
            sleep(1)
            pyautogui.hotkey("ctrl", "c")
            oddCrash = pyperclip.paste()
            pyautogui.hotkey("f12")
            oddCrash = re.findall(r"\d+\.\d+", oddCrash)
            print("ODD NO ARRAY")
            print(oddCrash)
            if len(oddCrash) == 0:
                oddCrash = None
                print("ERRO AO DETECTAR ODD PARA FAZER GALE, RETORNANDO ANALISAR")
                break
            elif len(oddCrash) != 0:
                oddCrash = float(oddCrash[0])
                if oddCrash < 2.00:
                    oddCrash = None
                    print("JOGANDO GALE")
                    jogarGale()
                    break
                elif oddCrash > 2.00:
                    oddCrash = None
                    incrementaRed(0)
                    print("SEM NECESSIDADE DO GALE, VOLTANDO ANALISAR O GRUPO")
                    sleep(7)
                    break
                else:
                    print("VERIFICANDO NECESSIDADE DO GALE")


def analisaGreen():
    while True:
        extrairImagem()
        imagem = cv2.imread("entrada.png")
        # Converte a imagem para o formato de texto usando o pytesseract
        textoGreen = pytesseract.image_to_string(imagem, lang="por")

        fogueteFinalizado = re.findall(r"\bFoguetinho finalizado\b", textoGreen)
        red = re.findall(r"\bRed\b", textoGreen)
        pipes = re.findall(r"\|", textoGreen)

        if len(fogueteFinalizado) != 0 and len(pipes) >= 2 and len(red) == 1:
            incrementaRed(1)
            print("DEU UM RED")
            if(incrementaRed() == 3):
                print("CHEGOU AO TOTAL DE 3 RED. ROBO VOLTARA EM 1 HORA!")
                esperaUmaHora()       
            break
        elif len(fogueteFinalizado) != 0 and len(red) == 0 and len(pipes) == 1 or len(pipes) == 0:
            break
        else:
            print("...::: VERIFICANDO GREEN :::...")
            
def esperaUmaHora():
    sleep(3600)

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