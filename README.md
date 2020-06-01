# INSZOOM project
## Business Requirement 2 - Build a intelligent interface to the database through which user can query it in natural language

##### List of Objectives :-
###### 1. The user shall be able to enter the query in natural language
###### 2. The model shall be able to convert the NL query into SQL query
###### 3. The model shall be able to fire the SQL query on database
###### 4. The user shall be able to view the fetched data from the database

##### Tools used :-
###### 1. spaCy
###### A natural language processing tool to carry out lemmatization, POS_tagging and tokenization on the input query. It is written in Cython and offers the fastest syntactic parser in the market.
###### Steps for installation : pip install -U spaCy and python -m spacy download en_core_web_sm
###### For more details visit: https://spacy.io/usage
###### 2. fuzzywuzzy
###### A sequence matcher based on Levenshtein distance
###### 3. Flask
###### For building the chatbot.

##### Steps for starting the application :-
###### 1. python database.py
###### First the SQL script file in database.py has to be run in order to create the database. You can add the script for your own database here.
###### 2. In mappings.csv you can provide the mapping structure for your specified database
###### 3. In pk_fk.csv you can provide the primary key-foreign key combinations for your specified database
###### 4. python br2_spacy.py - If you want to check the SQL generated manually
###### 5. python application.py - Starts the chatbot at localhost. Open your browser and type http://127.0.0.1:5000/ to view.




