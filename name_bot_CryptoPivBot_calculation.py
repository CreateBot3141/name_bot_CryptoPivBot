# -*- coding: utf-8 -*-

import iz_func
import time
import iz_telegram
import random

def get_refwral_partber (namebot,user_id):
    sql = "select id,user_id from bot_refer where namebot = '{}';".format(namebot)
    cursor.execute(sql)
    data = cursor.fetchall()
    koll = 0
    for rec in data: 
        koll = koll + 1
    return koll    

def get_refwral_url (namebot,user_id):
    variable = 't.me/'+str(namebot)+'?start='+str(user_id)
    return variable

def get_summ_invest (namebot,user_id):
    variable = 0
    sql = "select id,result from bot_balans where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and currency = 'QIWI RUB' and user_id <> ''".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    for rec in data: 
        id,result = rec.values()
        variable = variable + result 
    return variable    

def convert_dollar (summ):
    variable = round (summ / kurs,2)
    return variable

def get_pribol (namebot,user_id,tm,currency):
    koll = 0
    sql = "select id,result from bot_balans where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"' and currency = '"+str(currency)+"' and unixtime > "+str(tm)+";".format()
    cursor.execute(sql)
    data = cursor.fetchall()
    variable = 0
    for rec in data: 
        id,result = rec.values()
        variable = variable + result   
        koll = koll +1
    return variable,koll  

def get_pribol_all_exchange (namebot,user_id,tm):
    summ = 0
    koll = 0
    for obj in list:
        exchange = obj[0]
        procent  = obj[2]
        currency = 'ROBOT RUB ('+exchange+')'
        answer = get_pribol (namebot,user_id,tm,currency)
        summ = summ + answer[0]
        koll = koll + answer[1]
    return summ,koll

def get_referal_all_exchange (namebot,user_id,tm):
    summ = 0
    koll = 0
    for obj in list:
        exchange = obj[0]        
        procent  = obj[2]
        currency = 'REFER RUB ('+exchange+')'
        answer = get_pribol (namebot,user_id,tm,currency)
        summ = summ + answer[0]
        koll = koll + answer[1]
    return summ,koll

################################################## ----------------------------------- #################################################

def get_QIWI_Balans (namebot,user_id):

    variable = get_refwral_partber (namebot,user_id)
    name_variable = 'Число ваших парнёров'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('        [+] ',name_variable,':',variable)

    variable = get_refwral_url (namebot,user_id)
    name_variable = 'Ваша партнёрская ссылка'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('        [+] ',name_variable,':',variable)
    
    variable = get_summ_invest (namebot,user_id)
    name_variable = 'Сумма инвестиций рубли'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    variable_QIWI = variable

    variable = convert_dollar (variable_QIWI)
    name_variable = 'Сумма инвестиций доллар'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('        [+] ',name_variable,':',variable)

    return variable_QIWI

def insert_balans (namebot,user_id,variable_QIWI):
    import time
    summ_morga = (variable_QIWI * pr_morga / 100)*random.random()   ### Итоговая прибыль
    summ = summ_morga * pr_proga / 100                              ### Процент клиенту  
    unixtime = int(time.time())
    # Размазываем процент на все биржи

    for obj in list:
        exchange = obj[0]
        koll     = obj[1]
        procent  = obj[2]
        currency = 'ROBOT RUB ('+exchange+')'
        if koll > 0:
            summ_exchange = (summ * procent / 100) / koll
            for number in range(koll):
                if summ_exchange > 0:
                    sql = "INSERT INTO bot_balans (comment,currency,minus,namebot,plus,result,unixtime,user_id) VALUES ('','"+str(currency)+"',0,'"+namebot+"',"+str(summ_exchange)+","+str(summ_exchange)+","+str(unixtime)+",'"+str(user_id)+"')".format ()
                    cursor.execute(sql)
                    db.commit()
        else:
           pass            

        spon = 0
        user_id_refer = ''    
        sql = "select id,user_id_refer from bot_refer where namebot = '"+str(namebot)+"' and user_id = '"+str(user_id)+"'".format()
        cursor.execute(sql)
        data = cursor.fetchall()
        for rec in data: 
            id,user_id_refer = rec.values()

        if user_id_refer != '':
            spon = summ_exchange * pr_morga / 100 

        if spon > 0 and user_id_refer != '':
            currency = 'REFER RUB ('+exchange+')'
            sql = "INSERT INTO bot_balans (comment,currency,minus,namebot,plus,result,unixtime,user_id) VALUES ('','"+str(currency)+"',0,'"+namebot+"',"+str(spon)+","+str(spon)+","+str(unixtime)+",'"+str(user_id_refer)+"')".format ()
            cursor.execute(sql)
            db.commit()








