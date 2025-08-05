# data collection
import requests as re
import os
import time
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings

# unstructured to structured
from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe
from concurrent.futures import ThreadPoolExecutor, as_completed

disable_warnings(InsecureRequestWarning)

# Step 1: csv to dataframe
URL_file_name = "tranco_list.csv"
data_frame = pd.read_csv(URL_file_name)

# retrieve only "url" column and convert it to a list
URL_list = data_frame['url'].to_list()

# restrict the URL count
begin = 35000
end = 40000
collection_list = URL_list[begin:end]

# only for the legitimate
# Example: if you're scraping legit data from "tranco_list.csv"
collection_list = ["http://" + url for url in collection_list]

start = float((time.time()) / 60)

def process_url(url):
    try:
        response = re.get(url, verify=False, timeout=4)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            vector = fe.create_vector(soup)
            vector.append(str(url))
            return vector
        else:
            print("HTTP error:", response.status_code, url)
            return None
    except Exception as e:
        print("Error:", e, url)
        return None

def create_structured_data_multithreaded(url_list, max_threads=30):
    data_list = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(process_url, url): url for url in url_list}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            if result:
                data_list.append(result)
    return data_list

data = create_structured_data_multithreaded(collection_list, max_threads=30)

columns = [
    'has_title',
    'has_input',
    'has_button',
    'has_image',
    'has_submit',
    'has_link',
    'has_password',
    'has_email_input',
    'has_hidden_element',
    'has_audio',
    'has_video',
    'number_of_inputs',
    'number_of_buttons',
    'number_of_images',
    'number_of_option',
    'number_of_list',
    'number_of_th',
    'number_of_tr',
    'number_of_href',
    'number_of_paragraph',
    'number_of_script',
    'length_of_title',
    'has_h1',
    'has_h2',
    'has_h3',
    'length_of_text',
    'number_of_clickable_button',
    'number_of_a',
    'number_of_img',
    'number_of_div',
    'number_of_figure',
    'has_footer',
    'has_form',
    'has_text_area',
    'has_iframe',
    'has_text_input',
    'number_of_meta',
    'has_nav',
    'has_object',
    'has_picture',
    'number_of_sources',
    'number_of_span',
    'number_of_table',
    'URL'
]

df = pd.DataFrame(data=data, columns=columns)

# labelling
df['label'] = 0

df.to_csv("structured_data_legitimate.csv", mode='a', index=False, header=not os.path.exists("structured_data_legitimate.csv"))  # header should be false after the first run

end = float((time.time()) / 60)
print("Total time taken:", end - start)






















































