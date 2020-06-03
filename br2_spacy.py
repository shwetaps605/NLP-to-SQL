import spacy
nlp=spacy.load("en_core_web_sm")
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from itertools import combinations
import re
import pymysql
import datetime  


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
all_stopwords.add("equal")
all_stopwords.add("reverse")

synonyms= {'petitioner':["petitioner,company"],
"beneficiary":["client,applicant,beneficiary"],
"case":["case,application"]}

sum_synonyms=['sum','total']
count_synonyms=['count']
average_synonyms=['mean','average']
max_synonyms=['maximum','largest','highest','most']
min_synonyms=['minimum','smallest','lowest','least']
asc_synonyms=['ordered','sorted','alphabetical','alphabetically','increasing','ascending','alphabetic']
desc_synonyms=['reverse','descending']
equal_synonyms=['equal','=','==']
greater_synonyms=['greater','larger','bigger','>']
lesser_synonyms=['lesser','smaller','less','<']
between_synonyms=['between','range']
 
databaseServerIP            = "127.0.0.1"  # IP address of the MySQL database server
databaseUserName            = "root"       # User name of the database server
databaseUserPassword        = "root"           # Password for the database user
charSet                     = "utf8mb4"     # Character set
cusrorType                  = pymysql.cursors.DictCursor


data=pd.read_csv("mappings.csv")
idx=list(data[data['keywords'].isnull()].index)
data.drop(idx,axis=0,inplace=True)
PK_FK=pd.read_csv("Sheet2.csv")


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
    #final_list=list(set(final_list))
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
    all_keywords_list=[]
    idx_list=[]
    table=""

    for i in list_of_nouns :
        
        attr_list=list(data[data['keywords'].str.contains(i)]['Attributes'])
        if(len(attr_list)!=0):
            all_keywords_list.append(attr_list)

    common_attrs=[]
    for k in all_keywords_list:
       
        if(k == all_keywords_list[0]):
            common_attrs=list(set(k).union(common_attrs))
           
        else:
             if(len(list(set(k).intersection(common_attrs)))!=0):
                common_attrs=list(set(k).intersection(common_attrs))
                
            
    print("ALL THE COMMON ATTRIBUTES ARE:\n",common_attrs)
    a=common_attrs

           

    if(len(a)!=0):
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
       
        a_idx=data[data['Attributes']==a_max].index
        final_idx= a_idx
       
        for k in range(len(list(data['Attributes']))):
            if list(data['Attributes'])[k]==a_max:
                table=list(data['Table Name'])[k]
                break
        

    else:
        a_max=""
        table=""

    return a_max,table

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
    tab_list=[]
    attributes_list=[]
    attribute_string=[]
    tables_string=""
    order_by_string=""
    group_by_string=""
    o_str=""
    a_str=""
    attr=""
    
    que_list=re.split('and|,',clause)
   
    
    for i in que_list:

        if ("each" in i.lower().split()):
            group_by_clause=re.split("each",i)
            print(i)
            print("GROUP BY CLAUSE: ",group_by_clause)
            group_by_attribute,group_by_table=get_pos(group_by_clause[1])
            group_by_string=f"GROUP BY {group_by_attribute}"
            print("GROUP BY WALA STRING YE HAI",group_by_string)
            i=group_by_clause[0]
            tab_list.append(group_by_table)

        if(checkAggregateSum(i)):
            a_str="SUM"
     

        elif(checkAggregateAverage(i)):
            a_str="AVG"

        elif(checkAggregateCount(i)):
            a_str="COUNT"
            
        elif(checkAggregateMax(i)):
            a_str="MAX"

        elif(checkAggregateMin(i)):
            a_str="MIN"
            

        elif(checkAscendingOrder(i)):
            o_str="ASC"  

        elif(checkDescendingOrder(i)):
            o_str="DESC"  
        
        else:
            a_str=""
            o_str=""

        a,table_name=get_pos(i)

        if(len(a)!=0):
            print(f"\nATTRIBUTE FOUND:{a}\n")

            if a not in attributes_list:
                attributes_list.append(a)
                
            if table_name not in tab_list:
                tab_list.append(table_name)

            if(len(a_str)!=0):
                attr=a_str+"("+str(a)+")"
                
            else:
                attr=str(a)

            attribute_string.append(attr)

            if(len(o_str)!=0):
                order_by_string+=str(a)+" "+o_str

            print(f"The corresponding attributes are:{attributes_list}")
            print(f"The corresponding tables are:{tab_list}\n")

        else:
            attribute_string=""

            
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
                
                w_string.append(f"{li[1]}.{k2}={li[0]}.{k1}")
            

            else:
                print("No PK-FK combinations found!!")
            
        where_string=" AND ".join(map(str,w_string))
        print(f"\nPK-FK clause:{where_string}\n")

    else:
        print("NO WHERE CLAUSE NEEDED\n")
        where_string=""
        
    return where_string