namebot = '@CryptoPivBot'
kurs = 74.39
pr_morga = 15  ## Моржа за реферада процент
pr_proga = 60  ## Процент который передаем клиенту 
list = [['Binance',3,40],['Coinbase',3,40],['KuCoin',3,20],['Huobi',3,0],['Kraken',3,0],['ОКЕх',3,0],['Poloniex',3,0],['Gemini',3,0]]

print ('[+] Расчет данных телеграмм бота',namebot)
print ('[+] Курс доллора ',kurs)
db,cursor = iz_func.connect ()

sql = "select id,user_id from bot_user where namebot = '{}';".format(namebot)
cursor.execute(sql)
data = cursor.fetchall()
id = 0
for rec in data: 
    id,user_id = rec.values()
    print ('    [+] Расчет для пользователя ситемы:',user_id) 
    variable_QIWI = get_QIWI_Balans (namebot,user_id)
    print ('    [+] Выставление почасовой прибыли')
    insert_balans (namebot,user_id,variable_QIWI)

    ################################################################################################

    list1     = ['Прибыль робота За сегодня рубли','Прибыль робота За сегодня доллар','Прибыль робота За сегодня процент',1]
    list2     = ['Прибыль робота За вчера рубли',  'Прибыль робота За вчера доллар'  ,'Прибыль робота За вчера процент'  ,2]
    list3     = ['Прибыль робота За 7 дней рубли','Прибыль робота За 7 дней доллар','Прибыль робота За 7 дней процент',7]
    list4     = ['Прибыль робота За 30 дней рубли','Прибыль робота За 30 дней доллар','Прибыль робота За 30 дней процент',30]
    list5     = ['Прибыль робота За всё время рубли','Прибыль робота За всё время доллар','Прибыль робота За всё время процент',1000]

    list_all  = [list1,list2,list3,list4,list5]

    for task in list_all:

        name_variable = task[0]
        print ('    [+] ',name_variable)    
        tm = int(time.time()-(24*60*60*task[3]))
        variable = get_pribol_all_exchange (namebot,user_id,tm)[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('        [+]',name_variable,':',variable)
        variable_1 = variable

        name_variable = task[1]
        variable      = convert_dollar (variable_1)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('        [+]',name_variable,':',variable)

        name_variable = task[2]
        if variable_QIWI != 0:
            variable      = round ((variable_1 *100 / variable_QIWI),2)
        else:
            variable      = 0
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('        [+]',name_variable,':',variable)

    list1     = ['Итоговая прибыль За сегодня рубли','Итоговая прибыль За сегодня доллар','Итоговая прибыль За сегодня процент',1]
    list2     = ['Итоговая прибыль За вчера рубли',  'Итоговая прибыль За вчера доллар'  ,'Итоговая прибыль За вчера процент'  ,2]
    list3     = ['Итоговая прибыль За 7 дней рубли','Итоговая прибыль За 7 дней доллар','Итоговая прибыль За 7 дней процент',7]
    list4     = ['Итоговая прибыль За 30 дней рубли','Итоговая прибыль За 30 дней доллар','Итоговая прибыль За 30 дней процент',30]
    list5     = ['Итоговая прибыль За всё время рубли','Итоговая прибыль За всё время доллар','Итоговая прибыль За всё время процент',1000]

    list_all  = [list1]

    for task in list_all:
        name_variable = task[0]
        print ('    [+] ',name_variable) 
        tm = int(time.time()-(24*60*60*task[3]))
        variable = get_referal_all_exchange (namebot,user_id,tm)[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable)) 
        print ('        [+]',name_variable,':',variable)
        variable_summ_itog = variable
        variable_1         = variable 
        name_variable = task[1]
        variable      = convert_dollar (variable_1)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('        [+]',name_variable,':',variable)
        name_variable = task[2]
        if variable_QIWI != 0:
            variable      = round ((variable_1 *100 / variable_QIWI),2)
        else:
            variable      = 0
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Данные были обновлены'
    variable      = str(int(time.time()))
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)    

    name_variable = 'Баланс робота рубли'
    variable      = variable_QIWI + variable_summ_itog
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)    

    name_variable = 'Баланс робота доллар'
    variable      = round (variable / kurs)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)    

    name_variable = 'Ваш ID инвестора'
    variable      = str(user_id)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)    

