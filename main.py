# from bs4 import BeautifulSoup
# import requests

# url = 'https://vietjack.com/giai-bai-tap-tin-hoc-11/cau-hoi-trac-nghiem-tin-hoc-lop-11-co-dap-an.jsp'
# req = requests.get(url)
# soup = BeautifulSoup(req.text, "lxml")
# link_urls = []
# questions= []
# answers= []
# correct_answers=[]
# link_to_url = soup.find_all("a")

# for link in link_to_url:
#     if link.get('href')[:26] == '../giai-bai-tap-tin-hoc-11':
#         link_url = 'https://vietjack.com/' + link.get('href').replace('../', '')
#         link_urls.append(link_url)
# print (len(link_urls),'====== link_urls')
# for url in link_urls:
#     request_url = requests.get(url)
#     soup = BeautifulSoup(request_url.text, "lxml")
#     middle_col_div = soup.select_one('body > div.main > div.container > div > div.row > div > div.col-md-7.middle-col')
    
#     if middle_col_div:
#         p_elements = middle_col_div.find_all('p')
        
#         # Process and collect the content of the <p> elements
#         question = None
#         answer_choices = []
#         correct_answer = None
        
#         for p in p_elements:
#             text = p.get_text(strip=True)
#             if text.startswith('Câu '):
#                 if question is not None:
#                     # Store the previous question and its answer choices
#                     questions.append(question)
#                     answers.append(answer_choices)
#                     correct_answers.append(correct_answer)
#                     question = None
#                 question = text  # Store the question
#                 answer_choices = []  # Reset answer choices for the new question
#             elif text.startswith(('A.', 'B.', 'C.', 'D.')):
#                 answer_choices.append(text)  # Store answer choices
#             elif text.startswith('Đáp án:') or text.startswith('Đáp án đúng là: ') :
#                 correct_answer = text # Store the correct answer
# print(len(questions), '==== questions')
# print(len(answers), '==== answers')
# print(len(correct_answers), '==== correct_answers')

# # for x, y, z in zip(questions, answers, correct_answers):
# #     print('================================================================')
# #     print('Câu hỏi:', x)
# #     for t in y:
# #         print('Câu trả lời:', t)
# #     print('Câu trả lời đúng:', z)