def checkEqual(q):
    li=q.lower().split()
    if(len(list(set(equal_synonyms).intersection(li)))>0):
        return True
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

def checkBetween(q):
    li=q.lower().split()
    if(len(list(set(between_synonyms).intersection(li)))>0):
        return True
    else:
        return False

def get_conditional_attributes2(clause):
    tab_list=[]
    attributes_list=[]
    attr_val={}
    main_query=[]
    date_flag=False
    
    que_list=re.split('\sand\s|,',clause)
    
    for i in que_list:

        i_tokens=[token.orth_ for token in nlp(i) if not token.is_punct | token.is_space]
        print("Conditional Clause:\n",i)
        i=" ".join(map(str,i_tokens))

        if(checkBetween(i)):
            val_list=re.split('\sbetween\s|\srange\s',i)
            bet_val_list=re.split('&|to',val_list[1].strip())
            bet_val_first=bet_val_list[0].strip()
            bet_val_second=bet_val_list[1].strip()
            
            if( (re.match('\d{4}-\d{2}-\d{2}', bet_val_first)) and (re.match('\d{4}-\d{2}-\d{2}',  bet_val_second)) ):
                date_flag=True
    
            a,table_name=get_pos(val_list[0])
            tab_and_attr=table_name+"."+a
        
            if(date_flag):
                conditional_query= tab_and_attr+ " "+ "BETWEEN" + " "+f"'{bet_val_first}'" + " " + "AND" + " "+ f"'{bet_val_second}'"
            else:
                conditional_query= tab_and_attr+ " "+ "BETWEEN" + " "+f"{bet_val_first}" + " " + "AND" + " "+ f"{bet_val_second}"

            main_query.append(conditional_query)
            tables=table_name
            if tables not in tab_list:
                tab_list.append(tables)
            continue
        
        if(checkEqual(i) and checkGreater(i)):
            val_list=re.split('\sequal to\s|=|==',i)
            val=val_list[1:]
            sign=">="
        
        elif(checkEqual(i) and checkLesser(i)):
            val_list=re.split('\sequal to\s|=|==',i)
            val=val_list[1:]
            sign="<="
        
        elif(checkEqual(i)):
            val_list=re.split('\sequal to\s|\s=\s|\s==\s',i)
            val=val_list[1:]
            sign="="
    
        elif (checkGreater(i)):
            val_list=re.split('greater than|larger than|bigger than|>',i)
            val=val_list[1:]
            sign=">"
            
        elif(checkLesser(i)):
            val_list=re.split('less than|smaller than|<',i)
            val=val_list[1:]
            sign="<"
            
        a,table_name=get_pos(i)
        tab_and_attr=table_name+"."+a

    
        if(checkAggregateAverage(val[0])):
            attr,tab=get_pos(i)
            tab_and_attr=tab+"."+attr
            val_string="(SELECT"+" "+"AVG"+"("+tab_and_attr+")"+" "+"FROM"+" "+tab+")"
        elif(checkAggregateMax(i)):
            attr,tab=get_pos(i)
            tab_and_attr=tab+"."+attr
            val_string="(SELECT"+" "+"MAX"+"("+tab_and_attr+")"+" "+"FROM"+" "+tab+")"
        elif(checkAggregateMin(i)):
            attr,tab=get_pos(i)
            tab_and_attr=tab+"."+attr
            val_string="(SELECT"+" "+"MIN"+"("+tab_and_attr+")"+" "+"FROM"+" "+tab+")"
        elif(checkAggregateSum(i)):
            attr,tab=get_pos(i)
            tab_and_attr=tab+"."+attr
            val_string="(SELECT"+" "+"SUM"+"("+tab_and_attr+")"+" "+"FROM"+" "+tab+")"
        else:
            val_string=f"'{val[0].strip()}'"

        
        if((data[data['Attributes']==a]['keywords'].str.contains("date").bool())):

            
            #For queries involving current/previous year
            if(re.search( "year", val_string ) or re.search( "year", i )):

                #Case I: The user is trying to look for current year entries
                if(re.search( "current", val_string ) or re.search( "present", val_string )):
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().year)
                 
                #Case II: The user is trying to look for previous year entries
                elif(re.search( "previous", val_string ) or re.search( "last", val_string ) or re.search( "past", val_string )):
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().year-1)

                #Case III: The user is trying to look for any other year entry
                else:
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+val_string



            #For queries involving current/previous month
            elif(re.search( "month", val_string) or re.search( "month", i)):

                 #Case I: The user is trying to look for current month entries
                if(re.search( "current", val_string ) or re.search( "present", val_string ) ):  
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().year)+" "+"AND"+" "+"MONTH"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().month)
                   
                #Case II: The user is trying to look for previous month entries
                elif(re.search( "previous", val_string ) or re.search( "last", val_string ) or re.search( "past", val_string )):
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().year)+" "+"AND"+" "+"MONTH"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().month-1)

                elif(re.search( "next", val_string ) ):
                    conditional_query= "YEAR"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().year)+" "+"AND"+" "+"MONTH"+"("+tab_and_attr+")"+" "+ sign + " "+str(datetime.datetime.now().month+1)  


        else:
            conditional_query= tab_and_attr+ " "+ sign + " "+val_string
            print(conditional_query)

        main_query.append(conditional_query)
        attributes_list.append(a)
        tab=list(data[data['Attributes']==a]['Table Name'])
        tables=table_name
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
        t=list(set(t1))

    
    if (len(a1)!=0):
        attr_string=",".join(map(str,a1))
        tab_string=" INNER JOIN ".join(map(str,t))
        pk_fk_part=get_pk_fk(t)
        print("\nCONDITIONAL QUERY:",conditional_query)
        print("\nPK-FK",pk_fk_part)
       

        if 'Document_details' in t:
            if 'Document_details' in conditional_query:
                print("YEEEEEHAAAWWW\n")
                tab_string=" INNER JOIN ".join(map(str,t))
            else:
                tab_string=" LEFT JOIN ".join(map(str,t))
        
        if(len(pk_fk_part)==0 and len(conditional_query)<=1 ):
            where_string=""
            sql_query=f"SELECT  {attr_string} \nFROM {tab_string}"
        elif(len(pk_fk_part)>0 and len(conditional_query)<=1):
            where_string=pk_fk_part
            sql_query=f"SELECT  {attr_string} \nFROM {tab_string} \nON {where_string}"

        elif(len(pk_fk_part)==0 and len(conditional_query)>=1):
            where_string=conditional_query
            sql_query=f"SELECT  {attr_string} \nFROM {tab_string} \nWHERE {where_string}"
        else:
            where_string=pk_fk_part+"\nWHERE "+conditional_query
            sql_query=f"SELECT {attr_string} \nFROM {tab_string} \nON {where_string}"

        if(len(order_by)!=0):
            sql_query+="\nORDER BY"+" "+order_by

        if(len(group_by)!=0):
            sql_query+="\n"+group_by

    else:
        sql_query=""

    return sql_query



