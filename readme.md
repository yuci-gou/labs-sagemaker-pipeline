```
python3 -m venv .venv
source .venv/bin/activate
pip install boto3 sagemaker

python3 data-preprocess.py
python3 update_pipeline.py
```
