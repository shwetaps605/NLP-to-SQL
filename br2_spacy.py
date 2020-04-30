import spacy
nlp=spacy.load("en_core_web_sm")
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from itertools import combinations
import re
import pymysql


all_stopwords = nlp.Defaults.stop_words
all_stopwords.add("show")
all_stopwords.add("display")
all_stopwords.add("provide")
all_stopwords.remove('first')
all_stopwords.remove("name")
all_stopwords.remove("last")
all_stopwords.add("different")
all_stopwords.add("total")
all_stopwords.add("sum")
all_stopwords.add("average")
all_stopwords.add("maximum")
all_stopwords.add("minimum")
all_stopwords.add("increasing")
all_stopwords.add("decreasing")
all_stopwords.add("order")
all_stopwords.add("count")

synonyms= {'petitioner':["petitioner,company"],
"beneficiary":["client,applicant,beneficiary"],
"case":["case,application"]}
 
databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
databaseUserName            = "root"       # User name of the database server
databaseUserPassword        = "root"           # Password for the database user
charSet                     = "utf8mb4"     # Character set
cusrorType                  = pymysql.cursors.DictCursor


data=pd.read_csv("mappings.csv")
idx=list(data[data['keywords'].isnull()].index)
data.drop(idx,axis=0,inplace=True)
#print(data.head())

PK_FK=pd.read_csv("Sheet2.csv")
#print(PK_FK.head())

def search(myDict, lookup):
    for key, value in myDict.items():
        for v in value:
            if lookup in v:
                return key


def get_all_nouns(data):
    attribute_name=data[data['POS'].str.contains("NN",case=False, na=False)]['Words']
    attribute_name2=data[data['POS'].str.contains("JJ",case=False, na=False)]['Words']
    attribute_name3=data[data['POS'].str.contains("VB",case=False, na=False)]['Words']
    
    nouns_list=list(attribute_name)
    adjectives_list=list(attribute_name2)
    verbs_list=list(attribute_name3)

    nouns_and_adjectives=nouns_list+adjectives_list
    print(f"The nouns and adjectives are: {nouns_and_adjectives} \n")

    in_string=' '.join([str(elem) for elem in nouns_and_adjectives])
    lemmatized_nouns_and_adjectives = [word.lemma_ for word in nlp(in_string)]
    print (f"Lemmatizing the nouns and adjectives...\n{lemmatized_nouns_and_adjectives}\n")

    print(f"Verbs are: {verbs_list}\n")

    final_list=lemmatized_nouns_and_adjectives+verbs_list
    final_list=[str(elem) for elem in final_list]
    
    #Removing the unnecessary stop words
    final_list=[word for word in final_list if not word in all_stopwords]
    final_list=list(set(final_list))
    print(f"Removing the unnecessary words \nThe final list is:\n{final_list}\n")

    final_list2 = [ search(synonyms,w) for w in final_list if search(synonyms,w) is not None]
   
    return final_list

def convert_into_df(pos_tags):
    word_list=[]
    pos_list=[]
    for i in pos_tags:
        word_list.append(i[0])
        pos_list.append(i[1])
    return pd.DataFrame({"Words":word_list, "POS":pos_list})


def get_pos(query):
    
    doc = nlp(query)
    print(f"\nOriginal query:\n{doc}\n")
    
    tokens=[token.orth_ for token in doc if not token.is_punct | token.is_space]
    print(f"Tokenizing...:\n{tokens}\n")
    
    que_string = ' '.join([str(elem) for elem in tokens])
    pos_tags = [(i, i.tag_) for i in nlp(que_string)] 
    print(f"Tagging the parts of speech:\n{pos_tags}\n")
    
    df=convert_into_df(pos_tags)
    list_of_nouns=get_all_nouns(df)
    
    a=[]
    attr_list=[]

    for i in list_of_nouns :
        attr_list=list(data[data['keywords'].str.contains(i)]['Attributes'])

        if (i==list_of_nouns[0]):
            a=list(set(a).union(attr_list))
            print(f"{i}: {a}\n")

        else:
            #ensure that the selected candidate attributes have all the keywords
            if (len(list(set(a).intersection(attr_list)))!=0):
                a=list(set(a).intersection(attr_list))
            print(f"{i} : reduced to {a}\n")

    print(f"The possible attributes are:\n{a}\n")
    
    sim_dict={}
    s=0
    for i in a:
        s=0
        for j in list_of_nouns :
            s+=fuzz.token_set_ratio(i,j)
        sim_dict[i]=s
    print(sim_dict)
    
    a_list = max(sim_dict, key=sim_dict.get).split() 
    a_max= ",".join(map(str,a_list))
    return a_max

