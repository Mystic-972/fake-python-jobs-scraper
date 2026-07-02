import csv
import requests
from bs4 import BeautifulSoup

def main():
    url = "https://realpython.github.io/fake-jobs/"
    print(f"Mengambil data dari: {url}...")
    
    # Mengirim HTTP request ke website
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Gagal mengambil halaman web. Status code: {response.status_code}")
        return
        
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Mencari container postingan pekerjaan
    results = soup.find(id="ResultsContainer")
    if not results:
        print("Konten pekerjaan tidak ditemukan.")
        return
        
    job_elements = results.find_all("div", class_="card-content")
    print(f"Ditemukan {len(job_elements)} lowongan pekerjaan.")
    
    csv_file_path = "jobs.csv"
    with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Company", "Location", "Detail URL"])
        
        # Loop untuk mengambil info detail setiap pekerjaan
        for job_element in job_elements:
            title_element = job_element.find("h2", class_="title")
            company_element = job_element.find("h3", class_="company")
            location_element = job_element.find("p", class_="location")
            
            # card_content berada di dalam card. Link-link ada di card-footer
            card_element = job_element.find_parent("div", class_="card")
            apply_link = ""
            if card_element:
                links = card_element.find_all("a", class_="card-footer-item")
                # Mengambil link kedua 
                if len(links) >= 2:
                    apply_link = links[1]["href"]
            
            title = title_element.text.strip() if title_element else ""
            company = company_element.text.strip() if company_element else ""
            location = location_element.text.strip() if location_element else ""
            
            writer.writerow([title, company, location, apply_link])
            
    print(f"Data pekerjaan berhasil disimpan ke file: {csv_file_path}")

if __name__ == "__main__":
    main()
