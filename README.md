### Backend for BigBrother

#### Setup

```
conda create -n bigb python=3.8
pip install -r requirements.txt
uvicorn sql_app.main:app --reload
```

_Create User_
```

{
  "email": "mail@nivu.me",
  "full_name": "Nivu",
  "password": "root"
}
```