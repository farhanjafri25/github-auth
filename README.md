# GITHUB code Crawler using Treesitter

Welcome to the Python Codebase Crawler and Analyzer project! This tool leverages the power of Tree-sitter to parse and analyze Python codebases retrieved from GitHub repositories. By crawling these repositories, the tool extracts valuable metadata about the code, such as class and function definitions, and stores this information in a PostGres Database for further analysis.

## Features
- Tree-sitter Integration: Utilizes Tree-sitter's efficient and accurate parsing capabilities to understand and analyze Python codebases.
- GitHub Integration: Fetches and clones Python repositories from GitHub using provided URLs, allowing for easy analysis of open-source projects.
- Metadata Extraction: Identifies and extracts key components of the code, including classes, functions, and their attributes, and stores them in a structured format.
- Database Storage: Saves the extracted metadata into a relational database for easy querying and analysis.
- Error Handling and Validation: Implements robust error handling and validation mechanisms to ensure the accuracy and integrity of the data.

## Tech Stack used
Python
FastAPI
Postgres
Firebase


## Requirements
FastAPI
uvicorn
tree-sitter
firebase
pyrebase
pydantic
psycopg2-binary
python-dotenv

## How to use

1. Clone the repository to your local 

    ```shell
    git clone git@github.com:farhanjafri25/github-auth.git

2. Install the requirements 

    ```shell
    pip install -r requirements.txt

3. Run the app server

    ```shell
    uvicorn main:app --reload 

## Schema Design
1. File Table (file)
 - id - PK
 - file_name
 - repo_id

2. Classes Table (classes)
 - id - PK
 - class_name
 - file_id - fk

3. Functions Table (function)
 - id - PK
 - function_id - unique
 - function_name
 - file_id - FK
 - function_body 
 - class_id - FK



## API's List

    ```shell
    @Post /signup
    @Post /login
    @Post /repo
    @Get  /fetch-code
    @Get  /list-functions
    ```

    

## API's list and response 

1. Signup API
- This API sign's up a user, I am using firebase email, password authentication method for signing up
- Below is a Screen shot and response body for signup

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/signup-successful.png?raw=true)

- Below is the case for unsuccessful Signup

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/signup-unsuccessful.png?raw=true)

2. Login API
- This API is to log in a user using firebase authentication and get the bearer token
- API response for the login API

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/user-login.png?raw=true)

3. Repo API
- To Clone a repo, crawl and store the data in a PostGres Database
- API response and DB stored response for the same

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/save-gitrepo.png?raw=true)

- File Schema record
    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/file-table.png?raw=true)

- Class schema Record

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/class-table.png?raw=true)


- Functions Schema Record

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/function-table.png?raw=true)
    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/functions-table.png?raw=true)


    

4. Fetch functions list API
- To fetch all the function names and identifiers using pagination

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/list-functions.png?raw=true)

5. Fetch Code API
- To fetch the code block for the function identifier

    ![alt text](https://github.com/farhanjafri25/github-auth/blob/master/fetch-code.png?raw=true)


## Assumptions

I am crawling only Python codebases and the code outside of function scope are not covered in the project as not mentioned per the criteria.

