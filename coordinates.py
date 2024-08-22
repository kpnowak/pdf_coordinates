from openai import OpenAI, AzureOpenAI
import base64
import os



client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


with open('output_15_gram_jpg.txt', 'r', encoding='latin-1') as file:
    output_txt = file.read()


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = r"Find_mistakes_1.jpg"

# Getting the base64 string
base64_image = encode_image(image_path)

with open('output_15_gram_jpg.txt', 'r', encoding='latin-1') as file:
    input = file.read()


coordinates_instruction_1 = f"""
You are an expert in finding coordinates on images.
Your role is to find coordinates on the given image that will match pdf in 72 ppi format.
There is a review of the text on the image that has been already done before. You need to output the coordinates of 
the first letter of the sentences to which each part of the review applies. Remember that every first letter of the 
sentence is at different width and height of the page.

Here is an example of part of the review of the text on the image delimited by XXX below:
XXX
2. Source Sentence: "He study english with me at university."
   - Deviations: Incorrect verb conjugation, capitalization error
   - Reason: "Study" should be "studies" to agree with the subject, "english" should be capitalized.
   - New Sentence: "He studies English with me at university."
XXX

Delimited by XXX below you can see an example of how you shopuld output all of the coordinates of every part of the review:
XXX
The first letter of the sentence "He study english with me at university." is at the coordinates (54, 32).
XXX

Delimited by XXX below is a whole review of the text that applies to the image that you got as an imput:
XXX
{output_txt}
XXX

Remember that the pdf is in 72 ppi format.
The width of one page in pdf is 595 pts and the height is 842 pts
"""

coordinates_instruction_2 = f"""
You are an expert in finding coordinates on images.
Your role is to find coordinates on the given image that will match pdf in 72 ppi format.
There is a review of the text on the image that has been already done before. You need to output the coordinates of the first letter of the sentences to which each part of the review applies. Remember that every first letter of the sentence is at different width and height of the page.
For example, 1st sentence has its first letter "H" at the coordinates (45, 51). 2nd sentence has its first letter "I" at the coordinates (68, 51). 3rd sentence has its first letter "G" at the coordinates (78, 83).
You are not allowed to repeat coordinates. Every time, both x and y coordinates, need to be different, where (x, y).

Here is an example of part of the review of the text on the image delimited by XXX below:
XXX
2. Source Sentence: "He study english with me at university."
   - Deviations: Incorrect verb conjugation, capitalization error
   - Reason: "Study" should be "studies" to agree with the subject, "english" should be capitalized.
   - New Sentence: "He studies English with me at university."
XXX

Delimited by XXX below you can see an example of how you shopuld output all of the coordinates of every part of the review:
XXX
The first letter of the sentence "He study english with me at university." is at the coordinates (54, 32).
XXX

Delimited by XXX below is a whole review of the text that applies to the image that you got as an imput:
XXX
{output_txt}
XXX

Remember that the pdf is in 72 ppi format.
The width of one page in pdf is 595 pts and the height is 842 pts
"""

coordinates_instruction_3 = f"""
You are an expert in finding coordinates on images.
Your role is to find coordinates on the given image that will match pdf in 72 ppi format.
There is a review of the text on the image that has been already done before. You need to output the coordinates of the first letter of the sentences to which each part of the review applies. Remember that every first letter of the sentence is at different width and height of the page.
For easier allocation of coordinates create for yourself 3 columns in the pdf file, where if the first letter of the sentence is on the left side of the page, you will place coordinates in the left column. If first letter is in the middle, you will place coordinates in the middle column. If first letter is on the right side, you will place coordinates in the right column.
Start form the top of the page and use the technique described.

Here is an example of part of the review of the text on the image delimited by XXX below:
XXX
2. Source Sentence: "He study english with me at university."
   - Deviations: Incorrect verb conjugation, capitalization error
   - Reason: "Study" should be "studies" to agree with the subject, "english" should be capitalized.
   - New Sentence: "He studies English with me at university."
XXX

Delimited by XXX below you can see an example of how you shopuld output all of the coordinates of every part of the review:
XXX
The first letter of the sentence "He study english with me at university." is at the coordinates (54, 32).
XXX

Delimited by XXX below is a whole review of the text that applies to the image that you got as an imput:
XXX
{output_txt}
XXX

Remember that the pdf is in 72 ppi format.
The width of one page in pdf is 595 pts and the height is 842 pts
"""


separate_instructions = f"""
You are a helpful assistant that will change input to be perfectly organized for Python algorithm.

Here is an example of input delimited by XXX below:
XXX
1. The first letter of the sentence "He study english with me at university." is at the coordinates (54, 32).
XXX

Here is an example of how you should change it delimited by XXX below:
XXX
"Yesterday, I gone to a party with my friend David."(54, 32)Comment_content: 1. Source Sentence: "Yesterday, I gone to a party with my friend David." - Deviations: Incorrect verb tense - Reason: "Gone" is incorrect; the correct past tense should be "went." - New Sentence: "Yesterday, I went to a party with my friend David."
XXX
Do not write anything beside text delimited by XXX. Do not write XXX in output. Also don't add any additional spacing or enters between sentences. Always put new sentence in a new line.

Here is a whole comment_content that you need to use delimited by XXX below:
XXX
{input}
XXX
"""


def coordinates():
    url = f"data:image/jpeg;base64,{base64_image}"
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role":"assistant","content":"Your role is to find coordinates on the image."},
            {
            
            "role": "user",
            "content": [
                {"type": "text", "text": f"{coordinates_instruction_3}"},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
            
        ],
    )
    
    with open("result.txt", "w") as f:
        f.write(response.choices[0].message.content)
    
    return response.choices[0].message.content

def separate(output):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that prepare text for Python algorithm."},
            {"role": "user", "content": f"""{separate_instructions}
                                            Here is a whole input that you need to change delimited by XXX below
                                            XXX
                                            {output}
                                            XXX
             """},
        ]
    )
    with open("separate_output.txt", "w") as f:
        f.write(response.choices[0].message.content)

    

output = coordinates()
separate(output)