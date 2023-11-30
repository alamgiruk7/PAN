# import re, torch, os
# import nltk  # we'll use this to split into sentences
# import numpy as np
import os
import subprocess
import time
import wave

# import scipy
# from flask import Flask, jsonify, request
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import (
#     StreamingStdOutCallbackHandler,
# )  # for streaming resposne
# from langchain.prompts import ChatPromptTemplate
# from langchain.prompts.chat import SystemMessage, HumanMessagePromptTemplate
# from IPython.display import Audio
# from pydub import AudioSegment
# from bark.generation import (
#     generate_text_semantic,
#     preload_models,)
# from bark.api import semantic_to_waveform
# from bark import generate_audio, SAMPLE_RATE
# from transformers import AutoProcessor, BarkModel
# from video_gen import video_gen
# from tqdm import tqdm
# from os import path
# from scipy.io import wavfile
# from flask import Flask
# from flask_cors import CORS
# from TTS.tts.configs.bark_config import BarkConfig
# from TTS.tts.models.bark import Bark
# from utilities import MongoDBClient

from flask import Flask

app = Flask(__name__)
CORS(app)


CONNECTION_STRING = "mongodb://localhost:27017"
DATABASE = "pan"

mongo_client = MongoDBClient(CONNECTION_STRING, DATABASE)

# LLAMA2\
# device = 'CUDA'
# model_path = "C:/AI/NewsCaster/newscaster/api/llama-2-7b-chat-gguf.bin"


# Audio/ SunoAi-Bark
# output_folder = "C:/AI/NewsCaster/newscaster/inputs"
# output_filename = "Audio"

# def voice_clone():
#     config = BarkConfig()
#     model = Bark.init_from_config(config)
#     model.load_checkpoint(config, checkpoint_dir="C:/AI/NewsCaster/newscaster/bark/", eval=True)
#     model.to("cuda")
#     text = "Hello, my name is Rabia , how are you?"

#     # cloning a speaker.
#     # It assumes that you have a speaker file in `bark_voices/speaker_n/speaker.wav` or `bark_voices/speaker_n/speaker.npz`
#     output_dict = model.synthesize(text, config, speaker_id="speaker", voice_dirs="C:/AI/NewsCaster/newscaster/bark_voices/")
#     sample_rate= 24000
#     scipy.io.wavfile.write("bark_out.wav", rate =sample_rate , data= output_dict["wav"])

# @app.route('/askchatbot', methods=['POST'])
# def chatbot():
#     params = request.get_json()
#     question = f"""
#     Suppose you are a news anchor person, Generate flash news bulletin from the news articles provides below.
#     Start and end the bulletin like a real TV anchor
#     start with one Greeting according to the time, time = 11 am.
#     I'm here to bring you the latest [news topic/ introduction by analyzing the news.
#     then summarization shouldn't be more than 100 words. It should be in continuous flow.
#     Do not add conjunction in start of new paragraph. Start the summarization directly.
#     1. {params[0].values()}
#     2. {params[1].values()}
#     """
#     print(question, "dasdaoiusdjapoisjdaisdsa")
#     template = """Question: {question}
#     Answer: """
#     prompt = PromptTemplate(template=template, input_variables=["question"])
#     #Callbacks support token-wise streaming
#     callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
#     n_gpu_layers = 12  # Change this value based on your model and your GPU VRAM pool.
#     n_batch = 500  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.
#     llm = LlamaCpp(
#         model_path=model_path,
#         n_gpu_layers=n_gpu_layers,
#         n_batch=n_batch,
#         callback_manager=callback_manager,
#         verbose=True,
#         n_ctx=5000,
#         max_tokens=1000,
#         temperature=1
#     )
#     llm_chain = LLMChain(prompt=prompt, llm=llm)
#     result = llm_chain.run(question)
#     return jsonify(result)

# @app.route('/genaudio/', methods=['GET'])
# def genaudio():
#     text = request.args.get('response')


#     #save generated news to db
#     news_collection = mongo.db.news
#     news_collection.insert_one({'news': text})


#     cleaned_sentence = re.sub(r':', '', text)
#     script=cleaned_sentence.replace(",", " ").strip()
#     sentences = nltk.sent_tokenize(script)
#     processor_audio = AutoProcessor.from_pretrained("C:\\AI\\NewsCaster\\newscaster\\models\\T2A")
#     model_audio = BarkModel.from_pretrained("C:\\AI\\NewsCaster\\newscaster\\models\\T2A")
#     SPEAKER = "v2/en_speaker_9"
#     silence = np.zeros(int(0.25 * SAMPLE_RATE))

#     pieces = []
#     for sentence in sentences:
#         print(sentence)
#         audio_array = generate_audio(sentence, history_prompt=SPEAKER)
#         pieces += [audio_array]

#    #audio = Audio(np.concatenate(pieces), rate=SAMPLE_RATE)
#     concatenated_audio = np.concatenate(pieces)

#     # Convert to a NumPy array if it's not already
#     if not isinstance(concatenated_audio, np.ndarray):
#         concatenated_audio = np.array(concatenated_audio)

#     # Save the audio as a WAV file
#     # Generate a unique output file path based on output_folder and output_filename
#     output_file_path = os.path.join(output_folder, f'{output_filename}.wav')
#     counter = 1
#     while os.path.exists(output_file_path):
#         # If the file already exists, append a number to the filename and check again
#         output_file_path = os.path.join(output_folder, f'{output_filename}_{counter}.wav')
#         counter += 1

#     # Save the audio as a WAV file
#     wavfile.write(output_file_path, SAMPLE_RATE, concatenated_audio)
#     audioResult = Audio(np.concatenate(pieces), rate=SAMPLE_RATE)
#     audioData = {
#         "Audio_path" : output_file_path,
#     }
#     return jsonify(audioData)

# @app.route('/genvideo/', methods=['GET'])
# def vid_gen():
#     audioPath = request.args.get('audio_path')
#     outputPath = 'C:/AI/NewsCaster/newscaster/outputs'
#     output_filename = "output"
#     output_file_path = os.path.join(outputPath, f'{output_filename}')
#     counter = 0
#     while os.path.exists(output_file_path):
#         # If the file already exists, append a number to the filename and check again
#         output_file_path = os.path.join(outputPath, f'{output_filename}_{counter}')
#         counter += 1

#     inputAudioPath = audioPath
#     inputVideoPath = 'C:/AI/NewsCaster/newscaster/inputs/MoeenaAI.mp4'
#     checkpoint_path = 'C:/AI/NewsCaster/newscaster/api/Wav2Lip_master/checkpoints/wav2lip.pth'
#     unProcessedFramesFolderPath = os.path.join(output_file_path, 'frames')
#     os.makedirs(unProcessedFramesFolderPath, exist_ok=True)
#     lipSyncedOutputPath = os.path.join(output_file_path, 'result.mp4')

#     concatTextFilePath = os.path.join(output_file_path, 'concat.txt')
#     concatedVideoOutputPath = os.path.join(output_file_path, 'concated_output.avi')
#     finalProcessedOutputVideo = os.path.join(output_file_path, 'final_with_audio.mp4')
#     video_gen(checkpoint_path, inputVideoPath, inputAudioPath, lipSyncedOutputPath, unProcessedFramesFolderPath, output_file_path,
#                 concatTextFilePath, concatedVideoOutputPath,finalProcessedOutputVideo)
#     videoData = {
#         "Video_path" : output_file_path,
#     }
#     return jsonify(videoData)

# @app.route('/login', methods=['GET'])
# def user_login():
#     COLLECTON = 'users'
#     params = request.args.to_dict()
#     email = params["email"]
#     password = params["password"]
#     user = mongo_client.user_login(email, password, COLLECTON)

#     print(user, "user has been logged in atleast")

#     # userDetails = {
#     #     "email" : email,
#     # }
#     return jsonify(user)

# @app.route('/signup', methods=['GET'])
# def user_signup():
#     COLLECTON = 'users'
#     params = request.args.to_dict()
#     email = params["email"]
#     password = params["password"]
#     status = mongo_client.create_user(email, password, COLLECTON)

#     if status:
#         return jsonify({'found': True}), 200
#     else:
#         return jsonify({'found': False}), 404

# @app.route('/gethistory', methods=['GET'])
# def get_history():
#     news_collection = mongo.db.news
#     news_entries = list(news_collection.find({}))
#     for entry in news_entries:
#         entry['_id'] = str(entry['_id'])
#     return jsonify({'news': news_entries}), 200


@app.route("/getnews", methods=["GET"])
def get_news():
    params = request.get_json(silent=True)
    COLLECTION = "news"
    if params and "genre" in params and "source" in params:
        genre = params["genre"]
        source = params["source"]
        query = {"$and": [{"genre": genre}, {"source": source}]}
        results = mongo_client.find_documents(COLLECTION, query)
    else:
        results = mongo_client.find_all(COLLECTION)

    results_list = list(results)
    for entry in results_list:
        entry["_id"] = str(entry["_id"])
    return jsonify({"news": results_list}), 200


if __name__ == "__main__":
    app.run(debug=True)
