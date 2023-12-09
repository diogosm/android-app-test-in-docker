FROM python:3.8

WORKDIR /app
ADD . /app

# Install any needed packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

## add -s to use print and debugs
#CMD ["pytest","-rA", "-k", "test_app_expense_add_noName_noValue", "budget_test.py"]
CMD ["pytest","--pdb", "-v", "budget_test.py"]
