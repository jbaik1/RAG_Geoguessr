# Solving Geoguessr with Multimodal Language Models Using RAG

Geoguessr is a popular game where one must guess the location of the presented Google Street View image.

![image](https://images.squarespace-cdn.com/content/v1/60f6054f4e76b03092956de8/fbba3851-0172-409c-9eb0-2cbefadce395/Geoguessr+HUD.png)
(Example from https://www.plonkit.net/beginners-guide)

This notebook contains an implementation of RAG for solving these problems with multimodal LLMs, and compares the performance of 3 models: OpenAI's GPT-4o, Google's Gemini-1.5, and Anthropic's Claude 3.5.

A demo is shown in the notebook RAG_Geoguessr.ipynb

# Setup

To view just the RAG demos, create a new python virtual environment and use:

```pip install requirements.txt```

To run the notebooks with computer vision models, the needed packages are listed in the notebook.

Full dataset (~8GB) is from [https://www.kaggle.com/datasets/ubitquitin/geolocation-geoguessr-images-50k?resource=download](https://www.kaggle.com/datasets/ubitquitin/geolocation-geoguessr-images-50k?resource=download),
but I have uploaded a small portion of it on this repository for demonstration purposes.

# Results

A simple experiment results in the following accuracices:

| Model    | Accuracy|
| -------- | ------- |
| GPT-4o    |   0.74  |
|  Gemini 1.5   |   0.72  |
| Claude 3.5 Sonnet |   0.68  |

It appears that GPT-4o has the best accuracy over a sample size of 50 rounds. The rounds included countries like the United States, Thailand, Austrailia, Bolivia, and so on.

# Comparison with Modern CV Classification Models

I have ran some tests on ResNet, EfficientNet, and Vision Transformer to see how they compare to the LLMs. Because they are specialized at vision tasks, it is reasonable to expect that they will perform better. However, this was not the case. See efficientnet.ipynb, ViT.ipynb, and resnet.ipynb for the demos.

In addition, I fine-tuned an EfficientNet v2 model on the full dataset for about 48 hours. The best performance was around 58%, which is still low compared to the LLMs. 

This demonstrates that RAG can enable multimodal LLMs to perform well at this complex zero-shot task, and further highlights the potential of future LLMs to be come increasingly general-purpose. 