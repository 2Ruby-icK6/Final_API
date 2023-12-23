# Rovick Pasamonte - Final Project on CS Elective

## CRUD - JSON Type
 - Create (Insert data)
 - Read (View Data)
 - Update (Edit Data)
 - Delete (Delete Data)

## Security - JWT (JSON WEB Token)
 - Username = [Your Surname]
 - Password = {'123456'}

### Login First
 - To Secure API Endpoints if user does not login

### Format Default 
 - JSON Type

### URLs
 - [POST] http://127.0.0.1:5000/ # login page
 - [GET] http://127.0.0.1:5000/client # Client Table page (JSON)
 - [GET] http://127.0.0.1:5000/client/{id} # input your id in {id} 
 - [GET] http://127.0.0.1:5000/client/{id}?format=json # to see formatted to JSON
 - [GET] http://127.0.0.1:5000/client/search?criteria={Search} # search
 - [PUT] http://127.0.0.1:5000/client/{id} # To edit
 - [DELETE] http://127.0.0.1:5000/client/{id} # To delete