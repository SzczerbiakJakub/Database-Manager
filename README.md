# db_manager

  Welcome to Database Manager - a software developed for editing data quickly and easily.
Below is a brief introduction to the program's functionality with some graphic examples to
better understand it.

  Database Manager works with PostgreSQL, thus it's fundamental to download and install it
beforehand. To cooperate with the available databases, it uses psycopg2 - a Python library 
responsible for connecting with PostgreSQL databases.

  The GUI of DB Manager's current version is built using PyQt5 5.15.7

  ![home_page](https://github.com/SzczerbiakJakub/Tetris/assets/89864279/a9f0a983-4e02-45fd-8630-83790705531a)


  This main widget appears after turning on the Database Manager program. It stands for a welcome page and
shares basic information about the software's purpose. The login panel can be seen on the left side. It will
be used to connect to the currently existing Postgres databases.

  To continue, enter the data matching with those on your system and press the login button.

![login](https://github.com/SzczerbiakJakub/Tetris/assets/89864279/85c1a9da-2536-4a26-9379-4d9b74cf14ce)


Once correct data is entered, the user will log in to the system. Incorrect data will raise this error:

![login failure](https://github.com/SzczerbiakJakub/Tetris/assets/89864279/8fa49d19-8fd7-4aaf-ac22-a5ac7e7b4cce)


After logging in, the below widget is seen.

![db_widget](https://github.com/SzczerbiakJakub/Tetris/assets/89864279/0d6712cd-ac43-43c5-8173-910608a5cfdb)


It is the heart of this software - here lies all the functionality of it. On the top-left side is the small
user-greeting site that contains information about the currently selected database and the selected table 
within it. At first, no database or table is selected (symbolised by a "-" sign). Here is also a logout
button - after the edition is completed, one can just disconnect from the system and the previously covered 
main widget will appear on the screen.

Below, also on the left side, is a databases and databases' tables widget. It consists of buttons and a list
containing information on available ones. As every single database can have multiple tables, they are signed
with an indent column placed below the name of the database they belong to. Using the mentioned buttons, it is
possible to edit database structure (create/delete databases, do the same operation with tables).
