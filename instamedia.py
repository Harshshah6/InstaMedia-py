import argparse
import os
import time
import requests
from tqdm import tqdm


def get_arguments():
    parser = argparse.ArgumentParser(description="Simple Open Source Command Line / Script made by LEGENDARY STREAMER to save media like Reel / Post from instagram to locally without any water mark.\nGithub:- https://github.com/Harshshah6")

    parser.add_argument("-u", "--url", type=str, help="Url of an Instagram Post / Reel.")
    parser.add_argument("-o", "--out", type=str, help="File Name to Save as. (Optional)")

    return parser.parse_args() , parser

def main():
    args, parser = get_arguments()

    if( not args.url ):
        parser.print_help()  # Exit if there is no url passed
        exit()

    URL = args.url
    OUT = args.out if args.out else "-1"

    REQ_URL_TEMPLATE = "https://androsketchui.vercel.app/api/insta/{type}"

    if "www.instagram.com/reel/" in URL:
        REQ_URL = REQ_URL_TEMPLATE.format(type="reel")
    elif "www.instagram.com/p/" in URL:
        REQ_URL = REQ_URL_TEMPLATE.format(type="post")
    else:
        print("Invalid URL")
        exit()

    _param = {"url":URL, "secret":"privateLS"}
    response = requests.get(REQ_URL, params=_param).json()

    if not response.get("status") == "1":
        print("Error Parsing Url.")
        exit()

    DATA = response.get("data")  

    if type(DATA) == str:
        response = requests.get(DATA)
        if "content-disposition" in response.headers:
            content_disposition = response.headers["content-disposition"]
            filename = content_disposition.split("filename=")[1]
        else:
            filename = DATA.split("/")[-1]

        filename = filename[:filename.index(";")]

        filename = OUT if (not OUT == "-1") else filename 

        print("Downloading Reel ...")

        total_size = int(response.headers.get('content-length', 0))
        with open(filename, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    f.write(data)
                    pbar.update(len(data))
                    progress_percent = int(pbar.n / total_size * 100)
                    print(f"\rProgress: {progress_percent}%", end="\r")

        print(f"Downloaded file {filename}")
    
    elif type(DATA) == list:

        for item in DATA:
            response = requests.get(item)

            if response.headers["Content-Disposition"]:
               content_disposition = response.headers["Content-Disposition"]
               filename = content_disposition.split("filename=")[1]
            else:
                filename = "image_" + str(DATA.index(item)) + ".jpg"

            filename = OUT if (not OUT == "-1") else filename
            filename += str(DATA.index(item))

            print(f"Downloading Post ... {filename}")

            total_size = int(response.headers.get('content-length', 0))
            with open(filename, 'wb') as f:
                with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                    for data in response.iter_content(chunk_size=1024):
                        f.write(data)
                        pbar.update(len(data))
                        progress_percent = int(pbar.n / total_size * 100)
                        print(f"\rProgress: {progress_percent}%", end="\r")


            print(f"Downloaded file {filename}")
            print()
    else:
        print("An Unknown Error Occured")
        exit()

if __name__ == "__main__":
    # os.system('cls' if os.name=='nt' else 'clear') # Clear The Console Before Running The Script
    main() # Call Main Function
    print()