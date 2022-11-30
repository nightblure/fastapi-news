import requests

def test():

    TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNCIsImF1ZCI6WyJmYXN0YXBpLXVzZXJzOmF1dGgiXSwiZXhwIjoxNjY5ODM4ODM0fQ.Z6FuZ46A5JBt4I9XWpfzDHriz6_GMlS4qp7V6d8Agys'
    headers = {
        'Content-Type': 'application/json',
        "Authorization": f'Bearer {TOKEN}'
    }
    result = requests.get(url='http://127.0.0.1:8000/users/me', headers=headers)
    print(result)


test()