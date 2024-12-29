import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

#threads to allocate to downloading
threads = (12)

def download_map(route_number):
    base_url = "https://www.octranspo.com/images/files/files/routes_pdf_future/RD_Map_"
    route_number_str = str(route_number).zfill(3)
    url = base_url + route_number_str + "_(Jan2024).pdf"
    response = requests.get(url)
    if response.status_code == 404 or "Page not found" in response.text:
        print(f"No map for route {route_number_str}")
        return
    if "Content-Type" in response.headers and response.headers["Content-Type"] == "application/pdf":
        with open(f"RD_Map_{route_number_str}.pdf", "wb") as f:
            f.write(response.content)
        print(f"Downloaded map for route {route_number_str}")

def download_maps():
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(download_map, route_number) for route_number in range(1, 304)]
        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    download_maps()