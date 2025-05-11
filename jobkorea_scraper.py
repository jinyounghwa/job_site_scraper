import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.jobkorea.co.kr"
SEARCH_URL = "https://www.jobkorea.co.kr/recruit/joblist?jobtype=I000"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_job_links(page=1):
    url = f"{SEARCH_URL}&page={page}"
    print(f"요청 URL: {url}")
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = []
    job_tags = soup.select(".list-default .title > a")
    print(f"찾은 채용공고 수: {len(job_tags)}")
    for tag in job_tags:
        links.append(BASE_URL + tag["href"])
    return links

def parse_job_detail(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    def safe_text(selector):
        tag = soup.select_one(selector)
        return tag.get_text(strip=True) if tag else ""

    return {
        "회사명": safe_text(".co-name"),
        "직무명": safe_text(".recruit-title"),
        "산업분야": safe_text(".summary > li:nth-child(2)"),
        "주요업무": safe_text(".detail-content > div:nth-child(1)")
    }

def main():
    all_jobs = []
    for page in range(1, 3):  # 1~2페이지만
        print(f"크롤링 중: {page}페이지")
        links = get_job_links(page)
        print(f"수집된 링크 수: {len(links)}")
        
        for i, link in enumerate(links):
            try:
                print(f"[{i+1}/{len(links)}] 크롤링 중: {link}")
                job = parse_job_detail(link)
                print(f"수집된 정보: {job}")
                all_jobs.append(job)
                time.sleep(1)  # 서버 부하 방지
            except Exception as e:
                print(f"Error parsing {link}: {e}")

    print(f"총 수집된 채용정보 수: {len(all_jobs)}")
    if len(all_jobs) > 0:
        df = pd.DataFrame(all_jobs)
        print(f"DataFrame 생성 완료: {df.shape}")
        df.to_csv("jobkorea_it_jobs.csv", index=False, encoding="utf-8-sig")
        print("크롤링 완료! 결과는 jobkorea_it_jobs.csv 에 저장됨.")
    else:
        print("수집된 채용정보가 없습니다.")

if __name__ == "__main__":
    main()
