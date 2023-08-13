# Note: This is taken as it is from one of the source
# Not used in the project but keeping as a reference

import wikipedia
import transformers
import spacy
from transformers import AutoModelWithLMHead, AutoTokenizer
import random
import constants as const

tokenizer = AutoTokenizer.from_pretrained(const.MODEL_NAME)
model = AutoModelWithLMHead.from_pretrained(const.MODEL_NAME)
nlp = spacy.load("en_core_web_sm")

def get_question(answer, context, max_length=64):
  input_text = "answer: %s  context: %s </s>" % (answer, context)
  features = tokenizer([input_text], return_tensors='pt')

  output = model.generate(input_ids=features['input_ids'], 
               attention_mask=features['attention_mask'],
               max_length=max_length)

  return tokenizer.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)

def greet(entered_topic):
    print("Entered topic: ", entered_topic)
    topics = wikipedia.search(entered_topic)
    topics = topics[:3]
    random.shuffle(topics)
    for topic in topics:
        try:
            summary = wikipedia.summary(topic)
        except wikipedia.DisambiguationError as e:
            # print(e.options)
            s = random.choice(e.options)
            summary = wikipedia.summary(s)
        except wikipedia.PageError as e:
            continue
        break
    if(len(topics) == 0):
        return ["Please Type a Different Topic"]

    print("Selected topic: ", topic)        
    print("Summary: ", summary)
    summary = summary.replace("\n", "")
    doc = nlp(summary)

    answers = doc.ents
    filtered_answers = []
    for answer in answers:
        if(answer.text.lower() in entered_topic.lower() or entered_topic.lower() in answer.text.lower()):
            pass
        else:
            filtered_answers.append(answer)

    answer_1 = random.choice(filtered_answers)
    question_1 = get_question(answer_1, summary)
    question_1 = question_1[9:]
    print("Question: ", question_1)
    print("Answer: ", answer_1)
    return [question_1, gr.update(visible=True), gr.update(value=answer_1, visible=False)]

    
def get_answer(input_answer, gold_answer):
    print("Entered Answer: ", input_answer)
    return gr.update(value=gold_answer, visible=True)


with gr.Blocks() as demo:
    # with gr.Row():
        topic = gr.Textbox(label="Topic")
        greet_btn = gr.Button("Ask a Question")
        question = gr.Textbox(label="Question")
        input_answer = gr.Textbox(label="Your Answer", visible=False)
        answer_btn = gr.Button("Show Answer")        
        gold_answer = gr.Textbox(label="Correct Answer", visible=False)
        greet_btn.click(fn=greet, inputs=topic, outputs=[question, input_answer, gold_answer])

    # with gr.Row():
                        
        answer_btn.click(fn=get_answer, inputs=[input_answer,gold_answer], outputs=gold_answer)

demo.launch()