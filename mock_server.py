from flask import Flask, jsonify
import pandas as pd
import random
import time

app = Flask(__name__)

# 웹/앱서비스 기획, 경력직, 정규직 테스트 데이터 생성
def generate_web_app_planning_data(count_per_page=20, pages=5):
    companies = [
        "채용기업1","채용기업2","채용기업3","채용기업4","채용기업5","채용기업6","채용기업7","채용기업8","채용기업9","채용기업10"
        "채용기업11","채용기업12","채용기업13","채용기업14","채용기업15","채용기업16","채용기업17","채용기업18","채용기업19","채용기업20"
        "채용기업21","채용기업22","채용기업23","채용기업24","채용기업25","채용기업26","채용기업27","채용기업28","채용기업29","채용기업30"
    ]
    
    job_titles = [
        "서비스 기획자", "UX/UI 기획자", "웹서비스 기획자", "앱서비스 기획자", "프로덕트 매니저(PM)", 
        "서비스 운영 기획자", "콘텐츠 기획자", "플랫폼 기획자", "그로스 해커", "비즈니스 기획자",
        "UI/UX 디자이너", "서비스 디자이너", "프로젝트 매니저", "웹/앱 기획자", "디지털 프로덕트 기획자"
    ]
    
    industries = [
        "IT/웹/통신", "서비스업", "소프트웨어", "쇼핑몰/오픈마켓", "포털/컨텐츠", "게임", "금융/핀테크", 
        "미디어/광고", "교육", "여행/숙박/항공", "O2O 서비스", "SNS/블로그", "헬스케어/의료", "부동산/임대", 
        "물류/유통", "이커머스", "엔터테인먼트", "모빌리티", "푸드테크", "보안/암호화"
    ]
    
    locations = [
        "서울 강남구", "서울 서초구", "서울 마포구", "서울 영등포구", "서울 송파구", "서울 성동구", 
        "서울 용산구", "서울 중구", "서울 종로구", "서울 강서구", "서울 광진구", "서울 동작구",
        "경기 성남시 분당구", "경기 성남시 판교", "경기 성남시 수정구", "경기 성남시 중원구"
    ]
    
    experience_levels = ["경력 3~5년", "경력 5~7년", "경력 7~10년", "경력 10년 이상", "경력무관"]
    
    all_jobs = []
    for page in range(1, pages+1):
        for _ in range(count_per_page):
            company = random.choice(companies)
            job_title = random.choice(job_titles)
            industry = random.choice(industries)
            location = random.choice(locations)
            experience = random.choice(experience_levels[:4])  # 경력직만 선택
            
            # 채용정보 제목 생성
            title = f"[{company}] {job_title} {experience} 채용 (직원수 {random.randint(10, 100)}명)"
            
            # 직원수 생성 (100명 이하 중소기업)
            employee_count = random.randint(10, 100)
            
            job = {
                "회사명": company,
                "채용정보 제목": title,
                "직무": "웹/앱서비스 기획",
                "고용형태": "정규직",
                "경력": experience,
                "근무지역": location,
                "산업(업종)": industry,
                "직원수": f"{employee_count}명",
                "기업규모": "중소기업",
                "설립년도": f"{random.randint(2010, 2024)}년",
                "등록일": time.strftime("%Y-%m-%d", time.localtime(time.time() - random.randint(0, 14) * 86400)),
                "마감일": time.strftime("%Y-%m-%d", time.localtime(time.time() + random.randint(7, 30) * 86400)),
                "페이지": page
            }
            all_jobs.append(job)
    
    return all_jobs

