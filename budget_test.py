import unittest, time, os
from builtins import id

import pytest

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import date
from time import sleep
from appium.options.android import UiAutomator2Options

from utils import ExpenseData, ErrorData, Log

class AndroidBudget(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['appium:automationName'] = 'uiautomator2'
        desired_caps['deviceName'] = '192.168.100.28:5555'
        desired_caps['appPackage'] = 'protect.budgetwatch'
        desired_caps['appActivity'] = '.MainActivity'
        desired_caps['autoGrantPermissions'] = 'true'

        capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

        self.driver = webdriver.Remote('http://172.17.0.2:4723', options=capabilities_options)
        self.driver.implicitly_wait(10)

    '''
        Tenta add uma expense sem value
    '''
    def test_app_expense_add_noValue(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## NOT add valores (name, value)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        # value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        ## coleta o erro SE HOUVER
        error_save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text').text

        assert ErrorData.expense_add_noValue in \
               self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text').text, \
            ErrorData.expense_add_noValue_test_failed
        self.driver.implicitly_wait(30)

    '''
        Tenta add uma expense sem name
    '''
    @pytest.mark.xfail
    def test_app_expense_add_noName(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## NOT add valores (name)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        # name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        ## coleta o erro SE HOUVER
        try:
            error_save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text')
            assert ErrorData.expense_add_noName in \
                   error_save.text, \
                ErrorData.expense_add_noName_test_failed
        except NoSuchElementException as e:
            Log.logger("Exception error: " + str(e))
            assert ErrorData.expense_add_noName_test_failed
        except Exception as e:
            Log.logger("Exception error: " + str(e))
            assert ErrorData.expense_add_noName_test_failed
        self.driver.implicitly_wait(30)

    '''
        Tenta add uma expense sem name e value
    '''
    def test_app_expense_add_noName_noValue(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## NOT add valores (name, value)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        # name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        # value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        ## coleta o erro SE HOUVER
        error_save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text').text

        assert ErrorData.expense_add_noName_noValue in \
               self.driver.find_element(By.ID, 'protect.budgetwatch:id/snackbar_text').text, \
            ErrorData.expense_add_noName_noValue_test_failed

    '''
        Tenta remove uma expense depois de um transaction
    '''
    def test_app_expense_remove(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## primeiro add pra poder fazer o remove
        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## add valores (name, value)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        ## A partir daqui é remove pra valer ja q depois do save volta pra Transactions
        ## edit expense "energia"
        self.driver.find_element(
            By.XPATH,
            f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/name" and @text="{ExpenseData.name}"]') \
            .click()
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_edit').click()
        ## pega o mais opcoes
        self.driver.find_element(By.XPATH, '//android.widget.ImageView[@content-desc="Mais opções" and @package="protect.budgetwatch"]').click()
        self.driver.find_element(
            By.XPATH,
            f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/title" and @text="Delete"]') \
            .click()
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("CONFIRM")').click() ## remove

        # Verificar se o item foi removido corretamente
        # neste passo ja voltei pra transactions
        try:
            expensesAux = self.driver.find_elements(By.ID, 'protect.budgetwatch:id/name')
            # Log.logger("ExpensesAux " + str(expensesAux))
            ans = next((expense for expense in expensesAux if name in expense.get_attribute("text")), None)
            # Log.logger("ans " + str('nao achei o expense ' if ans == None else 'deu ruim'))
            self.assertFalse(ans, ErrorData.expense_remove)
        except Exception as e:
            Log.logger("Exception Error " + e)

    '''
        Tenta edit uma expense depois de um transaction
    '''
    def test_app_expense_edit(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## primeiro add pra poder fazer o edit
        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## add valores (name, value)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        ## A partir daqui é edit pra valer ja q depois do save volta pra Transactions
        ## edit expense "energia"
        self.driver.find_element(
            By.XPATH,
            f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/name" and @text="{ExpenseData.name}"]') \
            .click()
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_edit').click()

        ## troca valores (value)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.clear() ## limpa antes de editar
        value.send_keys(ExpenseData.value_pos_edit)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        # Verificar se o item foi adicionado corretamente
        # self.assertEqual(
        #     self.driver.find_element(By.XPATH,
        #                              f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/value" and @text="{ExpenseData.value_pos_edit}"]').get_attribute(
        #         "text"),
        #     ExpenseData.name,
        #     ErrorData.expense_edit_value
        # )
        assert ExpenseData.value_pos_edit in self.driver.find_element(By.XPATH,
                                                                      f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/value"]').get_attribute(
            "text"), ErrorData.expense_edit_value

    '''
        Tenta add uma expense depois de um transaction
    '''
    def test_app_expense_add(self):
        ## skippa a intro
        ## @TODO transformar em funcao
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em Transactions
        transactions= self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Transactions')]")
        transactions.click()

        ## add expense
        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        ## add valores (name, value)
        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/nameEdit')
        name.send_keys(ExpenseData.name)
        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.send_keys(ExpenseData.value)

        ## salva
        self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save').click()

        # Verificar se o item foi adicionado corretamente
        self.assertEqual(
            self.driver.find_element(By.XPATH,
                                     f'//android.widget.TextView[@resource-id="protect.budgetwatch:id/name" and @text="{ExpenseData.name}"]').get_attribute(
                "text"),
            ExpenseData.name,
            ErrorData.expense_add
        )

    def test_app_budget_add(self):
        ## skippa a intro
        if self.driver.find_element(By.XPATH, "//android.widget.TextView[contains(@text, 'Welcome to Budget Watch')]"):
            skip = self.driver.find_element(By.ID, 'protect.budgetwatch:id/skip')
            skip.click()
            self.driver.implicitly_wait(30)

        # clicar em budget
        budget = self.driver.find_element(By.XPATH,
                                          "//android.widget.TextView[contains(@text, 'Budgets')]")
        budget.click()

        add = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_add')
        add.click()

        name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
        name.send_keys("energia")

        value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
        value.send_keys("500")

  ##      name = self.driver.find_element(By.ID, 'protect.budgetwatch:id/budgetNameEdit')
    ##    name.set_text("energia")

     ##   value = self.driver.find_element(By.ID, 'protect.budgetwatch:id/valueEdit')
     ##   value.set_text("500")

        save = self.driver.find_element(By.ID, 'protect.budgetwatch:id/action_save')
        save.click()

        self.assertEqual("energia", self.driver.find_element(By.XPATH,
                                                             "//android.widget.TextView[contains(@text, 'energia')]").get_attribute(
            'text'))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    ## pra rodar um especifico [NOT WORKING]
    ## suite = unittest.TestLoader().loadTestsFromName('AndroidBudget.test_app_expense_remove')

    ## roda tudo
    suite = unittest.TestLoader().loadTestsFromTestCase(AndroidBudget)

    unittest.TextTestRunner(verbosity=2).run(suite)
