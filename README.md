### Backend for BigBrother

#### Setup

```
conda create -n bigb python=3.8
conda activate bigb
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Heroku Deploy Command
```
heroku git:remote -a bigbbe
git push heroku main
```

## Todo deployment docs