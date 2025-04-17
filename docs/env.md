# env

Packages

```bash
conda create -y -n mdagent python=3.10
source activate
conda activate mdagent

pip install uv
uv pip install -r requirements.txt
```

Data

```bash
mkdir -p data
```

MedQA: https://drive.google.com/file/d/1ImYUSLk9JbgHXOemfvyiDiirluZHPeQw/view

```bash
cd data
gdown --fuzzy 'https://drive.google.com/file/d/1ImYUSLk9JbgHXOemfvyiDiirluZHPeQw/view'  
unzip data_clean.zip 
cd -

mkdir -p data/medqa
cp data/data_clean/questions/US/test.jsonl data/medqa
cp data/data_clean/questions/US/train.jsonl data/medqa
```