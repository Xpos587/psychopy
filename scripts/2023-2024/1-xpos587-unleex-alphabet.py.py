import random
from threading import Thread
from typing import Optional

import pandas as pd
from psychopy import core, event, visual
from serial import Serial
from serial.tools import list_ports

port = "COM3"
for i in list(list_ports.comports()):
    if i.description.find("Arduino Mega 2560") != -1:
        port = i.device
        break
ser = Serial(port, 9600)
ser.timeout = 0

win = visual.Window([800, 600], units="norm")

phrase = "АБВГДЕ ЁЖЗИЙК ЛМНОПР СТУФХЦ ЧШЩЪЫЬ ЭЮЯ.,_"
target = (2, 2)

str_matrix = [[j for j in i] for i in phrase.split()]
col_order = list(range(len(str_matrix)))
row_order = list(range(len(str_matrix[0])))

gen_order = [[i, 1] for i in col_order]
gen_order.extend([[i, 0] for i in row_order])
random.shuffle(gen_order)

trgt_lights_cols = [
    i
    for i in range(len(gen_order))
    if gen_order[i][1] == 1 and gen_order[i][0] == target[0]
]
trgt_lights_rows = [
    i
    for i in range(len(gen_order))
    if gen_order[i][1] == 0 and gen_order[i][0] == target[1]
]
trgt_lights = [[i, 0] for i in trgt_lights_rows]
trgt_lights.extend([[i, 1] for i in trgt_lights_cols])
trgt_lights.sort()
start_pos_x = -len(phrase) * 0.025
matrix = [
    [
        visual.TextStim(
            win,
            text=str_matrix[i][j],
            pos=((start_pos_x + j) * 0.08, (-i * 0.1)),
        )
        for j in range(len(str_matrix[i]))
    ]
    for i in range(len(str_matrix))
]
square = visual.Rect(  # type: ignore
    win,
    width=0.1,
    height=0.1,
    fillColor="black",
    lineColor="black",
    pos=(0.9, -0.9),
)


def redraw():
    for row in matrix:
        for letter in row:
            letter.draw()
    square.draw()
    win.flip()


def change_state(index, axis):  # axis = 0 if rows, 1 if columns
    for i in range(len(matrix)):
        if axis == 0:
            matrix[index][i].color = "red"
        elif axis == 1:
            matrix[i][index].color = "red"
    square.fillColor = "white"
    redraw()
    core.wait(0.75)
    for i in range(len(matrix)):
        if axis == 0:
            matrix[index][i].color = "white"
        elif axis == 1:
            matrix[i][index].color = "white"
    square.fillColor = "black"
    redraw()


def split_list_by_underscore(array):
    result = []  # Итоговый список списков
    for sublist in array:  # Для каждого подсписка в исходном списке
        new_sublist = []  # Новый подсписок для текущего разделения
        current = []  # Текущий собираемый список
        for item in sublist:
            if item == "_":  # Если встретили символ разделителя
                new_sublist.append(
                    current
                )  # Добавляем собранный подсписок в список разделений
                current = []  # Начинаем новый подсписок
            else:
                current.append(item)  # Добавляем элемент в текущий подсписок
        if current:  # Добавляем последний подсписок, если он не пуст
            new_sublist.append(current)
        result.append(
            new_sublist
        )  # Добавляем разделённый подсписок в итоговый список
    return result


target = (2, 2)
collecting_data: Optional[Thread] = None
signals: list[str] = []
trgt_signals = []
non_trgt_signals = []

redraw()
while True:
    print(trgt_lights)
    key = event.waitKeys()
    if key:
        if key[0] == "escape":
            win.close()
            ser.close()
            core.quit()
        if key[0] == "space":
            iterno = 1
            while True:
                print(
                    f"Итерация {iterno}: порядок подсветки столбцов и строк:",
                    gen_order,
                )
                for elem in gen_order:  # elem = [index,axis]
                    print(trgt_lights, elem)
                    change_state(elem[0], elem[1])
                    if event.getKeys(keyList=["escape"]):
                        columns = [
                            "A0",
                            "A1",
                            "A2",
                            "A3",
                            "A4",
                            "A5",
                            "A6",
                            "A7",
                            "Diode",
                        ]
                        iters = [i.split("\r\n") for i in signals]
                        data = split_list_by_underscore(iters)

                        final_df = pd.DataFrame(columns=columns)

                        # Итерация по всем блокам данных
                        for block in data:
                            for sublist in block:
                                if len(sublist) == len(
                                    columns
                                ):  # Убедиться, что в подсписке 9 элементов
                                    temp_df = pd.DataFrame(
                                        [sublist], columns=columns
                                    )
                                    final_df = pd.concat(
                                        [final_df, temp_df], ignore_index=True
                                    )

                        final_df.to_csv("../../data/2023-2024/result.csv", index=False)
                        win.close()
                        ser.close()
                        core.quit()

                    encoded = ser.read(size=ser.in_waiting)
                    decoded = encoded.decode(encoding="utf-8").strip()
                    signals.append(decoded)
                    if elem in trgt_lights:
                        trgt_signals.append(decoded)
                    else:
                        non_trgt_signals.append(decoded)
                    core.wait(0.75)
                iterno += 1
                gen_order = [
                    [i, 1] for i in col_order
                ]  # second element is axis. 0 is row, 1 is column
                gen_order.extend([[i, 0] for i in row_order])
                random.shuffle(gen_order)
                trgt_lights_cols = [
                    i
                    for i in range(len(gen_order))
                    if gen_order[i][1] == 1 and gen_order[i][0] == target[0]
                ]
                trgt_lights_rows = [
                    i
                    for i in range(len(gen_order))
                    if gen_order[i][1] == 0 and gen_order[i][0] == target[1]
                ]
                trgt_lights = [[i, 0] for i in trgt_lights_rows]
                trgt_lights.extend([[i, 1] for i in trgt_lights_cols])
                trgt_lights.sort()
