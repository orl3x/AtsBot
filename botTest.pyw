import pyperclip
import tkinter as tk
import tkinter.ttk as ttk
from customModelSettingsAts1 import *
import modelsDB

def passwordWindow():
    passwordWindow = tk.Tk()
    passwordWindow.geometry("230x70")
    passwordWindow.title("Iniciar Sesión")
    passwordLabel = tk.Label(passwordWindow, text="Ingrese la contraseña")
    passwordLabel.config(font=('ARIAL', 13, 'bold'), fg="green")
    passwordEntry = tk.Entry(passwordWindow, show="*")
    passwordEntry.config(font=('ARIAL', 13), fg="black", bg="white", relief="groove", borderwidth="2")


    def enterEvent(event):
        if passwordEntry.get() == "201101":
            passwordWindow.destroy()
            changeModel()
        else:
            pag.alert("Contraseña Incorrecta")
            passwordWindow.destroy()

    def endProgram():
        passwordWindow.destroy()

    passwordWindow.bind('<Return>', enterEvent)
    passwordLabel.pack()
    passwordEntry.pack()
    passwordWindow.focus()
    passwordEntry.focus()
    passwordWindow.protocol("WM_DELETE_WINDOW", endProgram)
    passwordWindow.mainloop()



def scanProduct():
    print("Ejecutando scan product")
    global root
    root = tk.Tk()
    root.geometry("600x150")
    root.title("ATS Bot")
    label = tk.Label(root, text="Escanee el número de serie:")
    label.config(font=('ARIAL', '30'), fg='blue')
    global product
    product = tk.StringVar()
    textBox = tk.Entry(root, textvariable=product, width=20)
    textBox.config(font=('Arial', 30), bd=4)
    actualModel = hostDB.getModelFromDB()
    modelLabel = tk.Label(root, text="Modelo actual: "+str(actualModel))
    modelLabel.config(font=('ARIAL', 20), fg='green')
    changeModelBtn = tk.Button(root, text="Cambiar de modelo", command=passwordWindow)
    changeModelBtn.config(font=('ARIAL',10),fg='black', relief="groove")

    def enterEvent(event):
        global workOrder
        workOrder = tk.StringVar()
        workOrder.set(product.get())
        root.destroy()

    def endProgram():
        exit()

    root.bind('<Return>', enterEvent)
    label.pack()
    textBox.pack()
    if AtsModel():
        modelLabel.pack()
        emptyLabel = tk.Label(root, text=" ").pack()
        changeModelBtn.pack()
        root.geometry("600x200")
    textBox.focus()
    root.protocol("WM_DELETE_WINDOW", endProgram)
    root.mainloop()

def changeModel():
    #CREATING MAIN WINDOW
    comboValues = modelsDB.getModelsList()
    modelWindow = tk.Tk()
    modelWindow.geometry("400x150")
    ## CREATING LABEL AND COMBOBOX
    modelWindow.title("ATS Bot - Cambio de modelo")
    label = tk.Label(modelWindow, text="Seleccione el modelo:")
    label.config(font=('ARIAL', '15', "bold"), fg='blue')
    combobox = ttk.Combobox(modelWindow, values=comboValues, state="readonly",font=("Helvetica",15))

    def saveChangesFunction():
        model = combobox.get()
        print("File to be saved: "+model)
        hostDB.writeModelInDB(model)
        print("Driver model saved")
        modelWindow.destroy()
        root.destroy()
        time.sleep(1)
        scanProduct()



    ## CREATING BUTTON
    saveChanges = tk.Button(modelWindow, text="Guardar Cambios", command=saveChangesFunction)
    saveChanges.config(font=('ARIAL',11, "bold"), relief='raised', fg="green", borderwidth="3")
    emptyLabel = tk.Label(modelWindow, text=" ")
    label.pack()
    combobox.pack()
    emptyLabel.pack()
    saveChanges.pack()
    modelWindow.mainloop()

    #textBox.config(font=('Arial', 30), bd=4)


