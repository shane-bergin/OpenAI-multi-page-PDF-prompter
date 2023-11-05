Keep all files in the same directory, including your intended PDF you wish to send along to OpenAI. The script will send a PDF of any page length to OpenAI API. You need only change the system and prompt text in quotes to make use of this. Also, the .pdf file name you intend to work with. 

Edit the prompt text:

![image](https://github.com/shane-bergin/OpenAI-multi-page-PDF-prompter/assets/75746016/bf2242c3-e350-4623-b884-383841f41318)


And line 37 with your .pdf's file name

![image](https://github.com/shane-bergin/OpenAI-multi-page-PDF-prompter/assets/75746016/4b895cc4-433f-4524-93a0-7d58fa4257c6)


make sure the .py script has rwx 

chmod 777 pdfprompt.py

Your OpenAI API key needs to be in the open_ai file, line 1 
