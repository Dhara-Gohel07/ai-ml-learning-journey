import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
STOP_WORDS = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    words = [w for w in text.split() if w not in STOP_WORDS]
    return " ".join(words)

def preprocess_dataframe(df, text_col="post"):
    df["clean"] = df[text_col].apply(clean_text)
    return df
