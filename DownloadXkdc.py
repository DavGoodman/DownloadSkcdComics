# ! python3
# downloadXkcd.py - Downloads every single XKCD comic.
import requests, os, bs4

url = 'https://xkcd.com'
os.makedirs("xkcd", exist_ok=True)  # exist_ok=True prevents from throwing exception if folder already exists
while not url.endswith("#"):
    print("Downloading page %s..." % url)
    res = requests.get(url)
    res.raise_for_status()

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    comic_elem = soup.select("#comic img")
    if comic_elem == []:
        print("could not find comic image.")
    else:
        comic_url = "https:" + comic_elem[0].get("src")

        # Download image
        print("downloading image %s..." % (comic_url))
        res = requests.get(comic_url)
        res.raise_for_status()

        image_file = open(os.path.join("xkcd", os.path.basename(comic_url)), "wb")
        for chunk in res.iter_content(100000):
            image_file.write(chunk)
        image_file.close()

    prev_link = soup.select('a[rel="prev"]')[0]
    url = 'https://xkcd.com' + prev_link.get('href')
print("done")