Comando para instalação dos pacotes:

pip install -r requirements.txt 

Verificação Estática de Código (pylint e mypy): Para testar todos:

pylint *

# Para testar cada arquivo:
pylint <nome_do_arquivo.py> util

# Para testar um ou mais arquivos
mypy --show-error-codes --check-untyped-defs <nome_do_arquivo.py>  <nome_da_pasta>

# Testes com relatório de cobertura para o sonar (coverage.xml).
pytest tests/ -vv --cov=src --cov-report=xml

# Testes com relatório de cobertura exibido no console.
pytest tests/ -vv --cov=src