sum_synonyms=['sum','total']
count_synonyms=['count']
average_synonyms=['mean','average']
max_synonyms=['maximum','largest','highest','most']
min_synonyms=['minimum','smallest','lowest','least']
asc_synonyms=['ordered','sorted','alphabetical','alphabetically','increasing','ascending','alphabetic']
desc_synonyms=['reverse','descending']

def checkAggregateSum(q):
    li=q.lower().split()
    if(len(list(set(sum_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkAggregateAverage(q):
    li=q.lower().split()
    if(len(list(set(average_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkAggregateMax(q):
    li=q.lower().split()
    if(len(list(set(max_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkAggregateMin(q):
    li=q.lower().split()
    if(len(list(set(min_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkAggregateCount(q):
    li=q.lower().split()
    if(len(list(set(count_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkAscendingOrder(q):
    li=q.lower().split()
    if(len(list(set(asc_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkDescendingOrder(q):
    li=q.lower().split()
    if(len(list(set(desc_synonyms).intersection(li)))>0):
        return True
    else:
        return False



def get_attributes(clause):
    #print("Searching for..",clause)
    tab_list=[]
    attributes_list=[]
    attribute_string=[]
    tables_string=""
    order_by_string=""
    o_str=""
    a_str=""
    attr=""
    
    que_list=re.split('and|,',clause)
    group_by_clause=re.split("each"," ".join(map(str,que_list)))
    group_by_attribute=get_pos(group_by_clause[1])
    group_by_string=f"GROUP BY {group_by_attribute}"
    print("EACH KA SPLIT\n",group_by_clause)
    print("EACH KA ATTRIBUTE\n",group_by_attribute)
    print(que_list)
    
    for i in que_list:

        if(checkAggregateSum(i)):
            print("SUM hai\n",i)
            a_str="SUM"
     

        elif(checkAggregateAverage(i)):
            print("Average hai\n",i)
            a_str="AVG"

        elif(checkAggregateCount(i)):
            print("Count hai\n",i)
            a_str="COUNT"
            
        elif(checkAggregateMax(i)):
            print("Maximum hai\n",i)
            a_str="MAX"
            

        elif(checkAggregateMin(i)):
            print("Minimum hai\n",i)
            a_str="MIN"
            

        elif(checkAscendingOrder(i)):
            print("Ascending hai\n",i)
            o_str="ASC"  

        elif(checkDescendingOrder(i)):
            print("Descending hai\n",i)
            o_str="DESC"  
        
        else:
            a_str=""
            o_str=""

        print("###",i)
        a=get_pos(i)
        print(f"\nATTRIBUTE FOUND:{a}\n")

        if a not in attributes_list:
            attributes_list.append(a)
            
        tab=list(data[data['Attributes']==a]['Table Name'])
        tables=",".join(map(str,tab))
        if tables not in tab_list:
            tab_list.append(tables)

        if(len(a_str)!=0):
            attr=a_str+"("+str(a)+")"
            
        else:
            attr=str(a)

        attribute_string.append(attr)

        if(len(o_str)!=0):
            order_by_string+=str(a)+" "+o_str


        print("HMMMM\n",attribute_string)

    
    print(f"The corresponding attributes are:{attributes_list}")
    print(f"The corresponding tables are:{tab_list}\n")
            
    return attribute_string,tab_list,order_by_string,group_by_string


def get_pk_fk(tab_list):
    
    if len(tab_list)>1:    
        key_table1_list=[]
        key_table2_list=[]
        w_string=[]

        comb = combinations(tab_list, 2)
        joining_tables=[['headquarter','Petitioner'],
        ['Petitioner','Beneficiary'],
        ['Petitioner','caseprocess'],
        ['Beneficiary','caseprocess'],
        ['caseprocess','caseapproval'],
        ['Petitioner','caseapproval'],
        ['Beneficiary','caseapproval'],
        ['Document_details','Beneficiary']]
       
        for i in list(comb):
            
            if (list(i) not in joining_tables):
                if(list(i)[::-1] not in joining_tables):
                    print("No PK-FK pair for",list(i))
                    continue
            
            li=list(i)
            li=[w.lower() for w in li]
            sorted(li, key=str.lower)
        
            print("\nATRRIBUTE 1 \n",li[0].lower())
            print("\nATRRIBUTE 2 \n",li[1].lower())
         
            r=PK_FK[(PK_FK['Table1']== li[0]) & (PK_FK['Table2']== li[1])]
            r1=PK_FK[(PK_FK['Table1']== li[1]) & (PK_FK['Table2']== li[0])]

            if(r.shape[0]!=0):
               
                for k1 in list(r['Key-Table1']):
                    if k1 not in key_table1_list:
                        key_table1_list.append(k1)

                for k2 in list(r['Key-Table2']):
                    if k2 not in key_table2_list:
                        key_table2_list.append(k2)

                w_string.append(f"{li[0]}.{k1}={li[1]}.{k2}")


            elif(r1.shape[0]!=0):
                
                for k1 in list(r1['Key-Table2']):
                    if k1 not in key_table1_list:
                        key_table1_list.append(k1)

                for k2 in list(r1['Key-Table1']):
                    if k2 not in key_table2_list:
                        key_table2_list.append(k2)
                
                w_string.append(f"{li[1]}.{k1}={li[0]}.{k2}")
                

            else:
                print("No PK-FK combinations found!!")
            
        where_string=" AND ".join(map(str,w_string))

    else:
        print("NO WHERE CLAUSE NEEDED\n")
        where_string=""
        
    return where_string

equal_synonyms=['equal', '=','==']
greater_synonyms=['greater','larger','bigger','>']
lesser_synonyms=['lesser','smaller','less','<']


def checkEqual(q):
    print("EQUAL HAI\n")
    li=q.lower().split()
    match=(set(equal_synonyms).intersection(li))
    if(len(list(match)>0)):
        return match
    else:
        return False
    
def checkGreater(string):
    li=list(string.lower().split())
    if(len(list(set(greater_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def checkLesser(string):
    li=string.lower().split()
    if(len(list(set(lesser_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def get_conditional_attributes2(clause):
    tab_list=[]
    attributes_list=[]
    attr_val={}
    main_query=[]
    
    que_list=re.split('\sand\s|,',clause)
    
    for i in que_list:

        print("Conditional Clause:\n",i)
        
        if(checkEqual(i) and checkGreater(i)):
            val_list=re.split('\sequal to\s|=|==',i)
            val=val_list[1:]
            sign=">="
        
        elif(checkEqual(i) and checkLesser(i)):
            val_list=re.split('\sequal to\s|=|==',i)
            val=val_list[1:]
            sign="<="
        
        elif(checkEqual(i)):
            val_list=re.split('\sequal to\s|=|==',i)
            val=val_list[1:]
            sign="="
            print(val_list)
            print(val[0])
            
        elif (checkGreater(i)):
            val_list=re.split('greater than|larger than|bigger than|>',i)
            val=val_list[1:]
            sign=">"
            
        elif(checkLesser(i)):
            val_list=re.split('less than|smaller than|<',i)
            val=val_list[1:]
            sign="<"
            
        elif("between" in i.lower().split() or "range" in i.lower().split() ):
            val_list=re.split('\sbetween\s|\srange\s',i)
            bet_val_list=re.split('-|to',val_list[1].strip())
            bet_val_first=bet_val_list[0].strip()
            bet_val_second=bet_val_list[1].strip()
            a=get_pos(val_list[0])
            conditional_query= a+ " "+ "BETWEEN" + " "+f"'{bet_val_first}'" + " " + "AND" + " "+ f"'{bet_val_second}'"
            main_query.append(conditional_query)
            tab=list(data[data['Attributes']==a]['Table Name'])
            tables=",".join(map(str,tab))
            if tables not in tab_list:
                tab_list.append(tables)
            continue
    
        a=get_pos(i)
        conditional_query= a+ " "+ sign + " "+f"'{val[0].strip()}'"
        main_query.append(conditional_query)
        attributes_list.append(a)
        tab=list(data[data['Attributes']==a]['Table Name'])
        tables=",".join(map(str,tab))
        if tables not in tab_list:
            tab_list.append(tables)
                
    return attributes_list,tab_list,main_query


def convert_into_sql(query):
    query_clauses=re.split('having|where|whose|with',query)
    
    non_conditional_clause=query_clauses[0]
    print("QUERY CLAUSE:\n",query_clauses)
    conditional_clause=query_clauses[1:]
    
    a1,t1,order_by,group_by=get_attributes(non_conditional_clause)
    
    if (len(conditional_clause)!=0):
        a2,t2,q2=get_conditional_attributes2(" ".join(map(str,conditional_clause)))
        conditional_query=" AND ".join(map(str,q2))
        t=list(set(t1).union(t2))
    else:
        conditional_query=""
        t=t1

    attr_string=",".join(map(str,a1))
    tab_string=",".join(map(str,t))
    pk_fk_part=get_pk_fk(t)
   
    if(len(pk_fk_part)==0 and len(conditional_query)<=1 ):
        where_string=""
        sql_query=f"SELECT DISTINCT {attr_string} \nFROM {tab_string}"
    elif(len(pk_fk_part)>0 and len(conditional_query)<=1):
        where_string=pk_fk_part
        sql_query=f"SELECT DISTINCT {attr_string} \nFROM {tab_string} \nWHERE {where_string}"
    else:
        where_string=pk_fk_part+" AND "+conditional_query
        sql_query=f"SELECT DISTINCT {attr_string} \nFROM {tab_string} \nWHERE {where_string}"

    if(len(order_by)!=0):
        sql_query+="\nORDER BY"+" "+order_by

    if(len(group_by)!=0):
        sql_query+="\n"+group_by
    
    return sql_query



def generate_data(query):

    connectionInstance   = pymysql.connect(host=databaseServerIP, 
    user=databaseUserName, 
    password=databaseUserPassword,
    charset=charSet,
    cursorclass=cusrorType)

    sql_query=convert_into_sql(query)
    print(f"SQL generated:\n\n{sql_query}\n")

    NEWLINE='\n'

    try:
        cur = connectionInstance.cursor()                       
        cur.execute("USE INS")

        sqlQuery    = sql_query
        cur.execute(sqlQuery)
        rows = cur.fetchall()
        data_to_be_displayed=""
        
        attribute_names= [r.keys() for r in rows]
        header=attribute_names[0]
        data_to_be_displayed+="\t".join(map(str,list(header)))+NEWLINE

        for row in rows:
            records="\t\t\t\t".join(map(str,list(row.values())))
            data_to_be_displayed+=records+NEWLINE
            

    except Exception as e:
        print("Exeception occured:{}".format(e))
        data_to_be_displayed=" "

    finally:
        connectionInstance.close()

    return data_to_be_displayed

nl_query="Display case approval date and beneficiary visas"
ss= generate_data(nl_query.lower())
print(ss)











