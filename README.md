# 短網址
利用 Flask、Redis、MySQL
透過 RestFulAPI 的方式實現建立短網址、刪除、轉址的功能

# 部屬方式
1. 直接使用
   
   port預設為5000
   
   ```bash
   py ./app.py
   ```
   
3. Docker Compose
   
   透過docker-compose.yml的設定
   
   已經把flask從port 5000轉發到port 80上
   
   ```bash
   docker compose up
   ```
   

   
# Demo
1. Create
   
   curl -X POST -H "Content-type: application/json" -d '{"url":"https://www.facebook.com/","expireAt":"2024-08-30T09:20:41Z"}' 'http://localhost:port/api/v1/urls'
  ![image](https://github.com/s8900830/URL_Shortener_py_flask/blob/main/Image/create.png)
   
2. Redirect
   
   curl -L -X GET -i http://localhost:port/3Lr6vWrIL9xBblu
   ![image](https://github.com/s8900830/URL_Shortener_py_flask/blob/main/Image/redirect.png)
   
3. Delete
   
   curl -X DELETE -i http://localhost:port/api/v1/urls/3Lr6vWrIL9xBblu
   ![image](https://github.com/s8900830/URL_Shortener_py_flask/blob/main/Image/delete.png)
