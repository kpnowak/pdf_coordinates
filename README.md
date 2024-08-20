# pdf_coordinates

An algorithm that finds the coordinates of sentences that are commented on by the review algorithm and then places these comments in an appropriate position in a pdf file.

**Files explanation**

Find mistakes 1.pdf - input plain pdf with text that does not contain any comments

Find_mistakes_1.jpg - not useful, pdf in jpg

**comments.py** - Algorithm that takes all of the coordinates and text produced by coordinates.py and place comments in the pdf file. Then new pdf is saved as output_highlighted.pdf

**coordinates.py** - Algorithm that finds coordinates of the first letter of the sentences that were reviewed by the review algorithm. Then it creates special txt file that contains all of the information for comments.py to highlight sentences and put all of the comments.

output_15_gram_jpg.txt - Contains a review of the pdf file made by the algorithm from Text-vs-jpg---OpenAI-comparison repository - It is one of many created reviews.

**output_highlighted.pdf - final pdf that contains all of the comments and highlights**

result.txt - coordinates with source sentences created by coordinates.py

separate_output.txt - Special file prepared for comments.py by coordinates.py to place all of the comments and highlights

Uses OpenAI API gpt-4o
