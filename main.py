# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import numpy as np
import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def crowler():
    chromedriver_path = ".//chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\\Users\\Shamim\\AppData\\Local\\Google\\Chrome\\User Data")#Default
    options.add_argument("profile-directory=Default")
    options.add_argument("--no-sandbox");
    options.add_argument("--disable-dev-shm-usage");
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = 'normal'
    page = webdriver.Chrome(executable_path=chromedriver_path,chrome_options=options)
    page.get("https://app.rytr.me/create")

    #page.get("https://vu.um.ac.ir")
    sleep(60)
    select = Select(page.find_element(By.ID,"select-type"))
    print(select)
    # select by visible text
    select.select_by_visible_text('Cover Letter')
    sleep(60)
    print(select)
    sleep(60)
    """
    here you can find some useful codes

    scrolling page 

    page.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    explicit wait 

    page will wait until the element with class name of "submit-btn" is clickable
    after 10 seconds, if it is still not clickable, it will throw an exception, so you need to use
    catch block while using this

    submit = WebDriverWait(div, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-btn")))

    checking if you are in right page

    if page.current_url.__contains__("/details"):

    you can find multiple elements by using 
    find_elements_by_*
    then you need to iterate over the list
    """
    return 0
def preprocess(df):
    print(df.info())
    # convert to lower case
    df['country_name'] = df['country_name'].str.lower()
    df['university_name'] = df['university_name'].str.lower()
    df['program_name'] = df['program_name'].str.lower()
    df['duration'] = df['duration'].str.lower()
    df['structure'] = df['structure'].str.lower()
    df['city'] = df['city'].str.lower()

    #remove duplicates
    df.drop_duplicates(inplace=True)

    #remove unusefuls column
    cols = ['deadline','start_date','program_url','tution_1_currency','tution_2_currency']
    df = df.drop(cols,axis=1)
    #Take Care of Missing Data
    df['university_rank'] = df['university_rank'].fillna(900)
    #remove Rows With Missing Values
    df=df.dropna(subset=['tution_2_type'])
    df.reset_index(drop=True, inplace=True)

    #change tution money to term
    avg ={}
    avg['Tuition (Year)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Year)','tution_2_money'].mean())
    avg['Tuition (Trimester)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Trimester)','tution_2_money'].mean())
    avg['Tuition (Month)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Month)','tution_2_money'].mean())
    avg['Tuition (Module)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Module)','tution_2_money'].mean())
    avg['Tuition (Semester)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Semester)','tution_2_money'].mean())
    avg['Tuition (Credit)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Credit)','tution_2_money'].mean())
    avg['Tuition (Full programme)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Full programme)','tution_2_money'].mean())
    return df,avg

def process_words(avg,df_raw,uni,pro):
    df = df_raw.copy()
    structures = []
    requirements = []
    kw = []

    #select university and program
    df = df.loc[df['university_name'] == uni]
    df = df.loc[df['program_name'] == pro]

    #split lessons
    for x in df['structure']:
        structures.extend(str(x).split(","))
    #Tuition comparison
    if(avg[str(df.loc[0,'tuition_price_specification'])] > df.loc[0,'tution_2_money']):
        kw.append('affordable')

    #add information
    kw.append(df.loc[0,'university_rank'])
    kw.append(df.loc[0,'city'])
    kw.append(df.loc[0,'duration'])

    p3 = '.*<ul>'
    #split requirement
    for x in df['academic_req']:
        x = re.sub(p3, '', x)
        requirements.extend(str(x).split("<li>"))
        print("r=" ,x)
    # replace special characters
    p1 = r'[0-9]'
    p2 = '[\(\[].*?[\)\]]'
    for x in structures:
        x = x.replace(",","")
        x = x.replace("[","")
        x = x.replace("]","")
        x = x.replace("'","")
        x = x.replace('"','')
        x = re.sub(p1, '', x)
        x = re.sub(p2,'',x)
        kw.append(x)
    print(avg[str(df.loc[0,'tuition_price_specification'])])

    df.to_csv("output.csv")
    return kw

"""
<section id="AcademicRequirements"> <h2>Academic Requirements</h2> <section id="StudyRequirement"> <h6>Entry requirements</h6><p>To be eligible for entry to this program, you must have:</p><ul>

American University of Armenia
Economics
ferdowsi shamim
"""
if __name__ == '__main__':

    uni = input('What is your University name?\n')
    pro = input('What is your Program name?\n')
    key_list = input("Enter your keywords:\n").split()
    df = pd.read_csv('201709301651_masters_portal.csv')
    df,ave = preprocess(df)
    key_list.extend(process_words(ave,df,uni.lower(),pro.lower()))
    print(key_list)
    #crowler()

""""

    # tokenize columns
    df['clean'] = df['clean'].apply(lambda x: word_tokenize(x))

    # lemmatizing the words
    df['clean'] = df['clean'].apply(lambda x: [WordNetLemmatizer().lemmatize(w) for w in x])

    # remove stop words from token list
    df['clean'] = df['clean'].apply(
        lambda x: [w for w in x if
                   w not in stopwords.words('english')])

    # stemming the words
    df['clean'] = df['clean'].apply(
        lambda x: [PorterStemmer().stem(w) for w in x])

    # put words back together
    df['clean'] = df['clean'].apply(
        lambda x: ' '.join(w for w in x))
"""


