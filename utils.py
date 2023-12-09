from datetime import datetime, timedelta

class ExpenseData(object):
    name = "energia"
    nameBiggerThan20Chars = "energia energia energia energia"
    nameSmallerThan2Chars = "a"
    value = "150"
    value_wrong = "150.00abcdefzksa"
    value_pos_edit = "250"
    note_wrong = "nota super longa meu Deus como ela eh longa longa longa"
    date_wrong2 = "29 de dez. de 2023"
    date_correct = "29 de nov. de 2023"
    date_wrong3 = "doawjdoiadoipandoanda 102018 121"
    def __init__(self, driver):
        self.driver = driver
        self.date_wrong = datetime.strptime(self.driver.get_device_time("DD/MM/YYYY"), "%d/%m/%Y") + timedelta(weeks=1)

   
class ErrorData(object):
    expense_add = "Erro ao add expense!"
    expense_edit_value = "Erro ao edit expense!"
    expense_remove = "Erro ao remove expense!"
    expense_add_noName_noValue = "Name and Value are empty"
    expense_add_noName_noValue_test_failed = "Falha no teste de Name and Value are empty on adding expense"
    expense_add_noName = "Name is empty"
    expense_add_noName_test_failed = "Falha no teste de Name is empty on adding expense"
    expense_add_noValue = "Value is empty"
    expense_add_noValue_test_failed = "Falha no teste de Value is empty on adding expense"
    expense_add_name_limit_range = "Falha no teste de tamanho de name fora dos limites de tamanho"
    expense_add_value_invalid_chars= "Falha no teste de caracteres de value"
    expense_add_value_invalid= "Value invalid"
    expense_add_note_invalid= "Note invalid"
    expense_add_note_invalid_chars= "Falha no teste de caracteres de value"
    expense_add_data_invalid= "Date invalid"
    expense_add_date_invalid_msg= "Falha no teste de Data futura"

class Log:
    @staticmethod
    def logger(message: str):
        print('########## [DEBUG] #########', flush=True)
        print(message, flush=True)
