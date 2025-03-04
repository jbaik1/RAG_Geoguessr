# Solving Geoguessr Puzzles with Multimodal Language Models Using RAG

Geoguessr is a popular game where one must guess the location of the presented Google Street View image.

![image](https://images.squarespace-cdn.com/content/v1/60f6054f4e76b03092956de8/fbba3851-0172-409c-9eb0-2cbefadce395/Geoguessr+HUD.png)
(Example from https://www.plonkit.net/beginners-guide)

This notebook contains an implementation of RAG for solving these problems with multimodal LLMs, and compares the performance of 3 models: OpenAI's GPT-4o, Google's Gemini-1.5, and Anthropic's Claude 3.5.

A demo is shown in the notebook RAG_Geoguessr.ipynb

# Setup

To install the python packages, create a new Conda or virtual Python enviornment as use
`pip install requirements.txt`

Full dataset (~8GB) is from [https://www.kaggle.com/datasets/ubitquitin/geolocation-geoguessr-images-50k?resource=download](https://www.kaggle.com/datasets/ubitquitin/geolocation-geoguessr-images-50k?resource=download),
but I have uploaded a small portion of it on this repository for demonstration purposes.

# Results

A simple experiment results in the following accuracices:

| Model    | Accuracy|
| -------- | ------- |
| Claude   |   0.65  |
|  GPT     |   0.55  |
| Gemini   |   0.45  |

It appears that