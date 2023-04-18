# Automatic-motivation-letter-writing

In this project, we want a special motivation letter with the help of user input and the information we extract from university datasets
Write the desired field and university of the user.
In this program, we first ask the user for the desired university and the field he intends to apply for. Then some keywords from him
We get what we want. These keywords are the user's personal information such as GPA, major, university where he studies, etc.
Then, according to the name of the entered university and the entered field, we search in the dataset and find some keywords related to the total key.
We add words.
In the next step, we give these keywords to www.rytr.com, which is a writing assistant, to generate the motivation letter for us.

Sample input:
Stanford University
Computer Science
Bachelor of Computer Engineering, Ferdowsi University of Mashhad, GPA of 4, TA of Data
Mining Course, 3 years of work experience

Sample output:
A motivation letter in which these words are used directly or indirectly

preprocessing the second part of the project:
• Text preprocessing & keyword extraction
In this part, you should perform pre-processing on the dataset according to what you learned in the lesson. The steps below are sample preprocessing
There are things that need to be done. You can also do other pre-processing such as stemming or lemmatization
Do it if needed.
1. Text cleaning
2. Stop word removal
3. Tokenization
• Have a column named extracted_keywords and for each string the keywords you extracted
let the. Then draw the word cloud of this column.

After pre-processing, a code must be written that takes the name of the university and the desired field (the first and second lines in the input sample above),
Returns a number of related words of that string to the user.
Here, related words can be from the following categories:
The name of the courses of that field, the city of that university, the prerequisites of that course or field, the rank of the university, etc.
Or, for example, you can consider the keyword "affordable" if the desired course has a tuition fee of less than $5000.

This dataset contains 60425 master degree programs from around the world
Data columns (total 23 columns):
1. country_name: the name of the country where the university offering the program is
located.
2. country_code: the ISO 3166-1 alpha-2 country code for the country where the university
offering the program is located.
3. university_name: the name of the university offering the program.
4. university_rank: the rank or rating of the university offering the program, which could be
based on various criteria such as research output, teaching quality, reputation, etc.
5. program_name: the name of the master's program being offered by the university.
6. program_type: the type of program, which could be MSc, MBA or etc.
7. deadline: the deadline for submitting an application to the program.
8. duration: the duration of the program in months or years.
9. Language: the language of instruction for the program.
10. tution_1_currency: the currency of the tuition fees for the program.
11. tution_1_money: the amount of the tuition fees for the program, in the currency specified
in the previous column.
12. tution_1_type: the type of tuition fees, which could international, national, or some other
type.
13. tution_2_currency: the currency of an additional tuition fee (if applicable) for the
program.
14. tution_2_money: the amount of the additional tuition fee (if applicable) for the program,
in the currency specified in the previous column.
15. tution_2_type: the type of the additional tuition fee (if applicable), which could be
international, national or some other type.
16. tuition_price_specification: This column contains additional information about the tuition
fees, such as whether the tuition fee is for one semester or a year.
17. start_date: the start date of the program.
18. ielts_score: the minimum required IELTS score for non-native speakers of English to
apply to the program.
19. Structure: This column contains information about the structure of the program, such as
the name of the courses in the program.
20. academic_req: academic requirement for applying to this program.
21. facts: some information about this program and university.
22. City: the city where the program will be held.
23. program_url: the link to the program websit
