import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import glob
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import textract
from PyPDF2 import PdfFileReader
import subprocess
from pdfminer.pdfparser import PDFSyntaxError
import tqdm
import transformers
from transformers import pipeline
from tqdm import tqdm
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import docx2txt
import nltk
import re,string,unicodedata
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
import re,codecs
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity
import heapq
from operator import itemgetter
import pandas as pd
import numpy as np

#st.warning("Go to login page and then try this page")

@st.experimental_singleton
def models():
    model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
    tokenizer = AutoTokenizer.from_pretrained("t5-base")
    return model,tokenizer

model,tokenizer = models()

def pdf_text_conversion(file):
    pdf_text = PdfFileReader(file)
    current_page = 0
    text = ''
    number_pages = pdf_text.numPages
    while current_page<number_pages:
        x = pdf_text.getPage(current_page)
        file = x.extractText()
        text = text+file
        text = text.replace("\n","")
        current_page += 1
    return text

def remove_non_words(text):
    return ' '.join(re.findall(r"[^\W\d\s]+", text))

def to_lowercase(text):
    return text.lower()

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)

def apply_nltk(resume_parser_files):
    for m,i in enumerate(resume_parser_files):
        resume_parser_files[m] = remove_non_words(resume_parser_files[m])
        resume_parser_files[m]  = to_lowercase(resume_parser_files[m])
        resume_parser_files[m] = remove_punctuation(resume_parser_files[m])
    return resume_parser_files



def concat_all_files(files):
    list_files = []
    list_pdf = []
    list_doc = []
    list_docx = []
    for file in files:
        if file.name.endswith("pdf"):
            list_pdf.append(file)
        if file.name.endswith("doc"):
            list_doc.append(file)
        if file.name.endswith("docx"):
            list_docx.append(file)

        list_files = list_pdf + list_doc + list_docx
    return list_files

Ordered_list_Resume  = []
def parser(list_files):
    list_resume = []
    Temp_pdf = []
    Resumes = []
    for no,i in enumerate(list_files):
        #print(i)
        Ordered_list_Resume.append(i.name)
        Temp = i.name.split(".")
        

        print(Temp[1])
        if Temp[1] == "pdf" or Temp[1] == "PDF":
            try:
                text_extracted = pdf_text_conversion(i)
                Resumes.extend([text_extracted])
            except Exception as e: 
                print(e)

        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":  
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
            except Exception as e: 
                print(e)
    
        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            try:
                text = docx2txt.process(i)
                b = str(text)
                c = [b]
                Resumes.extend(c)
            except Exception as e: print(e)

        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
                print("This is EXE" , i)
                pass

        print("Done Parsing.")

    return Resumes


def jb_parser(list_files):
    list_resume = []
    Temp_pdf = []
    Resumes = []
    for no,i in enumerate(list_files):
        #print(i)
        Temp = i.name.split(".")
        if Temp[1] == "pdf" or Temp[1] == "PDF":
            try:
                text_extracted = pdf_text_conversion(i)
                Resumes.extend([text_extracted])
            except Exception as e: 
                print(e)

        if Temp[1] == "doc" or Temp[1] == "Doc" or Temp[1] == "DOC":  
            try:
                a = textract.process(i)
                a = a.replace(b'\n',  b' ')
                a = a.replace(b'\r',  b' ')
                b = str(a)
                c = [b]
                Resumes.extend(c)
            except Exception as e: 
                print(e)
    
        if Temp[1] == "docx" or Temp[1] == "Docx" or Temp[1] == "DOCX":
            try:
                text = docx2txt.process(i)
                b = str(text)
                c = [b]
                Resumes.extend(c)
            except Exception as e: print(e)

        if Temp[1] == "ex" or Temp[1] == "Exe" or Temp[1] == "EXE":
                print("This is EXE" , i)
                pass

        print("Done Parsing.")

    return Resumes

def job_desc_model(tttt,model,tokenizer):
    inputs = tokenizer(tttt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(
        inputs["input_ids"],max_length = 150,min_length = 40,length_penalty=2.0, num_beams=4, early_stopping=False
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens = True)
    return result

def fine_tune_model(Resumes,model,tokenizer):
    text = []
    for i in Resumes:
        tttt = str(i)
        try:
            inputs = tokenizer(tttt, return_tensors="pt", max_length=512, truncation=True)
            outputs = model.generate(
                inputs["input_ids"],max_length = 200,min_length = 50,length_penalty=2.0, num_beams=4, early_stopping=False
            )
            result = tokenizer.decode(outputs[0], skip_special_tokens = True)
            text.append(result)
        except:
            pass

    return text

def percentages(resume_model,result):
    list_percentages = []
    example_dict = {}
    for m,i in enumerate(resume_model):
        list_create = [resume_model[m],result]
        cv = TfidfVectorizer()
        tf_matrix = cv.fit_transform(list_create)
        matchPercentage = cosine_similarity(tf_matrix)[0][1] * 100
        matchPercentage = round(matchPercentage, 2)
        list_percentages.append(matchPercentage)
    return list_percentages

def percent_dataframe(Ordered_list_Resume,list_percentages):
    res = {}
    for key,value in sorted(zip(Ordered_list_Resume,list_percentages)):
        res[key] = value

    my_keys = sorted(res.items(), key=itemgetter(1), reverse=True)[:5]
    key_dict = dict(my_keys)
    df = pd.DataFrame(key_dict.items(),columns = ["Resumes","Score"])
    return df
    
#code
#st.subheader("Files Uploader")
# def file_uploader():
if "authenticated" not in st.session_state:
    st.warning("Please login first")

elif "authenticated" in st.session_state and st.button("Logout"):
    st.warning("Your session is logged out, Login to proceed!")

else:
    if st.session_state['authenticated']:
        st.header("Resume Screening")
        jd_file = st.file_uploader("Give one file for JD",type = ['pdf',"PDF",'docx','doc'],key="jd_file")
        resume_files = st.file_uploader("Resume folder",type = ['pdf','doc','docx'],key="resume_file",accept_multiple_files=True)
        if st.button("Done"):
            st.write("Loading...")
            if (resume_files is not None) and (jd_file is not None):
                #file_details = {"Filename":jd_file.name,"FileType":jd_file.type,"FileSize":jd_file.size}
                #st.write(file_details)
                resume_all_files = concat_all_files(resume_files)
                resume_parser_files = parser(resume_all_files)
                job_desc_parser_files = jb_parser([jd_file])
                job_desc_preprocess = apply_nltk(job_desc_parser_files)
                resume_preprocess = apply_nltk(resume_parser_files)
                resume_model = fine_tune_model(resume_preprocess,model,tokenizer)
                test = job_desc_preprocess[0]
                tttt = str(test)
                result = job_desc_model(tttt,model,tokenizer)
                list_percent = percentages(resume_model,result)
                #print(list_percent)
                df = percent_dataframe(Ordered_list_Resume,list_percent)
                st.write("Score out of 10")
                st.dataframe(df)

            elif (resume_files is None) and (jd_file is not None):
                st.warning("You need to upload your resumes")

            elif (resume_files is not None) and (jd_file is None):
                st.warning("Please give job description")

            else:
                st.warning("please give both resume and jd")




