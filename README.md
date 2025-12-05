# Projeto de Simulação ESP32 + Django

Este projeto contém a simulação realizada com ESP32 e uma interface backend em Django.

## Estrutura do Projeto

- `docs/` – PDFs do trabalho e relatórios.  
- `esp32/` – Código-fonte do ESP32.  
- `manage.py` e demais arquivos do Django – Backend do projeto.

## Pré-requisitos

Para rodar o projeto, é necessário ter instalado:

- Python 3.10
- Django  
- Django REST Framework (DRF)  

## Como rodar

1. Instale as dependências:
```bash
   pip install django djangorestframework
```
Aplique as migrations:

```bash
python manage.py migrate
```

Inicie o servidor:
```bash
python manage.py runserver
```

Pronto! O backend estará rodando e pronto para interação com o ESP32.
