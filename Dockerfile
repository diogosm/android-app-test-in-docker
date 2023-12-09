FROM python:3.8

WORKDIR /app
ADD . /app

# Install any needed packages in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest

COPY code.sh /app/code.sh
RUN chmod +x /app/code.sh

CMD ["/app/code.sh"]

## add -s to use print and debugs
#CMD ["pytest","-rA", "-k", "test_app_expense_add_date_correta", "budget_test.py"]
#CMD ["pytest","--pdb", "-v", "budget_test.py"]

## skip falhas
#CMD ["pytest","--pdb", "-v","--maxfail=99", "budget_test.py"]
