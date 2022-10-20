poetry export -f requirements.txt --output requirements.txt
pip install -r requirements.txt
pip install sphinx
cd docs && make html