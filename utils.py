class ExpenseData(object):
    name = "energia"
    value = "150"
    value_pos_edit = "250"
    
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

class Log:
    @staticmethod
    def logger(message: str):
        print('########## [DEBUG] #########', flush=True)
        print(message, flush=True)
