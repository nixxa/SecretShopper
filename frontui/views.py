"""
Routes and views for the flask application.
"""
# pylint: disable=line-too-long

from datetime import datetime
from flask import render_template
from flask.ext.mobility.decorators import mobile_template
from flask.ext.mobility import Mobility
from frontui import app


Mobility(app)

@app.route('/')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/qlist')
@app.route('/qlist/')
@mobile_template('{mobile/}questionnaire.html')
def questionnaire(template):
    """Renders questionnaire page"""
    questions = dict()
    # page 1
    questions['page1'] = [
        {'label': 'Стелла без повреждений, чистая, указаны все цены, светятся все элементы (в темное время суток)', 'field_name': 'p1_r1'},
        {'label': 'Газон и дорожное покрытие (включая бордюрный камень) очищены от мусора, грязи, (снега и льда зимой)', 'field_name': 'p1_r2'},
        {'label': 'Все фонари общего освещения горят (в темное время суток)', 'field_name': 'p1_r3'},
        {'label': 'Заправочные островки и топливораздаточные колонки (ТРК) чистые, без повреждений', 'field_name': 'p1_r4'},
        {'label': 'У ТРК нет видимых не обработанных разливов топлива', 'field_name': 'p1_r5'}]
    # page 2
    questions['page2'] = [
        {'label': 'Оператор АЗС одет в полную униформу, выглядит опрятно и чисто', 'field_name': 'p2_r1'},
        {'label': 'Имеется табличка с указанием имени, фамилии, должности (бейдж)', 'field_name': 'p2_r2'},
        {'label': 'Оператор АЗС НЕ жует жвачку, НЕ принимает пищу, НЕ разговаривает по телефону', 'field_name': 'p2_r3'},
        {'label': 'Оператор поприветствовал Вас доброжелательно и вежливо', 'field_name': 'p2_r4'},
        {'label': 'Оператор уточнил вид топлива', 'field_name': 'p2_r5'},
        {'label': 'Оператор повторил вслух вид топлива и сообщил номер ТРК', 'field_name': 'p2_r6'},
        {'label': 'Оператор НЕ положил крышку бензобака на автомобиль', 'field_name': 'p2_r7'},
        {'label': 'Оператор НЕ пролил бензин на а/м', 'field_name': 'p2_r8'},
        {'label': 'Оператор своевременно вынул пистолет из бака после заправки', 'field_name': 'p2_r9'},
        {'label': 'Оператор поблагодарил и пригласил приехать снова', 'field_name': 'p2_r10'}]
    # page 3
    questions['page3'] = [
        {'label': 'Стекла окон фасада и двери без повреждений, чистые', 'field_name': 'p3_r1'},
        {'label': 'Отсутствуют объявления/информация, написанные от руки', 'field_name': 'p3_r2'},
        {'label': 'Территория вокруг здания  чистая, без мусора (снега и льда зимой), урна для мусора заполнена не более чем на 2/3', 'field_name': 'p3_r3'},
        {'label': 'Пол чистый, мусора нет (в здании магазина)', 'field_name': 'p3_r4'},
        {'label': 'Полки без повреждений, чистые, заполнены товаром, все товары с ценниками, нет просроченного товара', 'field_name': 'p3_r5'},
        {'label': 'Столы в кафе чистые, стулья аккуратно выровненные', 'field_name': 'p3_r6'},
        {'label': 'На витрине представлено не менее 15 готовых пончиков - при наличии кафе', 'field_name': 'p3_r7'},
        {'label': 'Нет "шубы" в морозильных ларях', 'field_name': 'p3_r8'},
        {'label': 'Двери в подсобные помещения закрыты', 'field_name': 'p3_r9'},
        {'label': 'Телевизор работает на новостном канале без звука/с минимальным звуком', 'field_name': 'p3_r10'},
        {'label': 'В торговом зале хорошо слышна запись музыки и рекламных объявлений', 'field_name': 'p3_r11'}]
    # page 4
    questions['page4'] = [
        {'label': 'Туалет: пол, стены - чистые, сантехника чистая, без видимых повреждений', 'field_name': 'p4_r1'},
        {'label': 'Туалет: туалетная бумага, крючки для одежды и объявление "Не бросать в унитаз" в наличии', 'field_name': 'p4_r2'},
        {'label': 'Туалет: соблюдается график уборки туалета', 'field_name': 'p4_r3'},
        {'label': 'Туалет: мыльный раствор в диспенсере в наличии', 'field_name': 'pr_r4'}
    ]
    # page 5
    questions['page5'] = [
        {'label': 'Кассир: Одет в полную униформу, выглядит опрятно и презентабельно, пирсинг и яркие украшения отсутствуют', 'field_name': 'p5_r1'},
        {'label': 'Кассир: Имеется табличка с указанием имени, фамилии, должности (бейдж)', 'field_name': 'p5_r2'},
        {'label': 'Кассир: Оператор-кассир на кассе кафе одет в фартук и козырек', 'field_name': 'p5_r3'},
        {'label': 'Кассир: Чистые руки/ногти, отсутствие колец (исключение обручальное)', 'field_name': 'p5_r4'},
        {'label': 'Кассир: Длинные волосы собраны (у женщин), сотрудник чисто выбрит/усы, борода аккуратно подстрижены (у мужчин)', 'field_name': 'p5_r5'},
        {'label': 'Кассир: НЕ жует жвачку, НЕ принимает пищу, НЕ разговаривает по телефону', 'field_name': 'p5_r6'}
    ]
    # page 6
    questions['page6'] = [
        {'label': 'Кассир: Установил зрительный контакт, улыбнулся доброжелательно и вежливо', 'field_name': 'p6_r1'},
        {'label': 'Кассир: Поприветствовал клиента', 'field_name': 'p6_r2'},
        {'label': 'Кассир: Выяснил потребность клиента', 'field_name': 'p6_r3'},
        {'label': 'Кассир: Предложил приобрести большее кол-во топлива (торговля с плюсом)', 'field_name': 'p6_r4'},
        {'label': 'Кассир: Грамотно презентовал ассортимент кафе - при наличии кафе', 'field_name': 'p6_r5'},
        {'label': 'Кассир: Предложил приобрести дополнительное блюдо из ассортимента кафе', 'field_name': 'p6_r6'},
        {'label': 'Кассир: Уточнил наличие/ предложил приобрести карту "Астра"', 'field_name': 'p6_r7'},
        {'label': 'Кассир: Повторил вслух заказ клиента, получил обратную связь, озвучил сумму заказа', 'field_name': 'p6_r8'},
        {'label': 'Кассир: Проговорил вслух сумму, полученную от клиента', 'field_name': 'p6_r9'},
        {'label': 'Кассир: Выдал номер заказа', 'field_name': 'p6_r10'},
        {'label': 'Кассир: Правильно произвел расчет на ККМ ("пробил" весь заказ, ввел сумму полученную от клиента)', 'field_name': 'p6_r11'},
        {'label': 'Кассир: Выдал чек, проговорил вслух и выдал сумму сдачи (при заправке по пластиковым картам - 2 чека)', 'field_name': 'p6_r12'},
        {'label': 'Кассир: Быстро и правильно собрал заказ (выпечка, напитки и т.д.) - при наличии кафе', 'field_name': 'p6_r13'},
        {'label': 'Кассир: Поблагодарил и пригласил приехать снова', 'field_name': 'p6_r14'}
    ]
    return render_template(
        template,
        questions=questions,
        title='Контрольный лист посещения'
    )
