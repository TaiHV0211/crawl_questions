from bs4 import BeautifulSoup
import requests
import csv
titles = []
url = 'https://tech12h.com/bai-hoc/trac-nghiem-tin-hoc-10-ket-noi-tri-thuc-ki-i.html'
request_url = requests.get(url)
soup = BeautifulSoup(request_url.text, "lxml")
title = soup.select_one('body > main > div > div > div > div.col-lg-9.order-lg-last.col-main > div.block-content > div.heading-primary > h1 > span')
if title:
    title = title.get_text(strip=True)
    titles.append(title)
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
                print("Câu trả lời:", element["answers"])
                print("Câu trả lời đúng:", element["correct_answer"])
                questions_responses.append(result)
                result = ''
            else:
                result = result + element + " "
        print()
    for item in questions_responses:
        print(item)

    csv_filename = 'tinhoc_10.csv'
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Viết tiêu đề cho các cột
        writer.writerow(['Title', 'url','Câu hỏi', 'Câu trả lời', 'Câu trả lời đúng'])
        
        # Lặp qua danh sách các tiêu đề và danh sách câu hỏi và câu trả lời tương ứng
        for i in range(len(titles)):
            title = titles[i]
            # questions_and_answers = questions_responses[i]
            for question_responses in questions_responses:
                question = question_responses.strip('"')
                for item in questions_and_answers:
                    if isinstance(item[0], dict):
                        answers = item[0]["answers"]
                        correct_answer = item[0]["correct_answer"]
                answers_correct = []
                answers_correct.append(correct_answer)
                writer.writerow([title,url,question, answers, answers_correct])
else:
    print("Không tìm thấy phần tử 'accordionExample'")