def mes():
    ##OPEN MES
    showDesktop()
    findAndClick(mesIconPic, 5, 0.9, True)
    findAndClick(mesLoginBtnPic, 10, 0.9, False)
    findAndClick(mesSideMenuBtnPic,10, 0.9,False)
    findAndClick(startWorkingSideMenuPic,10, 0.9,False)
    time.sleep(0.2)
    pag.press('tab')
    ## PASTE AND ENTER WO
    pag.write(workOrder.get())
    pag.press('enter')
    findAndClick(blueOKbtnPic,4, 0.9,False)
    time.sleep(0.2)
    pag.press('enter')

    #DEFINE GLOBAL VARIABLE TO STORE MODEL
    global model
    if AtsModel() is False:
        ##LOOK FOR PROCESS SCAN SEARCH
        findAndClick(processScanSearchPic, 5, 0.9, False)
        findAndClick(processScanSearchTextBoxPic, 5, 0.9, False)
        time.sleep(0.2)

        ##ENTER WO IN PROCESS SCAN SEARCH
        pag.write(workOrder.get())
        findAndClick(mesSearchBtnPic, 5, 0.9, False)
        time.sleep(0.5)
        pag.press('tab', presses=5)
        time.sleep(0.2)
        pag.keyDown('ctrlleft')
        pag.press('c')
        pag.keyUp('ctrlleft')

        ##SET MODEL INTO VARIABLE
        model = pyperclip.paste()
        model = eval(model.replace('-',''))
    else:
        if hostDB.getModelFromDB() is not None:
            model = hostDB.getModelFromDB()
            model = eval(model.replace('-', ''))
        else:
            pag.alert('Ocurrio un error, solicite la presencia del tecnico de pruebas\n\n'
                      'Error: Model not found in DB')
            exit()

    #SHOW DESKTOP
    time.sleep(0.2)
    showDesktop()


def ats():
    # Open ATS
    findAndClick(atsShortcutPic,10, 0.90, True)
    time.sleep(0.2)

    #findAndClick(runBtnPic, 5, 0.9, False)
    findAndClick(settingsBtnPic, 45, 0.9, False)
    if findAndBool(barcodeLabelPic, 10, 0.9):
        time.sleep(1)
        pag.press('tab', presses=2, interval=0.1)
        pag.press('enter')
    findAndClick(botTestFilesPic, 5, 0.95, True)
    findAndClick(ATS1FolderPic if AtsModel() else ATS2FolderPic, 5, 0.97, True)

    # FIRST TIME OPENING FILE
    while pag.locateCenterOnScreen(modelAtsFile, confidence=0.98) is None:
        print('Encontré el archivo')
        pag.scroll(-300)
    # LOAD FILE
    pag.doubleClick(pag.locateCenterOnScreen(modelAtsFile, confidence=0.98))
    time.sleep(0.3)
    while pag.locateCenterOnScreen(atsOpenBtnPic, confidence=0.95) is None:
        pag.scroll(-300)
    time.sleep(0.5)
    pag.click(pag.locateCenterOnScreen(atsOpenBtnPic))
    findAndClick(botTestFilesPic, 5, 0.95, True)
    findAndClick(ATS1FolderPic if AtsModel() else ATS2FolderPic, 5, 0.97, True)


    # SECOND TIME OPENING FILE
    while pag.locateCenterOnScreen(modelAtsFile, confidence=0.98) is None:
        pag.scroll(-300)
    pag.doubleClick(pag.locateCenterOnScreen(modelAtsFile, confidence=0.98))
    time.sleep(0.3)
    # FINISHED LOADING FILE

    # NEXT COMES CUSTOM MODEL SETTINGS
    print('before custom model settings')
    setSettings(model.writeCurrent, model.dwSwitch)
    print('after custom model settings')

    ### VALIDATE EVERYTHINGS OK
    if findAndBool(inventronicsLogoPic, 5, 0.95):
      pag.alert('¡Configuración Exitosa! Puede comenza a probar.')





killTasks()
scanProduct()
mes()
print(model)
print(model.get_data)
modelAtsFile = model.ssAts1 if AtsModel() else model.ssAts2
print(modelAtsFile)
print(model)
ats()

