def generate_data(query):
    char1='\t'
    connectionInstance   = pymysql.connect(host=databaseServerIP, 
    user=databaseUserName, 
    password=databaseUserPassword,
    charset=charSet,
    cursorclass=cusrorType)

    sql_query=""
    data_to_be_displayed=""

    try:
        sql_query=convert_into_sql(query)
        if(len(sql_query)!=0):
            
            NEWLINE='\n'
            try:
                cur = connectionInstance.cursor()                       
                cur.execute("USE INS")

                sqlQuery    = sql_query
                cur.execute(sqlQuery)
                rows = cur.fetchall()
                data_to_be_displayed=""
                print(f"\nSQL generated:\n\n{sql_query}\n")
                    
                attribute_names= [r.keys() for r in rows]
                header=attribute_names[0]
                width1=char1*6
                data_to_be_displayed+=width1.join(map(str,list(header)))+NEWLINE
                print()

                for row in rows:
                    records=width1.join(map(str,list(row.values())))
                    data_to_be_displayed+=records+NEWLINE
                
            except Exception as e:
                print("Exeception occured:{}".format(e))
                data_to_be_displayed="NO RESULTS FOUND"

            finally:
                connectionInstance.close()

        else:
            print("NO RESULTS FOUND\n")
            data_to_be_displayed="NO RESULTS FOUND"

    except Exception as e:
        print("Exeception occured:{}".format(e))
        print("NO QUERY GENERATED\n")
        data_to_be_displayed="NO RESULTS FOUND"
    return data_to_be_displayed

#nl_query="give me client EMPLOYEE id, client name, corporation NAMES of all clients "
#ss= generate_data(nl_query.lower())
#print(ss)











