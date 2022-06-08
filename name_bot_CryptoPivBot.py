


def start_prog (user_id,namebot,message_in,status,message_id,name_file_picture,telefon_nome):
    import time
    import iz_func
    import iz_telegram

    if  message_in.find ('/start') != -1:    	
        iz_func.save_variable (user_id,"status","",namebot)
        iz_telegram.language (namebot,user_id)
        status = ''


    if message_in == 'Вывести прибыль':
        summ = int(iz_telegram.load_variable (user_id,namebot,'Баланс робота рубли'))
        if summ > 0:
            message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Вывести прибыль4','S',0)
        else:    
            message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Вывести прибыль2','S',0)



    if message_in == 'Пополнить торговый баланс':
        iz_func.save_variable (user_id,"status","Пополнить торговый баланс",namebot)

    if  status == 'Пополнить торговый баланс': 
        print ('[+] message_in',message_in)
        summ = 0
        try:
            summ = int (message_in)
            iz_func.save_variable (user_id,namebot,"Сумма к пополнения",str(summ))
            if summ < 1000:
                message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Недостаточно средств','S',0)
            else:    
                message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Сумма к пополнений','S',0) 
        except Exception as e:
            print ('[e]',e)
            message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'Введите правельно сумму','S',0) 
        iz_func.save_variable (user_id,"status","",namebot)

    if message_in.find ('Отмена') != -1:
        iz_func.save_variable (user_id,"status","",namebot)
        status = ''
        message_out,menu,answer  = iz_telegram.send_message (user_id,namebot,'ОтменаЗапуск','S',0)
        label = 'no send'
