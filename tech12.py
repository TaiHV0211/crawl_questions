import os
from bs4 import BeautifulSoup
import requests
import csv

url = 'https://tech12h.com/cong-nghe/trac-nghiem-tin-hoc-10-ket-noi-tri-thuc.html'
req = requests.get(url)
soup = BeautifulSoup(req.text, "lxml")
link_urls = []
questions= []
answers= []
correct_answers=[]
titles = []
link_to_url = soup.find_all("a")

for link in link_to_url:
    if link.get('href')[:48] == '/bai-hoc/trac-nghiem-tin-hoc-10-ket-noi-tri-thuc':
        link_url = 'https://tech12h.com' + link.get('href').replace('../', '')
        link_urls.append(link_url)
    elif link.get('href')[:67] == 'https://tech12h.com/bai-hoc/trac-nghiem-tin-hoc-10-ket-noi-tri-thuc': 
        link_urls.append(link.get('href'))
csv_filename = 'tinhoc_10.csv'
for url in link_urls:
    request_url = requests.get(url)
    soup = BeautifulSoup(request_url.text, "lxml")
    title = soup.select_one('body > main > div > div > div > div.col-lg-9.order-lg-last.col-main > div.block-content > div.heading-primary > h1 > span')
    accordion = soup.find('div', {'id': 'accordionExample'})

    if accordion:
        questions_and_answers = []
        elements = accordion.find_all(['p', 'ul'])
        
        # Mảng tạm để lưu trữ các phần tử 'p'
        temp_paragraphs = []
        
        for element in elements:
            if element.name == 'p':
                # Nếu gặp phần tử 'p', kiểm tra xem mảng tạm có dữ liệu không
                # Nếu có, lưu nó vào mảng chính và làm sạch mảng tạm
                if temp_paragraphs:
                    questions_and_answers.append(temp_paragraphs)
                    temp_paragraphs = []
                temp_paragraphs.append(element.get_text(strip=True))
            elif element.name == 'ul':
                questions_and_answers.append(temp_paragraphs)
                temp_paragraphs = []
                # Nếu gặp phần tử 'ul', lấy danh sách câu trả lời và câu trả lời đúng
                answer_elements = element.find_all('li')
                answers = [answer.get_text(strip=True).replace('\xa0', '') for answer in answer_elements if answer.get_text(strip=True).startswith(('A.', 'B.', 'C.', 'D.'))]
                correct_answer = [answer.get_text(strip=True) for answer in answer_elements if answer.find('h6')]
                correct_answer = correct_answer[0] if correct_answer else None
                temp_paragraphs.append({"answers": answers, "correct_answer": correct_answer})
        
        # Kiểm tra xem mảng tạm còn dữ liệu không và thêm vào mảng chính
        if temp_paragraphs:
            questions_and_answers.append(temp_paragraphs)
        questions_responses = []
        result = ''
        # In ra kết quả
        for item in questions_and_answers:   
            for element in item:
                if isinstance(element, dict):
                    questions_responses.append(result)
                    result = ''
                else:
                    result = result + element + " "

        file_exists = os.path.isfile(csv_filename)

        with open(csv_filename, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Viết tiêu đề cho các cột
            if not file_exists:
                writer.writerow(['Title', 'url','Câu hỏi', 'Câu trả lời', 'Câu trả lời đúng'])

            # Lặp qua danh sách các tiêu đề và danh sách câu hỏi và câu trả lời tương ứng

            # questions_and_answers = questions_responses[i]
            for question_responses in questions_responses:
                question = question_responses
                for item in questions_and_answers:
                    if isinstance(item[0], dict):
                        answers = item[0]["answers"]
                        correct_answer = item[0]["correct_answer"]
                answers_correct = []
                answers_correct.append(correct_answer)
                writer.writerow([title.get_text(strip=True),url,question, answers, answers_correct])
    else:
        print("Không tìm thấy phần tử 'accordionExample'")