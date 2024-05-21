#Crear una aplicación para memorizar información
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup)
from random import shuffle
from random import randint

class Question():
    "contiene una pregunta, una respuesta correcta y 3 incorrectas"
    def __init__(self,question,rigth_answer,wrong1,wrong2,wrong3):
        self.question=question
        self.rigth_answer=rigth_answer
        self.wrong1=wrong1
        self.wrong2=wrong2
        self.wrong3=wrong3

questions_list = []

q1 = Question('¿El Idioma oficial de Brasil?', 'Portugues', 'Ingles', 'Español', 'Brasilero')
q2 = Question('¿Qué color no aparece en la bandera americana?', 'Verde', 'Rojo', 'Blanco', 'Azul')
q3 = Question('Casa tradicional de pueblo yakurt', 'Yurta', 'Urasa', 'Igloo', 'Khata')
q4 = Question('¿Cuál es la raíz cuadrada de 1964 dividido entre 2?', '22,1585', '44,25,35', '13,1465', 'Ninguna')

questions_list.append(q1)
questions_list.append(q2)
questions_list.append(q3)
questions_list.append(q4)
app = QApplication([])


window = QWidget()
window.setWindowTitle('Tarjeta de memoria')
window.resize(300, 300)

'''Interfaz para la aplicación de Tarjeta de memoria'''
btn_OK = QPushButton('Responder') # botón de responder
lb_Question = QLabel('¿Qué nacionalidad no existe?') # texto de pregunta


RadioGroupBox = QGroupBox("Opciones de respuesta") # grupo en la pantalla para botones de radio con respuestas
rbtn_1 = QRadioButton('Enets')
rbtn_2 = QRadioButton('Chulyms')
rbtn_3 = QRadioButton('Pitufos')
rbtn_4 = QRadioButton('Aleutas')

RadioGroup = QButtonGroup()
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() # los verticales estarán dentro de los horizontales
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) # dos respuestas en la primera columna
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) # dos respuestas en la segunda columna
layout_ans3.addWidget(rbtn_4)


layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3) # las columnas están en la misma línea


RadioGroupBox.setLayout(layout_ans1) # el “panel” con opciones de respuesta está listo 


# Crear un panel de resultados ---Se agregó
AnsGroupBox = QGroupBox('Resultado de prueba')
lb_Result = QLabel('¿Es correcto o no?')
lb_Correct = QLabel('¡Aquí estará la respuesta!')

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

layout_line1 = QHBoxLayout() # pregunta
layout_line2 = QHBoxLayout() # opciones de respuesta o resultados de prueba
layout_line3 = QHBoxLayout() # botón de “Responder”


layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)
RadioGroupBox.show()
AnsGroupBox.hide()


layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # el botón debería ser grande
layout_line3.addStretch(1)


# Ahora vamos a colocar las líneas que hemos creado una debajo de la otra:
layout_card = QVBoxLayout()


layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # los espacios entre el contenido

answers=[rbtn_1,rbtn_2,rbtn_3,rbtn_4]

'''FUNCIONES'''
def show_result():
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Siguiente pregunta')


def show_question():
    AnsGroupBox.hide()
    RadioGroupBox.show()
    btn_OK.setText('Responder')

    RadioGroup.setExclusive(False)
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    
    RadioGroup.setExclusive(True)

def ask(q:Question):
    shuffle(answers)
    answers[0].setText(q.rigth_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question)
    lb_Correct.setText(q.rigth_answer)
    show_question()

def check_answer():
    if answers[0].isChecked():
        window.score += 1
        print('Estadísticas\n - preguntas totales:', window.total, '\n preguntas correctas:', window.score)
        print('Calificación:', (window.score/window.total)*100)
        show_correct('¡Correcto!')
    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('¡Incorrecto!')
            print('Estadísticas\n - preguntas totales:', window.total, '\n preguntas correctas:', window.score)
            print('Calificación:', (window.score/window.total)*100)

def show_correct(res):
    lb_Result.setText(res)
    show_result()

def next_question():
    window.total += 1
    cur_question = randint(0, len(questions_list) - 1)
    q = questions_list[cur_question]
    ask(q)

def click_OK():
    if btn_OK.text() == 'Responder':
        check_answer()
    else:
        next_question()


window.cur_question = -1
window.total = 0
window.score = 0
btn_OK.clicked.connect(click_OK)

next_question()

window.setLayout(layout_card)
window.show()
app.exec()