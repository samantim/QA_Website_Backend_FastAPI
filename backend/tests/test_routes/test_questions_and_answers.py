#There could be a lot of other test cases, but I tried to cover more controversial ones

from fastapi import status, File
from pathlib import Path

#create a new question
def test_create_question(client, general_auth_token_header):
    # form values will send as dict but with data parameter
    input = {"description" : "question 1 desc"}
    # for sending a uploadfile, we should open a file and read it in a variable
    file_path = Path(".")/"test_question_file.txt"
    with open(file_path.absolute(), "rb") as f:
        file_body = f.read()
    #this is the format of file parameter value which will send as files parameter
    input_file = {"attachment" : ("test_question_file.txt", file_body)}
    response = client.post("/questions", data = input, files = input_file, headers = general_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "question 1 desc"
    with open(Path(".")/"attachments"/"test_question_file.txt", "rb") as saved_file:
        saved_file_body = saved_file.read()
        assert file_body == saved_file_body

#get question id {1} which has been posted before
def test_get_question_by_id(client, general_auth_token_header):
    question_id = 1
    response = client.get(f"/questions/{question_id}", headers = general_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "question 1 desc"

#check getting a question with wrong id
def test_get_question_by_invalid_id(client, general_auth_token_header):
    question_id = 2
    response = client.get(f"/questions/{question_id}", headers = general_auth_token_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Question id {question_id} not found!"

#get all the question by admin
def test_get_all_questions_admin(client, admin_auth_token_header):
    response = client.get("/questions/get/all", headers = admin_auth_token_header)
    assert response.status_code == status.HTTP_200_OK

#post an answer for question id {1}
def test_create_answer(client, general_auth_token_header):
    # form values will send as dict but with data parameter
    input = {"description" : "answer 1 for question 1 desc",
             "question_id" : 1}
    # for sending a uploadfile, we should open a file and read it in a variable
    file_path = Path(".")/"test_answer_file.txt"
    with open(file_path.absolute(), "rb") as f:
        file_body = f.read()
    #this is the format of file parameter value which will send as files parameter
    input_file = {"attachment" : ("test_answer_file.txt", file_body)}
    response = client.post("/answers", data = input, files = input_file, headers = general_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["description"] == "answer 1 for question 1 desc"
    assert response.json()["question"] == "question 1 desc"
    with open(Path(".")/"attachments"/"test_answer_file.txt", "rb") as saved_file:
        saved_file_body = saved_file.read()
        assert file_body == saved_file_body

#get answers of question id {1}
def test_get_all_answers_of_question(client, admin_auth_token_header):
    question_id = 1
    response = client.get(f"/answers/get/all/{question_id}", headers = admin_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["description"] == "answer 1 for question 1 desc" 

#delete question id {1}
def test_delete_question_integrity_check(client, admin_auth_token_header):
    question_id = 1
    response = client.delete(f"/questions/delete/{question_id}", headers = admin_auth_token_header)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] =="No question to delete!"

#delete answer id {1}
def test_delete_answer(client, admin_auth_token_header):
    answer_id = 1
    response = client.delete(f"/answers/delete/{answer_id}", headers = admin_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] ==f"Answer id {answer_id} seccessfully deleted!"

#delete question id {1}
def test_delete_question(client, admin_auth_token_header):
    question_id = 1
    response = client.delete(f"/questions/delete/{question_id}", headers = admin_auth_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["msg"] ==f"Question id {question_id} seccessfully deleted!"
