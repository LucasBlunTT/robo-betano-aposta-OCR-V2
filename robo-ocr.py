import mss
import mss.tools
import pyautogui
import re
import pytesseract
import cv2
import pyperclip
from time import sleep

caminho = r"C:\Program Files\Tesseract-OCR"
palavraEntrada = 'Entrada'
palavraGreen = 'GREEN'
palavraFogueteConfirmado = 'Foguetinho confirmado'
palavraRed = 'Red'
palavraPossivelEntrada = 'ATENÇÃO, POSSÍVEL ENTRADA'

pytesseract.pytesseract.tesseract_cmd = caminho + r"\tesseract.exe"

# pyautogui.mouseInfo()


def jogar():
    # pyautogui.moveTo(3025,855) # Entrada betano
    pyautogui.moveTo(3105, 654)  # Entrada de testes
    pyautogui.click()
    print('...::: ENTROU COM A APOSTA :::...')
    sleep(1)
    # analisaGreen()
    analisaVela()


def jogarGale():
    # pyautogui.moveTo(3025,855) # Entrada betano
    pyautogui.moveTo(3105, 654)  # Entrada de testes
    pyautogui.click()
    print('...::: ENTROU COM O GALE :::...')


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
        print(output)
        sleep(1)


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
            pyautogui.moveTo(2473, 369, duration=1)
            pyautogui.click()

            sleep(1)
            pyautogui.moveTo(2850, 350)

            pyautogui.doubleClick()
            pyautogui.hotkey('ctrl', 'c')

            oddCrash = pyperclip.paste()
            oddCrash = re.findall(r'\d+\.\d+', oddCrash)
            oddCrash = float(oddCrash[0])
            print(oddCrash)

            pyautogui.hotkey('enter')

            if(oddCrash < 2.00):
                print("JOGANDO GALE")
                jogarGale()
                break
                
        else:
            print("VERIFICANDO NECESSIDADE DO GALE")

# def analisaGreen():
   # while(True):
    #    extrairImagem()
    #    imagem = cv2.imread("entrada.png")
    #    # Converte a imagem para o formato de texto usando o pytesseract
    #    textoGreen = pytesseract.image_to_string(imagem, lang="por")
    #
    #    fogueteFinalizado = re.findall(r'\bFoguetinho finalizado\b', textoGreen)
    #
    #    #print(confirmacaoGreen)
    #    print(fogueteFinalizado)
    #
    #    #if len(confirmacaoGreen) != 0 and len(fogueteFinalizado) != 0:
    #    if len(fogueteFinalizado) != 0:
    #        break
    #    else:
    #         print('...::: VERIFICANDO GREEN :::...')


while(True):
    extrairImagem()

    imagem = cv2.imread("entrada.png")
    # Converte a imagem para o formato de texto usando o pytesseract
    texto = pytesseract.image_to_string(imagem, lang="por")
    print(texto)
    confirmacaoFoguete = re.findall(r'\bFoguetinho confirmado\b', texto)
    entrada = re.findall(r'\bEntrada\b', texto)
    odd = re.findall(r'\d+\.\d+', texto)

    if len(confirmacaoFoguete) != 0 and len(entrada) != 0 and len(odd) != 0:
        variavelFoguete = confirmacaoFoguete[0]
        variavelEntrada = entrada[0]
        variavelOdd = odd[0]

        print(variavelFoguete)
        print(variavelEntrada)
        print(variavelOdd)

        jogar()
    else:
        print("ESPERANDO ENTRADA")