# 테스트 데이터를 CSV로 저장
def save_to_csv(data, filename="job_site_web_app_planning.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    return f"{len(data)}개의 데이터가 {filename}에 저장되었습니다."

# API 엔드포인트: 모든 채용 정보 조회
@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    jobs = generate_web_app_planning_data(pages=3)
    return jsonify(jobs)

# API 엔드포인트: CSV 파일 생성
@app.route('/api/generate-csv', methods=['GET'])
def generate_csv():
    jobs = generate_web_app_planning_data(pages=3)
    result = save_to_csv(jobs)
    return jsonify({"message": result})

# API 엔드포인트: 특정 페이지의 채용 정보 조회
@app.route('/api/jobs/page/<int:page>', methods=['GET'])
def get_jobs_by_page(page):
    all_jobs = generate_web_app_planning_data(pages=3)
    page_jobs = [job for job in all_jobs if job['페이지'] == page]
    return jsonify(page_jobs)

# 메인 페이지
@app.route('/')
def index():
    return """
    <html>
        <head>
            <title>job_site 웹/앱서비스 기획 채용정보</title>
            <style>
                body { font-family: 'Malgun Gothic', Arial, sans-serif; margin: 0; padding: 20px; line-height: 1.6; }
                .container { max-width: 1000px; margin: 0 auto; }
                h1 { color: #333; }
                h2 { color: #555; margin-top: 30px; }
                .btn { display: inline-block; background: #4CAF50; color: white; padding: 10px 15px; text-decoration: none; border-radius: 4px; margin-right: 10px; }
                .btn:hover { background: #45a049; }
                pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
                .page-btns { margin: 20px 0; }
                .page-btn { display: inline-block; background: #f0f0f0; color: #333; padding: 8px 12px; text-decoration: none; border-radius: 4px; margin-right: 5px; }
                .page-btn:hover, .page-btn.active { background: #007bff; color: white; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
                th { background-color: #f2f2f2; }
                tr:hover { background-color: #f5f5f5; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>채용정보 웹/앱서비스 기획 채용정보</h1>
                <p>웹/앱서비스 기획, 경력직, 정규직 채용정보를 제공하는 테스트 서버입니다.</p>
                
                <h2>사용 가능한 API 엔드포인트:</h2>
                <ul>
                    <li><a href="/api/jobs">/api/jobs</a> - 모든 채용 정보 조회 (JSON)</li>
                    <li><a href="/api/jobs/page/1">/api/jobs/page/1</a> - 1페이지 채용 정보 조회 (JSON)</li>
                    <li><a href="/api/generate-csv">/api/generate-csv</a> - CSV 파일 생성</li>
                </ul>
                
                <h2>CSV 파일 생성하기:</h2>
                <a href="/api/generate-csv" class="btn">CSV 파일 생성</a>
                
                <h2>채용정보 페이지 보기:</h2>
                <div class="page-btns">
                    <a href="#" class="page-btn active" data-page="1">1</a>
                    <a href="#" class="page-btn" data-page="2">2</a>
                    <a href="#" class="page-btn" data-page="3">3</a>
                </div>
                
                <table id="jobs-table">
                    <thead>
                        <tr>
                            <th>채용정보 제목</th>
                            <th>회사명</th>
                            <th>산업(업종)</th>
                            <th>경력</th>
                            <th>근무지역</th>
                            <th>등록일</th>
                            <th>마감일</th>
                        </tr>
                    </thead>
                    <tbody id="jobs-data">
                        <tr><td colspan="7">로딩 중...</td></tr>
                    </tbody>
                </table>
                
                <script>
                    // 페이지 로드 시 1페이지 데이터 표시
                    document.addEventListener('DOMContentLoaded', () => {
                        loadPageData(1);
                        
                        // 페이지 버튼 클릭 이벤트 처리
                        document.querySelectorAll('.page-btn').forEach(btn => {
                            btn.addEventListener('click', (e) => {
                                e.preventDefault();
                                const page = parseInt(e.target.dataset.page);
                                loadPageData(page);
                                
                                // 활성 페이지 버튼 스타일 변경
                                document.querySelectorAll('.page-btn').forEach(b => {
                                    b.classList.remove('active');
                                });
                                e.target.classList.add('active');
                            });
                        });
                    });
                    
                    // 페이지별 데이터 로드 함수
                    function loadPageData(page) {
                        fetch(`/api/jobs/page/${page}`)
                            .then(response => response.json())
                            .then(data => {
                                const tableBody = document.getElementById('jobs-data');
                                tableBody.innerHTML = '';
                                
                                data.forEach(job => {
                                    const row = document.createElement('tr');
                                    row.innerHTML = `
                                        <td>${job['채용정보 제목']}</td>
                                        <td>${job['회사명']}</td>
                                        <td>${job['산업(업종)']}</td>
                                        <td>${job['경력']}</td>
                                        <td>${job['근무지역']}</td>
                                        <td>${job['등록일']}</td>
                                        <td>${job['마감일']}</td>
                                    `;
                                    tableBody.appendChild(row);
                                });
                            });
                    }
                </script>
            </div>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5000)
