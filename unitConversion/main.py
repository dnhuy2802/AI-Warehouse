from tkinter import *
from tkinter import messagebox
import time
import pandas as pd
from pyparsing import col

root = Tk()
root.title("UNIT CONVERTER")


# Function


def convertKmToMiles(km):
    miles = km * 0.6213712
    return miles


def convertCToF(c):
    f = (c * 9 / 5) + 32
    return f


def convertGallonToL(gallon):
    l = gallon / 0.264172
    return l


def convertGmt7to9(data):
    result = data + 2
    if result > 24:
        result -= 24
    return result


def deleteInput(*inputs):
    for input in inputs:
        input.delete(0, END)


def checkInputNumber(input, output, type):
    if type == "gmt7To9":
        timestamp = input.get()
        if len(timestamp) == 8 and timestamp[2] == ':' and timestamp[5] == ':':
            number = checkInputNumber(timestamp[0:2], output, "")
            return number
        else:
            deleteInput(input)
            deleteInput(output)
            return False
    else:
        try:
            if type != "":
                number = float(input.get())
            else:
                # Case get hours for GMT+7
                number = float(input)
            # delete old output
            deleteInput(output)
            return number
        except ValueError:
            deleteInput(input)
            deleteInput(output)
            return False


def convertController(input, output, type: str):

    floatInput = checkInputNumber(input, output, type)
    if floatInput == False:
        output = "Wrong input !!!"
        return output
    else:
        if type == "kmToMiles":
            return convertKmToMiles(floatInput)
        elif type == "cToF":
            return convertCToF(floatInput)
        elif type == "gallonToL":
            return convertGallonToL(floatInput)
        elif type == "gmt7To9":
            timestamp = input.get()
            data = str(int(convertGmt7to9(floatInput))) + timestamp[2:]
            return data
        else:
            output = "No Options !!!"
            return output


def writeToCsv(inputKm, inputMiles, inputC, inputF, inputGallon, inputL, inputGmt7, inputGmt9):

    # dictionary of lists
    data_input = {'Km': [inputKm.get()], 'Km Convert To Miles': [inputMiles.get()],
                  'C': [inputC.get()], 'C Convert To F': [inputF.get()],
                  'Gallon': [inputGallon.get()], 'Gallon Convert To L': [inputL.get()],
                  'Gmt7': [inputGmt7.get()], 'Gmt7 Convert To Gmt9': [inputGmt9.get()]}
    # data_input = [[inputKm.get(), inputMiles.get(), inputC.get(), inputF.get(),
    #               inputGallon.get(), inputL.get(), inputGmt7.get(), inputGmt9.get()]]

    try:
        pd.read_csv('convert_data.csv')
        data_save = pd.DataFrame(data_input)
        data_save.to_csv('convert_data.csv', mode='a',
                         header=False, index=False)
    except FileNotFoundError:
        data_save = pd.DataFrame(data_input)
        data_save.to_csv('convert_data.csv', index=False)

    messagebox.showinfo("Success", "Data saved to csv file")


def exitProgram():
    root.destroy()
    exit()


# Buttons


# Main Label
labelMain = Label(root, text="UNIT CONVERTER",
                  font=("Arial", 30), bg="#cccccc")

# Label column 1
labelInputKm = Label(root, text="Input km :  ")
labelOutputMiles = Label(root, text="Convert: ")
labelInputC = Label(root, text="Input độ C :  ")
labelOutputF = Label(root, text="Convert : ")
labelInputGallon = Label(root, text="Input gallon :  ")
labelOutputL = Label(root, text="Convert: ")
labelInputGmt7 = Label(root, text="Input GMT +7  :  ")
labelOutputGmt9 = Label(root, text="Convert : ")

# Label column 3
labelKm = Label(root, text="KM")
labelMiles = Label(root, text="MILES")
labelC = Label(root, text="C")
labelF = Label(root, text="F")
labelGallon = Label(root, text="GALLON")
labelL = Label(root, text="L")
labelGmt7 = Label(root, text="AM")
labelGmt9 = Label(root, text="AM")

# Label column 5
labelKmToMiles = Label(root, text="Convert km to miles", pady=30)
labelCToF = Label(root, text="Convert C to F", pady=30)
labelGallonToL = Label(root, text="Convert Gallon to L", pady=30)
labelGmt7To9 = Label(root, text="Convert GMT +7 to GMT +9", pady=30)

# Input
inputKm = Entry(root, width=30)
inputMiles = Entry(root, width=30)
inputC = Entry(root, width=30)
inputF = Entry(root, width=30)
inputGallon = Entry(root, width=30)
inputL = Entry(root, width=30)
inputGmt7 = Entry(root, width=30)
inputGmt9 = Entry(root, width=30)

