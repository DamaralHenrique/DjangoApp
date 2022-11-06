# Django basic project
## Group 8

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/RicardoHonda"><img src="https://avatars.githubusercontent.com/u/62343088?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Ricardo Tamay Honda <br/> 11803778</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/DamaralHenrique"><img src="https://avatars.githubusercontent.com/u/62445591?v=4" width="100px;" alt=""/><br /><sub><b>Henrique D'Amaral Matheus<br/>11345513</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/Edu-Hiroshi"><img src="https://avatars.githubusercontent.com/u/97803912?s=400&u=14625cf4c91606d4787d983fd2692ee4db47ff4e&v=4" width="100px;" alt=""/><br /><sub><b>Eduardo Hiroshi Ito<br/>11806868</b></sub></a><br /></td>
  </tr>
</table>

## Overview

The project technical description can be found on the `assets/` folder:
- Use cases: [Casos_de_uso.pdf](https://github.com/DamaralHenrique/DjangoApp/blob/main/assets/Casos_de_uso.pdf)

The folder `/assests/images` contains the following diagrams:
- Classes diagrams (class 3);
- DER (class 6);
- Use cases navigation diagram (class 7).

![class_diagram](assets/images/Diagrama_classes.png)

## 🚀 Quick Start

To get this project up and running locally on your computer:
1. Create a virtual environment and activate it using the following commands:
   ```
   python -m venv env
   .\env\bin\Activate.ps1 # or .\env\scripts\Activate.ps1
   ```

2. Then, install the following dependences:
   ```
   pip install django
   
   pip install reportlab

   pip install fpdf2
   ```

3. Assuming you have Python setup, run the following commands:
   ```
   python manage.py runserver
   ```
   
4. If everything went well, the following message will be shown on the terminal: "Starting development server at http://127.0.0.1:8000". You will then be able to open `http://localhost:8000`, and the following message will appear **"PCS3643 - Laboratório de Engenharia de Software I"**

## 🧪 Testing

Creating a database to make tests (repeat these steps after modifying the python files):
1. On the menage.py script folder:
```
python manage.py makemigrations
```

2. To create the database, execute:
```
python manage.py migrate
```

3. The tests are defined in the `flight\test.py` file. To execute them, run:
```
python manage.py test
```

### Login test

Use the following credentials to test the login for each function:

```
{
   id: "operador",
   password: "qwer",
},
{
   id: "funcionario",
   password: "qwer",
},
{
   id: "gerente",
   password: "qwer",
},

```

The visible pages for each function can be found in the "diagrama_casos-de_uso.png" image, which is inside the `assests` folder


## REF
The Django Template used is referenced from Thales Bruno: https://github.com/thalesbruno/django_bootstrap