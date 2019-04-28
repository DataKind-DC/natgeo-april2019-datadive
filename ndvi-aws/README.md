# Steps to download Sentinel-2 data [WIP]

1) Install requirements (requires Python >= 3.6):

```bash
pip install -r requirements.txt
```

2) Fill out your credentials for the Copernicus Sentinel API in *.env* and run

```bash
source .env
```

(or otherwise get those credentials into your environment).


3) Generate list of Sentinel-2 image files:

```bash
python part1.py
```

4) TODO: Download each of the generated files and upload to AWS S3 bucket.

