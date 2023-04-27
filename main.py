
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import pandas as pd
import re
#import docx


def crowler(role, skill):
    #creating windows and page

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
    # page.set_page_load_timeout(300)
    sleep(100)

    # choose use case
    """
    print("Use case: ")
    element = page.find_element(By.CLASS_NAME,'_button_10rvi_27')
    sleep(3)

    element = page.find_element(By.XPATH,' // img[ @ alt ="Cover Letter"]')
    sleep(5)
    #Select(element)
    print(element)
    sleep(5)
"""
   # cover_letter_element = page.find_element(By.XPATH,' // div[ @ data - value ="cover_letter"]')
   # sleep(10)
    #cover_letter_element.click()
    #sleep(10)
    #print("")
    #select = Select(page.find_element(By.ID, "select-type"))
    #print(select)

    #Job Role
    wait = WebDriverWait(page, 10)
    print("Job Role:")
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs--panel--0"]/form/div[3]/div[1]/div/input')))
    input_field.send_keys(role)
    sleep(10)

    #Job skills
    print("Job Skills : ")
    #waiting
    input_field = wait.until( EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs--panel--0"]/form/div[3]/div[2]/div/input')))
    input_field.send_keys(skill)
    sleep(10)

    #scroll
    page.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # last click
    print("click :")
    button = page.find_element(By.XPATH,'//*[@id="tabs--panel--0"]/form/div[5]/div/button')
    #button = page.find_element(By.CLASS_NAME,'_button_194hd_2_primary_194hd_53_medium_194hd_31')
    button.click()
    # if (page.find_element(By.ID,'popup').isDisplayed()):
    #     page.switchTo().alert().accept();
    #     button.click()

    sleep(10)

    #get letter
    div_letter = page.find_element(By.XPATH,'// *[ @ id = "root"] / div / div[1] / div[2] / div / div[3] / div / div')
    letter = div_letter.text
    print("Motivation Letter:")
    sleep(10)
    """
    checking if you are in right page
    if page.current_url.__contains__("/details"):

    """
    return letter
def preprocess(df):
    #print(df.info())

    #remove unusefuls column
    cols = ['country_code','deadline','start_date','program_url','tution_1_currency','tution_1_type','tution_2_type','tution_2_currency','facts',]
    df = df.drop(cols,axis=1)

    #remove duplicates
    df.drop_duplicates(inplace=True)

    #remove irrelevant data
    df = df[df['ielts_score'] < 10]
    df = df[df['ielts_score'] > 0]

    #remove outliers
    # get average of each kind of tuition money for compare
    avg = {}
    avg['Tuition (Year)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Year)', 'tution_1_money'].mean())
    avg['Tuition (Trimester)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Trimester)', 'tution_1_money'].mean())
    avg['Tuition (Month)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Month)', 'tution_1_money'].mean())
    avg['Tuition (Module)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Module)', 'tution_1_money'].mean())
    avg['Tuition (Semester)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Semester)', 'tution_1_money'].mean())
    avg['Tuition (Credit)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Credit)', 'tution_1_money'].mean())
    avg['Tuition (Full programme)'] = int(df.loc[df['tuition_price_specification'] == 'Tuition (Full programme)', 'tution_1_money'].mean())
    #standard data
    df.loc[df['tuition_price_specification'] == 'Tuition (Year)', 'tution_1_money'] = df['tution_1_money']/ 12
    df.loc[df['tuition_price_specification'] == 'Tuition (Trimester)', 'tution_1_money'] = df['tution_1_money']/ 3
    df.loc[df['tuition_price_specification'] == 'Tuition (Module)', 'tution_1_money'] = df['tution_1_money']/ 3
    df.loc[df['tuition_price_specification'] == 'Tuition (Semester)', 'tution_1_money']=df['tution_1_money'] / 8
    df.loc[df['tuition_price_specification'] == 'Tuition (Full programme)', 'tution_1_money'] =df['tution_1_money']/ 12
    average = df['tution_1_money'].mean()
    Q1 = df['tution_1_money'].quantile(0.25)
    Q3 = df['tution_1_money'].quantile(0.75)
    IQR = Q3 - Q1
    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    df = df[df['ielts_score'] < upper_range]
    df = df[df['ielts_score'] > lower_range]

    #Take Care of Missing Data
    df['ielts_score'] = df['ielts_score'].fillna(0, inplace=True)

    #remove Rows With Missing Value
    df=df.dropna(subset=['tution_1_money'])
    df.reset_index(drop=True, inplace=True)

    #standardize data
    # convert to lower case
    df['country_name'] = df['country_name'].str.lower()
    df['duration'] = df['duration'].str.lower()
    df['language'] = df['language'].str.lower()
    df['structure'] = df['structure'].str.lower()
    df['structure'] = df['structure'].str.replace('[','')
    df['structure'] = df['structure'].str.replace(']','')
    df['academic_req'] = df['academic_req'].str.lower()
    df['city'] = df['city'].str.lower()
    df['city'] = df['city'].str.replace("[^\w\s]","")

    #normalize

    #test data
    #print(df.sample(10))

    return df,average

