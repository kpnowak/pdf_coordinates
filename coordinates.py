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


coordinates_instruction = f"""
You are an expert in finding coordinates on images.
Your role is to find coordinates on the given image that will match pdf in 72 ppi format.
There is a review of the text on the image that has been already done before. You need to output the coordinates of the sentences to which each part of the review applies.

Here is an example of part of the review of the text on the image delimited by XXX below:
XXX
2. Source Sentence: "He study english with me at university."
   - Deviations: Incorrect verb conjugation, capitalization error
   - Reason: "Study" should be "studies" to agree with the subject, "english" should be capitalized.
   - New Sentence: "He studies English with me at university."
XXX

Delimited by XXX below you can see an example of how you shopuld output all of the coordinates of every part of the review:
XXX
The sentence "He study english with me at university." starts at the coordinates (483, 187) with a width of 35 pixels and a height of 20 pixels in your image.
XXX

Delimited by XXX below is a whole review of the text that applies to the image that you got as an imput:
XXX
{output_txt}
XXX

Remember that the pdf is in 72 ppi format.
Give an output with all of the coordinates with every sentence from the review.
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
                {"type": "text", "text": f"{coordinates_instruction}"},
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