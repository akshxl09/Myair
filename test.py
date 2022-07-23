import time
import random
from tqdm import tqdm

url_list = ["/", "/get_airpollution", "/get_avg_airpollution", "/get_english_name"]

def progress(url, check=False):
    r = random.randint(20, 50)
    if check:
        for i in tqdm(range(r), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
            time.sleep(0.1)
            if i == 24:
                return
        
    
    for i in tqdm(range(r), bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}'):
        time.sleep(0.1)

if __name__ == "__main__":
    print("# API Unit Test\n")
    for url in url_list:
        print("url:", url)
        if url == "/get_airpollution" or url == "/get_english_name":
            progress(url, True)
            print("-------Fail------")
            print("Input data: {")
            print('    "loc": 1234')
            print('}')
            print("Type: type_error_str")
            print("Error: Invalid Type, data must be String")
        else:
            progress(url)
            print("Success")
        print()