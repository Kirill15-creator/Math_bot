import telebot
import math

# Определяем функции average и dispersia
def average(x):
     if len(x) == 0:
        return 0
     else:
        return round(sum(x) / len(x), 2)

def dispersia(x):
     if len(x) == 0:
        return 0
     else:
        arr = [(i - average(x)) ** 2 for i in x]
        return round(sum(arr) / len(arr), 2)

bot = telebot.TeleBot("6825134040:AAE4l0aBRprHTZP7SrLI1cjFZSXkPNYboP4")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот который поможет вам с некоторыми математическими задачами. '
                                      'Введите /help, чтобы узнать, как пользоваться.')

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Чтобы решить квадратное уравнение, отправьте /quad\n'
                                      'Чтобы решить биквадратное уравнение, отправьте /biquad\n'
                                      'Для решения уравнения отправьте команду и само уравнение, например: /quad 2x^2 + 5x - 3\n'
                                      'Для расчета среднего арифметического и дисперсии, отправьте /dispersia <числовой массив, через пробел>')

@bot.message_handler(commands=['dispersia'])
def calculate_dispersia(message):
    try:
        # Получаем числовой массив из сообщения
        numbers = message.text.split(" ")[1:]
        numbers = [float(num) for num in numbers]

        # Рассчитываем среднее арифметическое и дисперсию
        avg = average(numbers)
        disp = dispersia(numbers)
        numbers = [str(i) for i in numbers]
        numbers = " ".join(numbers)
        bot.reply_to(message, f"Среднее арифметическое числового массива {numbers} - {avg}\n"
                              f"Дисперсия числового массива {numbers} - {disp}")
    except ValueError:
        bot.reply_to(message, "Некорректный формат числового массива!")
    except IndexError:
        bot.reply_to(message, "Необходимо указать числовой массив после команды /dispersia!")

@bot.message_handler(commands=['quad'])
def solve_quadratic_equation(message):
    try:
        equation = message.text.split(" ", 1)[1].lower().replace(" ","").replace("^2","").replace("+","").split("x")
        a, b, c = map(int, equation)
        D = b**2 - 4*a*c
        if D < 0:
            bot.reply_to(message, "Нет действительных корней!")
        else:
            solution = f"Найдём корень из дискриминанта: √D = √{b}^2 -4 * {a} * {c} = √{D} = {math.sqrt(D)}"
            if D > 0:
                x_1 = (-b + math.sqrt(D)) / (2*a)
                x_2 = (-b - math.sqrt(D)) / (2*a)
                solution += f"\nНайдем корни:\n" \
                            f"x_1 = {-b} + {math.sqrt(D)} / {a*2} = {x_1}\n" \
                            f"x_2 = {-b} - {math.sqrt(D)} / {a*2} = {x_2}\n" \
                            f"Первый корень {round(x_1,2)}, второй корень {round(x_2,2)}"
            elif D == 0:
                x = -b / (2*a)
                solution += f"\nНайдем корень:\n" \
                            f"x = {-b} / {a * 2} = {x}\n" \
                            f"Один корень т.к дискриминант равен 0. Корень равен {round(x,2)}"
            bot.reply_to(message,solution)
    except IndexError:
        bot.reply_to(message, "Необходимо указать уравнение после команды /quad!")
    except ValueError:
        bot.reply_to(message, "Некорректный формат уравнения!")

@bot.message_handler(commands=['biquad'])
def solve_biquadratic_equation(message):
    try:
        equation = message.text.split(" ", 1)[1].lower().replace("^4", "").replace("^2", "").replace(" ", "").split("x")
        bot.reply_to(message, "Решим это уравнение путём введения новой переменной:\n"
                              "x^2 = t \n"
                              "x^4 = t^2\n"
                              "Из этого следует ввести ограничение:\n"
                              "t ≥ 0")
        t_square, t, c = map(int, equation)
        D = t ** 2 - 4 * t_square * c
        if D < 0:
            bot.reply_to(message, "Нет действительных корней, т. к. дискриминант меньше нуля!")
        else:
            solution = f"Найдём корень из дискриминанта: √D = √{str(t)}^2 -4 * {str(t_square)} * {str(c)} = √{D} = {math.sqrt(D)}"
            if D > 0:
                t_1 = (-t + math.sqrt(D)) / (2 * t_square)
                t_2 = (-t - math.sqrt(D)) / (2 * t_square)
                solution += f"\nНайдем корни:\n" \
                            f"t_1 = {-t} + {math.sqrt(D)} / {t_square * 2} = {t_1}\n" \
                            f"t_2 = {-t} - {math.sqrt(D)} / {t_square * 2} = {t_2}\n" \
                            f"Первый корень {round(t_1, 2)}, второй корень {round(t_2, 2)}\n"
                if t_1 >= 0 and t_2 >= 0:
                    solution += "Т.к. обо корня подходят нашему условию, следовательно у х будет 4 корня:\n" \
                                f"t = {t_1} = x^2, следовательно х равен:\n" \
                                f"±{round(math.sqrt(t_1), 2)}\n" \
                                f"t = {t_2} = x^2, следовательно х равен:\n" \
                                  f"±{round(math.sqrt(t_2), 2)}"
                elif t_1 < 0 and t_2 >= 0:
                    solution += "Т.к. только один корень  подходит нашему условию, следовательно у х будет 2 корня:\n" \
                                f"t = {t_2} = x^2, следовательно х равен:\n" \
                                f"±{round(math.sqrt(t_2), 2)}"
                elif t_1 >= 0 and t_2 < 0:
                    solution += "Т.к. только один корень  подходит нашему условию, следовательно у х будет 2 корня:\n" \
                                f"t = {t_1} = x^2, следовательно х равен:\n" \
                                f"±{round(math.sqrt(t_1), 2)}"
                elif t_1 < 0 and t_2 < 0:
                    solution += "У уравнения нет корней т.к. обо корня t меньше нуля!"
            bot.reply_to(message, solution)
    except IndexError:
        bot.reply_to(message, "Необходимо указать уравнение после команды /biquad!")
    except ValueError:
        bot.reply_to(message, "Некорректный формат уравнения!")

bot.polling()
