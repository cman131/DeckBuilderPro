# MakeFriendsYouCanCallByNicknamesEvenWhenYouAreOld
A Python Flask web application to create CCG decks. The first iteration will only include magic cards, but will hopefully be expanded to include other games such as Weiss|Schwartz and Android: Netrunner.

##How to set up and run
###Linux
 1. Now we need to install a few things so open terminal and run these commands:

 ```
sudo bash linux-install.sh
 ```
 2. You also need to install and <a href='http://dev.mysql.com/downloads/windows/installer/'>set up mysql</a>
 3. Navigate to where you have cloned this project
   3.1. If you have not yet, follow the recommended git setup section or just do it how you want.
 4. Now make a copy of the config_example.py file named 'config.py'
 5. Now fill the user, password, and api_key variables with what you have from setting up mysql
 ```
import os
basedir = os.path.abspath(os.path.dirname(__file__))

MYSQL_DATABASE_USER = "iamtotallyavalidusername"
MYSQL_DATABASE_PASSWORD = "lookatmeimapassword"
MYSQL_DATABASE_DB = "DeckBuilder"
MYSQL_DATABASE_HOST = "localhost"
 ```
 <h5 style='color: red'>WARNING: Do NOT ever commit your config information</h5>
 <p>this would make them public knowledge</p>

 6. Now run the dbSetup.py with ```python dbSetup.py```
 7. If all went well you should now be able to run ```python run.py``` to start the server on <a href='http://localhost:5000'>localhost:5000</a>


<h1>Recommended Git Setup</h1>
1. Fork this project on github
2. Make sure you have <a href='https://git-scm.com/book/en/v2/Getting-Started-Installing-Git'>git installed</a>.
3. Now go ahead and open a terminal or git bash if on windows.
4. Navigate to the directory you want this project to be in.
5. Now execute ```git clone https://github.com/{GitUsername}/DeckBuilderPro.git```
  5.1 replace {GitUsername} with your git username
6. The remaining command is to set the remote ```git add remote upstream https://github.com/cman131/DeckBuilderPro.git```
