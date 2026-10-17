from pathlib import Path
from PIL import Image
from ollama_reader import read_receipt

folder = Path(__file__).parent / "sample_images"

for file in sorted(folder.iterdir()):
    if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
        print("\n===", file.name, "===")
        print(read_receipt(Image.open(file)))