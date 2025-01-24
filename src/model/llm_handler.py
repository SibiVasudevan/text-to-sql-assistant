from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class SQLGenerator:
    def __init__(self):
        # Initialize FLAN-T5-small model and tokenizer
        self.model_name = "google/flan-t5-small"
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_name) #Handles text tokenization
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_name) # Loads the model
        
    def generate_sql(self, text_query: str, schema: str) -> str:
        # Construct prompt combining schema and query
        prompt = f"""
        Given the database schema:
        {schema}
        
        Convert this question to SQL:
        {text_query}
        """
        
        # Convert text to tokens and generate SQL
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=512)
        outputs = self.model.generate(**inputs, max_length=128)
        sql_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return sql_query
    