print ('    [+] Расчет прибыли партнеров')    
sql = "select id,user_id from bot_user where namebot = '{}';".format(namebot)
cursor.execute(sql)
data = cursor.fetchall()
id = 0
for rec in data: 
    id,user_id = rec.values()

    variable_parner_01  = 0
    variable_parner_02  = 0
    variable_parner_07  = 0
    variable_parner_30  = 0
    variable_parner_00  = 0
    variable_QIWI_01    = 0

    sql = "select id,user_id_refer from bot_refer where namebot = '{}' and user_id_refer = '"+str(user_id)+"';".format(namebot)
    cursor.execute(sql)
    data_refer = cursor.fetchall()
    for rec_refer in data_refer: 
        id_refer,user_id_refer = rec2.values()
        print ('        [+] Новый реферал:',user_id_refer) 

        ls_01 = iz_telegram.load_variable (user_id_refer,namebot,'Прибыль робота За сегодня рубли')
        if ls_01 != '':
            variable_parner_01  = variable_parner_01 + float(ls_01)

        ls_02 = iz_telegram.load_variable (user_id_refer,namebot,'Прибыль робота За вчера рубли')
        if ls_02 != '':
            variable_parner_02  = variable_parner_02 + float(ls_02)

        ls_07 = iz_telegram.load_variable (user_id_refer,namebot,'Прибыль робота За 7 дней рубли')
        if ls_07 != '':
            variable_parner_07  = user_id_refer + float(ls_07)

        ls_30 = iz_telegram.load_variable (user_id_refer,namebot,'Прибыль робота За 30 дней рубли')
        if ls_30 != '':
            variable_parner_30  = variable_parner_30 + float(ls_30)

        ls_00 = iz_telegram.load_variable (user_id_refer,namebot,'Прибыль робота За всё время рубли')
        if ls_00 != '':
            variable_parner_00  = variable_parner_00 + float(ls_00)


        ls__QIWI_01 = iz_telegram.load_variable (user_id_refer,namebot,'Сумма инвестиций рубли')
        if ls__QIWI_01 != '':
            variable_QIWI_01 = variable_QIWI_01 + float(ls__QIWI_01)


    name_variable = 'Прибыль партнера За сегодня рубли'       
    variable = variable_parner_01
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)  

    name_variable = 'Прибыль партнера За сегодня доллар'
    variable      = convert_dollar (variable_parner_01)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)  

    name_variable = 'Прибыль партнера За сегодня процент'
    if variable_QIWI_01 != '' and variable_QIWI_01 != 0:
        variable = round ((variable_parner_01 * 100 / variable_QIWI_01),2)
    else:    
        variable = 0        
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)  

    name_variable = 'Прибыль партнера За вчера рубли'  
    variable = variable_parner_02  
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)  

    name_variable = 'Прибыль партнера За вчера доллар'
    variable      = convert_dollar (variable_parner_02)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('    [+] ',name_variable,variable)  

    name_variable = 'Прибыль партнера За вчера процент'
    if variable_QIWI_01 != '' and variable_QIWI_01 != 0 :    
        variable = round ((variable_parner_02 * 100 / variable_QIWI_01),2)
    else:
        variable = 0
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 7 дней рубли'
    variable = variable_parner_07
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 7 дней доллар'
    variable      = convert_dollar (variable_parner_07)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 7 дней процент'
    if variable_QIWI_01 != '' and variable_QIWI_01 != 0:       
        variable = round ((variable_parner_07 * 100 / variable_QIWI_01),2)
    else:    
        variable = 0
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 30 дней рубли'       
    variable = variable_parner_30
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 30 дней доллар'      
    variable      = convert_dollar (variable_parner_30)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За 30 дней процент'
    if variable_QIWI_01 != '' and variable_QIWI_01 != 0:            
        variable = round ((variable_parner_30 * 100 / variable_QIWI_01),2)
    else:    
        variable = 0
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За всё время рубли'     
    variable = variable_parner_00
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За всё время доллар'
    variable      = convert_dollar (variable_parner_00)
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Прибыль партнера За всё время процент'
    if variable_QIWI_01 != '' and variable_QIWI_01 != 0:                
        variable = round ((variable_parner_00 * 100 / variable_QIWI_01),2)
    else:
        variable = 0
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))


