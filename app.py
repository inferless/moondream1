import os
os.environ["HF_HUB_ENABLE_HF_TRANSFER"]='1'
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, CodeGenTokenizerFast as Tokenizer
from PIL import Image
import urllib

class InferlessPythonModel:
    def initialize(self):
        model_id = "vikhyatk/moondream1"
        snapshot_download(repo_id=model_id,allow_patterns=["*.safetensors"])
        self.model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True).to("cuda")
        self.tokenizer = Tokenizer.from_pretrained(model_id)

    def download_image(self,image_url):
        file_name = f'image.{image_url.split(".")[-1]}'
        urllib.request.urlretrieve(image_url, file_name)
        return file_name

    def infer(self,inputs):
        image_url = inputs["image_url"]
        question = inputs["question"]
        file_name = self.download_image(image_url)
        image = Image.open(file_name)
        enc_image = self.model.encode_image(image)
        generated_text = self.model.answer_question(enc_image, question, self.tokenizer)
        return { "generated_answer" : generated_text }
        
    def finalize(self):
        self.pipe = None
