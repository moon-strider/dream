import json
import logging
import os
import time

import sentry_sdk
import torch
from flask import Flask, request, jsonify
from sentry_sdk.integrations.flask import FlaskIntegration
from transformers import AutoModelForCausalLM, AutoTokenizer

from common.prompts import META_GOALS_PROMPT
from common.universal_templates import GENERATIVE_ROBOT_TEMPLATE


sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[FlaskIntegration()])

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

PRETRAINED_MODEL_NAME_OR_PATH = os.environ.get("PRETRAINED_MODEL_NAME_OR_PATH")
HALF_PRECISION = os.environ.get("HALF_PRECISION", 0)
HALF_PRECISION = 0 if HALF_PRECISION is None else bool(int(HALF_PRECISION))
logger.info(f"PRETRAINED_MODEL_NAME_OR_PATH = {PRETRAINED_MODEL_NAME_OR_PATH}")
LANGUAGE = os.getenv("LANGUAGE", "EN")
NAMING = {
    "EN": ["AI", "Human"],
    "RU": ["Чат-бот", "Человек"],
}

app = Flask(__name__)
logging.getLogger("werkzeug").setLevel("WARNING")

DEFAULT_CONFIGS = {
    "EleutherAI/gpt-j-6B": json.load(open("common/generative_configs/default_generative_config.json", "r")),
    "OpenAssistant/pythia-12b-sft-v8-7k-steps": json.load(
        open("common/generative_configs/default_generative_config.json", "r")
    ),
    "togethercomputer/GPT-JT-6B-v1": json.load(open("common/generative_configs/default_generative_config.json", "r")),
}


def generate_responses(context, model, tokenizer, prompt, generation_params, continue_last_uttr=False):
    outputs = []
    dialog_context = ""
    if prompt:
        dialog_context += prompt + "\n"
    s = len(context) % 2
    context = [f"{NAMING[LANGUAGE][(s + uttr_id) % 2]}: {uttr}" for uttr_id, uttr in enumerate(context)]
    if continue_last_uttr:
        dialog_context += "\n".join(context)
    else:
        dialog_context += "\n".join(context) + f"\n{NAMING[LANGUAGE][0]}:"

    logger.info(f"context inside generate_responses seen as: {dialog_context}")
    bot_input_ids = tokenizer([dialog_context], return_tensors="pt").input_ids
    with torch.no_grad():
        if torch.cuda.is_available():
            bot_input_ids = bot_input_ids.to("cuda")
        chat_history_ids = model.generate(
            bot_input_ids,
            pad_token_id=tokenizer.eos_token_id,
            **generation_params,
        )
    if torch.cuda.is_available():
        chat_history_ids = chat_history_ids.cpu()
    for result in chat_history_ids:
        output = tokenizer.decode(result, skip_special_tokens=True)
        result_cut = output.replace(dialog_context + " ", "")
        result_cut = [x.strip() for x in GENERATIVE_ROBOT_TEMPLATE.split(result_cut) if x.strip()][0]
        logger.info(f"hypothesis: {result_cut}")
        outputs.append(result_cut)

    return outputs


try:
    tokenizer = AutoTokenizer.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH)
    if HALF_PRECISION:
        model = AutoModelForCausalLM.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH, torch_dtype=torch.float16)
    else:
        model = AutoModelForCausalLM.from_pretrained(PRETRAINED_MODEL_NAME_OR_PATH)
    if torch.cuda.is_available():
        model.to("cuda")
        logger.info("transformers_lm is set to run on cuda")
    config = DEFAULT_CONFIGS[PRETRAINED_MODEL_NAME_OR_PATH]
    example_response = generate_responses(
        ["What is the goal of SpaceX?"],
        model,
        tokenizer,
        "You are a SpaceX Assistant.",
        config,
    )
    logger.info(f"example response: {example_response}")
    logger.info("transformers_lm is ready")
except Exception as e:
    sentry_sdk.capture_exception(e)
    logger.exception(e)
    raise e


@app.route("/ping", methods=["POST"])
def ping():
    return "pong"


@app.route("/respond", methods=["POST"])
def respond():
    st_time = time.time()
    contexts = request.json.get("dialog_contexts", [])
    prompts = request.json.get("prompts", [])
    configs = request.json.get("configs", None)
    configs = [None] * len(prompts) if configs is None else configs
    configs = [DEFAULT_CONFIGS[PRETRAINED_MODEL_NAME_OR_PATH] if el is None else el for el in configs]
    if len(contexts) > 0 and len(prompts) == 0:
        prompts = [""] * len(contexts)

    try:
        responses = []
        for context, prompt, config in zip(contexts, prompts, configs):
            curr_responses = []
            outputs = generate_responses(context, model, tokenizer, prompt, config)
            for response in outputs:
                if len(response) >= 2:
                    curr_responses += [response]
                else:
                    curr_responses += [""]
            responses += [curr_responses]

    except Exception as exc:
        logger.exception(exc)
        sentry_sdk.capture_exception(exc)
        responses = [[""]] * len(contexts)

    logger.info(f"transformers_lm output: {responses}")
    total_time = time.time() - st_time
    logger.info(f"transformers_lm exec time: {total_time:.3f}s")
    return jsonify(responses)


@app.route("/generate_goals", methods=["POST"])
def generate_goals():
    st_time = time.time()

    prompts = request.json.get("prompts", None)
    prompts = [] if prompts is None else prompts
    configs = request.json.get("configs", None)
    configs = [None] * len(prompts) if configs is None else configs
    configs = [DEFAULT_CONFIGS[PRETRAINED_MODEL_NAME_OR_PATH] if el is None else el for el in configs]

    try:
        responses = []
        for prompt, config in zip(prompts, configs):
            context = ["hi", META_GOALS_PROMPT + f"\nPrompt: '''{prompt}'''\nResult:"]
            goals_for_prompt = generate_responses(context, model, tokenizer, "", config)[0]
            logger.info(f"Generated goals: `{goals_for_prompt}` for prompt: `{prompt}`")
            responses += [goals_for_prompt]

    except Exception as exc:
        logger.info(exc)
        sentry_sdk.capture_exception(exc)
        responses = [""] * len(prompts)

    total_time = time.time() - st_time
    logger.info(f"openai-api generate_goals exec time: {total_time:.3f}s")
    return jsonify(responses)
