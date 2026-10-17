import io
import json
import re
import ollama

MODEL = "qwen2.5vl:3b"  # use the exact name from `ollama list`

PROMPT = """Look at this receipt image and extract the data.
Reply with ONLY a JSON object, no other text, like this:
{"store": "Store Name", "date": "MM/DD/YYYY", "total": 12.34, "category": "Groceries"}

Rules:
- "total" is the final amount paid as a number, not the subtotal
- "category" must be one of: Groceries, Food, Travel, Shopping, Health, Other"""

ALLOWED = ["Groceries", "Food", "Travel", "Shopping", "Health", "Other"]


def ask_model(image_bytes, temperature):
    response = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT, "images": [image_bytes]}],
        options={
            "temperature": temperature,
            "repeat_penalty": 1.15,
            "num_predict": 150,
        },
    )
    return response["message"]["content"]


def read_receipt(image):
    image = image.convert("RGB")
    image.thumbnail((1024, 1024))
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    image_bytes = buf.getvalue()

    data = None
    raw = ""
    for temp in (0.2, 0.5, 0.8):
        try:
            raw = ask_model(image_bytes, temp)
        except ollama.ResponseError as e:
            print(f"Attempt at temperature {temp} failed: {e}")
            continue
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
                break
            except json.JSONDecodeError:
                continue

    if data is None:
        raise ValueError("Model could not read this receipt. Last reply: " + raw[:200])

    try:
        data["total"] = float(str(data.get("total", 0)).replace("$", "").replace(",", ""))
    except (ValueError, TypeError):
        data["total"] = 0.0

    if data.get("category") not in ALLOWED:
        data["category"] = "Other"

    return data