def process_words(avg,df_raw,uni,pro):
    df = df_raw.copy()
    #print(df.info())
    structures = []#for col structure
    role = []
    skill = []

    #select university and program
    df = df.loc[df['university_name'].str.lower() == uni]
    df = df.loc[df['program_name'].str.lower() == pro]
    df.reset_index(drop=True, inplace=True)

    #print(df.info())

    if 0 in df.index:
#add information
        if(str(df.loc[0,'city']) != 'nan'):
            role.append(" in "+ str(df.loc[0,'city']))
        if(str(df.loc[0,'university_rank']) != 'nan'):
            role.append(" rank " + str(int(df.loc[0,'university_rank'])))
        if(str(df.loc[0,'duration']) != 'nan'):
            role.append(' longs ' + df.loc[0,'duration'])
    # split lessons
        structures.extend(str(df.loc[0, 'structure']).split(","))
    # Tuition comparison
        if(avg > df.loc[0,'tution_1_money']):
            role.append(' affordable ')
    #split requirement
        requirements = df.loc[0,'academic_req']
        requirements = re.sub('.*<ul>', '', requirements)
        requirements = re.sub('</section>.*','',requirements)
        requirements = re.sub('<[^<]+?>', '', requirements)
        print("Requirements:\n" ,requirements)


    # replace special characters
    for x in structures:
        x = re.sub('[0-9]', '', x)
        x = re.sub('[\(\[].*?[\)\]]','',x)
        x = x.replace("[^\w\s]","")
        x = x.replace("'","")
        x = x.replace('"','')
        skill.append(x)

    df.to_csv("output.csv")
    return role , skill

"""
American University of Armenia
Economics
ferdowsi shamim
"""
if __name__ == '__main__':
    #get information from user
    uni = input('What is your University name?\n')
    pro = input('What is your Program name?\n')
    key_list_user = input("Enter your keywords:\n").split(" ")
    # uni = 'Flinders University'
    # pro = 'Clinical Education'
    # key_list_user =['ferdowsi','shamim']
    role=[uni," "+pro]
    #read file
    df = pd.read_csv('201709301651_masters_portal.csv')
    #preprocess file
    df,ave = preprocess(df)
    #get keywords and spilit in Job Role & Job Skill because of rytr.me
    r,skill = process_words(ave,df,uni.lower(),pro.lower())
    role.extend(r)
    #add user keys
    key_list_user.extend(skill)
    print("Role:\n",role,"\nSkill:\n",key_list_user)
    #crawl letter from website and print
    letter = crowler(role ,key_list_user)
    print(letter)
    #Add the letter to the document & Save the document
    # document = docx.Document()
    # document.add_paragraph(letter)
    # document.save('motivationLetter.docx')
""""
    # put words back together
    df['clean'] = df['clean'].apply(
    lambda x: ' '.join(w for w in x))
"""


"""
 how preprocess dataset for keyword extraction in py step by step

    Load the dataset: First, you need to load the dataset into Python using the appropriate library. For example, if the dataset is in a .csv format, you can use the pandas library to read the file.

    Clean the data: Once the dataset is loaded, you need to clean it by removing any irrelevant or missing data. This can include removing any punctuation, removing any stop words, and correcting any spelling errors.

    Tokenize the data: Tokenization is the process of breaking the text into smaller pieces, such as words or phrases. This can be done using the Natural Language Toolkit (NLTK) library.

    Lemmatize the data: Lemmatization is the process of reducing words to their root form. This can be done using the NLTK library.

    Calculate the frequency of words: Once you have lemmatized the data, you can calculate the frequency of each word in the dataset. This can be done using the Counter library.

    Extract keywords: Finally, you can use the frequency of words to extract keywords from the dataset. This can be done using the TF-IDF algorithm.


"""