# Button
buttonDelKm = Button(root, text="Delete", padx=20, pady=5,
                     width=7, bg="red", command=lambda: deleteInput(inputKm, inputMiles))
buttonConMiles = Button(root, text="Convert to Miles", padx=20, pady=5,
                        width=7,
                        command=lambda: inputMiles.insert(0, convertController(inputKm, inputMiles, "kmToMiles")))

buttonDelC = Button(root, text="Delete", padx=20, pady=5,
                    width=7, bg="red", command=lambda: deleteInput(inputC, inputF))
buttonConF = Button(root, text="Convert to F", padx=20, pady=5, width=7,
                    command=lambda: inputF.insert(0, convertController(inputC, inputF, "cToF")))

buttonDelGallon = Button(root, text="Delete", padx=20,
                         pady=5, width=7, bg="red", command=lambda: deleteInput(inputGallon, inputL))
buttonConL = Button(root, text="Convert to L", padx=20, pady=5, width=7,
                    command=lambda: inputL.insert(0, convertController(inputGallon, inputL, "gallonToL")))

buttonDelGmt7 = Button(root, text="Delete", padx=20,
                       pady=5, width=7, bg="red", command=lambda: deleteInput(inputGmt7, inputGmt9))
buttonConGmt9 = Button(root, text="Convert to GMT+9", padx=20, pady=5, width=7,
                       command=lambda: inputGmt9.insert(0, convertController(inputGmt7, inputGmt9, "gmt7To9")))

# Display

labelMain.grid(row=0, column=0, columnspan=6)

# column 1
labelInputKm.grid(row=1, column=1, padx=10, pady=10)
labelOutputMiles.grid(row=2, column=1, padx=10, pady=10)
labelInputC.grid(row=3, column=1, padx=10, pady=10)
labelOutputF.grid(row=4, column=1, padx=10, pady=10)
labelInputGallon.grid(row=5, column=1, padx=10, pady=10)
labelOutputL.grid(row=6, column=1, padx=10, pady=10)
labelInputGmt7.grid(row=7, column=1, padx=10, pady=10)
labelOutputGmt9.grid(row=8, column=1, padx=10, pady=10)

# column 2
inputKm.grid(row=1, column=2)
inputMiles.grid(row=2, column=2)
inputC.grid(row=3, column=2)
inputF.grid(row=4, column=2)
inputGallon.grid(row=5, column=2)
inputL.grid(row=6, column=2)
inputGmt7.grid(row=7, column=2)
inputGmt9.grid(row=8, column=2)

# column 3
labelKm.grid(row=1, column=3)
labelMiles.grid(row=2, column=3)
labelC.grid(row=3, column=3)
labelF.grid(row=4, column=3)
labelGallon.grid(row=5, column=3)
labelL.grid(row=6, column=3)
labelGmt7.grid(row=7, column=3)
labelGmt9.grid(row=8, column=3)

# column 4
buttonDelKm.grid(row=1, column=4)
buttonConMiles.grid(row=2, column=4)
buttonDelC.grid(row=3, column=4)
buttonConF.grid(row=4, column=4)
buttonDelGallon.grid(row=5, column=4)
buttonConL.grid(row=6, column=4)
buttonDelGmt7.grid(row=7, column=4)
buttonConGmt9.grid(row=8, column=4)

# column 5
labelKmToMiles.grid(row=1, column=5, rowspan=2, padx=10)
labelCToF.grid(row=3, column=5, rowspan=2, padx=10)
labelGallonToL.grid(row=5, column=5, rowspan=2, padx=10)
labelGmt7To9.grid(row=7, column=5, rowspan=2, padx=10)

# navigation
buttonDelAll = Button(root, text="Delete All", bg="red", padx=5,
                      pady=5, width=10,
                      command=lambda: deleteInput(inputKm, inputMiles, inputC, inputF, inputGallon, inputL, inputGmt7,
                                                  inputGmt9))
buttonDelAll.grid(row=9, column=0, columnspan=2)

buttonSaveFile = Button(root, text="Save File", padx=5, pady=5, width=10,
                        command=lambda: writeToCsv(inputKm, inputMiles, inputC, inputF, inputGallon, inputL, inputGmt7,
                                                   inputGmt9))
buttonSaveFile.grid(row=9, column=2, columnspan=2)

buttonExit = Button(root, text="Exit", padx=5, pady=5,
                    width=10, command=lambda: exitProgram())
buttonExit.grid(row=9, column=4, columnspan=2)

root.mainloop()
