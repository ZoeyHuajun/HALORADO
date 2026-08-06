# get the tool from hugging face(translation and ai model)
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "Qwen/Qwen2.5-0.5B-Instruct"
#download tokenizer and model 从训练好的模型里加载
tokenizer = AutoTokenizer.from_pretrained(model_name)
#ai model 预测文字
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto"
)
#create a function to ask ai model
def ask_ai(message):

    messages = [
        {
            "role": "user",
            "content": message
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True # ai answers
    )

    model_inputs = tokenizer(
        [text], # to numbers
        return_tensors="pt" #pytorch
    )

    generated_ids = model.generate(
        **model_inputs, #dictionay unpacking 
        max_new_tokens=150
    )

    generated_ids = generated_ids[:, model_inputs.input_ids.shape[1]:]

    response = tokenizer.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return response