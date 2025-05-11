import requests
from bs4 import BeautifulSoup

# 기본 URL 및 헤더 설정
BASE_URL = "https://www.job_site.co.kr"
SEARCH_URL = "https://www.job_site.co.kr/recruit/joblist?jobtype=I000"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def check_page_structure():
    url = f"{SEARCH_URL}&page=1"
    print(f"요청 URL: {url}")
    
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()  # 응답 상태 확인
        
        print(f"응답 상태 코드: {res.status_code}")
        
        # HTML 파싱
        soup = BeautifulSoup(res.text, "html.parser")
        
        # 페이지 타이틀 확인
        print(f"페이지 타이틀: {soup.title.text}")
        
        # 주요 컨테이너 확인
        print("\n=== 주요 컨테이너 확인 ===")
        main_containers = soup.select("div.recruit-info")
        print(f"div.recruit-info 요소 수: {len(main_containers)}")
        
        # 다른 가능한 컨테이너 확인
        containers = [
            ".list-default", ".list-post", ".list-grid", 
            ".joodJobList", ".jobList", ".devthink-list", 
            ".recruit-list", ".list-recruit"
        ]
        
        print("\n=== 가능한 컨테이너 확인 ===")
        for container in containers:
            elements = soup.select(container)
            print(f"{container} 요소 수: {len(elements)}")
        
        # 채용 공고 링크 확인 (다양한 선택자 시도)
        print("\n=== 채용 공고 링크 확인 ===")
        selectors = [
            ".list-default .title > a", 
            ".list-default .post-list-info > a",
            ".jobList .title > a", 
            ".jobList a.title", 
            ".recruit-list .title > a",
            ".recruit-list a.title",
            ".list-post .title > a",
            ".list-post a.title",
            "a.title",
            ".title > a",
            ".jobsearch-result .title > a",
            ".job-list .title > a"
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            print(f"{selector} 요소 수: {len(links)}")
            if links:
                print(f"첫 번째 링크: {links[0].get('href')}")
                print(f"링크 텍스트: {links[0].text.strip()}")
        
        # 페이지 구조 탐색
        print("\n=== 페이지 구조 탐색 ===")
        # 모든 <a> 태그 중 href 속성이 /Recruit/GI_Read/ 패턴을 포함하는 것 찾기
        job_links = []
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href", "")
            if "/Recruit/GI_Read/" in href:
                job_links.append(a_tag)
        
        print(f"채용 공고 링크로 추정되는 <a> 태그 수: {len(job_links)}")
        if job_links:
            for i, link in enumerate(job_links[:5]):  # 처음 5개만 출력
                print(f"{i+1}. href: {link.get('href')}")
                print(f"   텍스트: {link.text.strip()}")
                print(f"   부모 태그: {link.parent.name}")
                print(f"   부모 클래스: {link.parent.get('class')}")
                print("---")
        
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_page_structure()
