## User
### Token取得(一般ユーザー)
```
curl -k -X POST http://127.0.0.1:8000/api/user/token/ ^
-H "Content-Type: application/json" ^
-d "{\"email\": \"bunsekiya@test.com\", \"password\": \"bunbun343\"}"
```
### Token取得(ビルダー)
```
curl -k -X POST http://127.0.0.1:8000/api/user/token/ ^
-H "Content-Type: application/json" ^
-d "{\"email\": \"api-user@test.com\", \"password\": \"bunbun343\"}"
```

## 会社概要
## 取得
```
curl -k http://127.0.0.1:8000/api/company_info/ ^
-H "UserID: 4f1219ad-d381-470c-a1b2-b2cc983893be" ^
-H "Authorization: Bearer 
```

## 更新
```
curl -X PUT "http://127.0.0.1:8000/api/company_info/" ^
-H "UserID: 4f1219ad-d381-470c-a1b2-b2cc983893be" ^
-H "Content-Type: application/json" ^
-H "Authorization: Bearer " ^
-d "{\"foundation_date\": \"2024-09-26\", \"post_code\": \"2147483\"}"

```
## 定数
### 従業員数

```
curl -k "http://127.0.0.1:8000/api/employee_size/" ^
-H "UserID: 8de9ea9f-2e1e-40ed-8b65-588a2ba20a61" ^
-H "Authorization: Bearer "

```