print ('    [+] Расчет арбитража')    

sql = "select id,user_id from bot_user where namebot = '{}';".format(namebot)
cursor.execute(sql)
data = cursor.fetchall()
id = 0
for rec in data: 
    id,user_id = rec.values()

    name_variable = 'Арбитражных цепочек за сегодня'
    tm = 60*60*24
    variable = get_pribol_all_exchange (namebot,user_id,tm)[1]
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('[+] ',name_variable,variable)

    name_variable = 'Торговых сделок за сегодня'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Арбитражных цепочек за вчера'
    tm = 60*60*24*2
    variable = get_pribol_all_exchange (namebot,user_id,tm)[1]
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('[+] ',name_variable,variable)

    name_variable = 'Торговых сделок за вчера'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Арбитражных цепочек за 7 дней'
    tm = 60*60*24*7
    variable = get_pribol_all_exchange (namebot,user_id,tm)[1]
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('[+] ',name_variable,variable)

    name_variable = 'Торговых сделок за 7 дней'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Арбитражных цепочек за 30 дней'
    tm = 60*60*24*30
    variable = get_pribol_all_exchange (namebot,user_id,tm)[1]
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('[+] ',name_variable,variable)

    name_variable = 'Торговых сделок за 30 дней'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

    name_variable = 'Арбитражных цепочек за все время'
    tm = 60*60*24*1000
    variable = get_pribol_all_exchange (namebot,user_id,tm)[1]
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
    print ('[+] ',name_variable,variable)

    name_variable = 'Торговых сделок за все время'
    iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))


print ('    [+] Расчет арбитража по биржам')    

for exchange in list:
    currency = 'ROBOT RUB ('+exchange[0]+')'
    sql = "select id,user_id from bot_user where namebot = '{}';".format(namebot)
    cursor.execute(sql)
    data = cursor.fetchall()
    id = 0
    for rec in data: 
        id,user_id = rec.values()

        tm = 60*60*24        
        answer    = get_pribol (namebot,user_id,tm,currency)

        name_variable = 'Арбитражных цепочек за сегодня ('+exchange[0]+')'
        variable  = answer[1]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Торговых сделок за сегодня ('+exchange[0]+')'
        variable  = answer[1]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за сегодня ('+exchange[0]+')'
        variable  = answer[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за сегодня доллар ('+exchange[0]+')'
        variable      = convert_dollar (variable)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)




        tm = 60*60*24*2
        variable = get_pribol (namebot,user_id,tm,currency)[1]

        name_variable = 'Арбитражных цепочек за вчера ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Торговых сделок за вчера ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))

        name_variable = 'Прибыль робота за вчера ('+exchange[0]+')'
        variable  = answer[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за вчера доллар ('+exchange[0]+')'
        variable      = convert_dollar (variable)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)



        tm = 60*60*24*7
        variable = get_pribol (namebot,user_id,tm,currency)[1]

        name_variable = 'Арбитражных цепочек за 7 дней ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Торговых сделок за 7 дней ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за 7 дней ('+exchange[0]+')'
        variable  = answer[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за 7 дней доллар ('+exchange[0]+')'
        variable      = convert_dollar (variable)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)



        tm = 60*60*24*30
        variable = get_pribol (namebot,user_id,tm,currency)[1]

        name_variable = 'Арбитражных цепочек за 30 дней ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Торговых сделок за 30 дней ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за 30 дней ('+exchange[0]+')'
        variable  = answer[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за 30 дней доллар ('+exchange[0]+')'
        variable      = convert_dollar (variable)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)




        tm = 60*60*24*1000
        variable = get_pribol (namebot,user_id,tm,currency)[1]

        name_variable = 'Арбитражных цепочек за все время ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Торговых сделок за все время ('+exchange[0]+')'
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за все время ('+exchange[0]+')'
        variable  = answer[0]
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)

        name_variable = 'Прибыль робота за все время доллар ('+exchange[0]+')'
        variable      = convert_dollar (variable)
        iz_telegram.save_variable (user_id,namebot,name_variable,str(variable))        
        print ('[+] ',name_variable,variable)


