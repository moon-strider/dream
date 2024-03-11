import logging
import json
import os
import time

import sentry_sdk
import torch
from flask import Flask, request, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from transformers import AutoModelForCausalLM, AutoTokenizer
#from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[FlaskIntegration()])


logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

PRETRAINED_MODEL_NAME_OR_PATH = os.environ.get("PRETRAINED_MODEL_NAME_OR_PATH")
N_HYPOTHESES_TO_GENERATE = int(os.environ.get("N_HYPOTHESES_TO_GENERATE", 1))
CONFIG_NAME = os.environ.get("CONFIG_NAME")
logging.info(f"PRETRAINED_MODEL_NAME_OR_PATH = {PRETRAINED_MODEL_NAME_OR_PATH}")
DEFAULT_CONFIDENCE = 0.9
ZERO_CONFIDENCE = 0.0
MAX_HISTORY_DEPTH = 3
with open(CONFIG_NAME, "r") as f:
    generation_params = json.load(f)
generation_params["num_return_sequences"] = N_HYPOTHESES_TO_GENERATE

try:
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH)
    #model = AutoModelForSeq2SeqLM.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH)
    model = AutoModelForCausalLM.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH)
    if torch.cuda.is_available():
        model.to("cuda")
        logger.info("dialogpt is set to run on cuda")

    logger.info("dialogpt is ready")
except Exception as e:
    sentry_sdk.capture_exception(e)
    logger.exception(e)
    raise e

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel("WARNING")


def generate_responses(context, model, tokenizer):
    encoded_context = []
    for uttr in context[-MAX_HISTORY_DEPTH:]:
        encoded_context += [tokenizer.encode(uttr + " " + tokenizer.eos_token, return_tensors="pt")]
    bot_input_ids = torch.cat(encoded_context, dim=-1)

    with torch.no_grad():
        if torch.cuda.is_available():
            bot_input_ids = bot_input_ids.to("cuda")
        chat_history_ids = model.generate(bot_input_ids, pad_token_id=tokenizer.eos_token_id, **generation_params)
        if torch.cuda.is_available():
            chat_history_ids = chat_history_ids.cpu()

    outputs = [tokenizer.decode(x[len(bot_input_ids[0]) :], skip_special_tokens=True) for x in chat_history_ids]
    return outputs


@app.route("/respond", methods=["POST"])
def respond():
    st_time = time.time()
    contexts = request.json.get("utterances_histories", [])

    try:
        responses = []
        confidences = []
        for context in contexts:
            curr_responses = []
            curr_confidences = []
            outputs = generate_responses(context, model, tokenizer)
            for response in outputs:
                if len(response) > 3:
                    # drop too short responses
                    curr_responses += [response]
                    curr_confidences += [DEFAULT_CONFIDENCE]
                else:
                    curr_responses += [""]
                    curr_confidences += [ZERO_CONFIDENCE]

            responses += [curr_responses]
            confidences += [curr_confidences]

    except Exception as exc:
        logger.exception(exc)
        sentry_sdk.capture_exception(exc)
        responses = [[""]] * len(contexts)
        confidences = [[ZERO_CONFIDENCE]] * len(contexts)

    total_time = time.time() - st_time
    logger.info(f"dialogpt exec time: {total_time:.3f}s")
    return jsonify(list(zip(responses, confidences)))
