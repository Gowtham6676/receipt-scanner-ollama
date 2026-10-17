# Smart Receipt Scanner (Local AI)

Upload a photo of a receipt and a local vision model running in Ollama extracts the
store, date, total, and spending category. Results go into a table with a spending chart
and can be downloaded as CSV. Everything runs on your own computer, so receipts never leave your machine.

## Features
- Reads receipt images with a local Ollama vision model
- Returns structured data (store, date, total, category)
- Retry logic and validation for unreliable model output
- Spending-by-category chart and CSV export
- Streamlit web interface

## Tech stack
Python, Ollama (qwen2.5vl:3b), Streamlit, Pandas, Pillow

## Setup
1. Install Python 3.10+ and [Ollama](https://ollama.com)
2. Download a vision model: `ollama pull qwen2.5vl:3b`
3. Install the libraries:
```
   pip install -r requirements.txt
```
4. Run the app:
```
   streamlit run app.py
```

## Results
Tested on 5 sample receipts:

| Field | Correct |
|---|---|
| Store | X / 5 |
| Date | X / 5 |
| Total | X / 5 |

## Limitations
- Small vision models can misread blurry or crumpled receipts
- Category labels are guessed by the model and can be wrong
- Currency is not detected yet
- Needs Ollama running locally, so it can't be hosted on Streamlit Cloud

## Future improvements
- Editable results table to correct mistakes
- Currency detection and monthly summaries
- Comparison with other models