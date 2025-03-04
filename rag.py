import base64
import json
from dotenv import load_dotenv

from langchain_core.messages import HumanMessage
from langchain_community.document_loaders import TextLoader
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class LLM_Guesser():
   def __init__(self, model_name):
      self.llm = None
      self.model_name = model_name
      
      if model_name == "GPT":
         self.llm = ChatOpenAI(model="gpt-4o", max_tokens=512, temperature=0)
      elif model_name == "Claude":
         self.llm = ChatAnthropic(
               model="claude-3-5-sonnet-20240620",
               max_tokens=512,
               temperature=0
            )
         pass
      elif model_name == "Gemini":
         self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-001",
            temperature=0,
            max_tokens=512
         )
         pass
      
      
      embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
      self.vector_store = InMemoryVectorStore(embeddings)
      self.document_ids = []
      
      loader = TextLoader("reference.txt")
      reference_doc = loader.load()
      text_splitter = RecursiveCharacterTextSplitter(
         chunk_size=1000,  # chunk size (characters)
         chunk_overlap=200,  # chunk overlap (characters)
         add_start_index=True,  # track index in original document
      )
      all_splits = text_splitter.split_documents(reference_doc)
      self.document_ids = self.vector_store.add_documents(documents=all_splits)

   
   def describe(self, image_path):
      """An initial LLM description of a given image

      Args:
         image_path (str): path to image

      Returns:
         str: LLM description of image
      """
      with open(image_path, "rb") as image_file:
         image_data = base64.b64encode(image_file.read()).decode('utf-8')
      
      prompt = """
      
      Describe the image in detail, paying attention to details that can give clues about the location of this image. 
      Here are some example details:
      1. Car license plates
      2. Road marks and signals
      3. Left vs right driving
      4. Language
      5. Vegetation and weather
      6. Geography, Flags
      7. House shape/materials
      ... and any other noteworthy details, no matter how small they are
      
      Finally, take a guess as to which country of the photo
      """

      msg = self.llm.invoke(
         [
            HumanMessage(
               content=[
                  {"type": "text", "text": prompt},
                  {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                  },
               ]
            )
         ]
      )
      description = msg.content
      return description


   def retrieve(self, location_clues):
      """Given a description of the location, find sections of the reference document
      that can help make a better guess

      Args:
         location_clues (str): Initial LLM description of picture

      Returns:
         str: Contents of relevent document chunks
      """
      retrieved_docs = self.vector_store.similarity_search(location_clues, k=3) # find relevant docs to the query
      docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
      return docs_content

   def generate(self, context, image_path):
      """Make an educated guess after consulting reference with RAG

      Args:
         context (str): Relevent document materials from vector store
         image_path (str): Path to image

      Returns:
         str: Output of the LLM
      """
      with open(image_path, "rb") as image_file:
         image_data = base64.b64encode(image_file.read()).decode('utf-8')
         
      prompt = f"""
      Carefully analyze the photo, in order to correctly guess the location of the photo.
      Give an elaborate reasoning as to why you chose the country. 
      Include details such as: 
      1. Car license plates
      2. Road marks and signals
      3. Left vs right driving
      4. Language
      5. Vegetation and weather
      6. Geography, Flags
      7. House shape/materials
      ... and any other noteworthy details, and corroborate with the following reference material,
      
      Some relevant materials: {context}
      
      Return your answer strictly in the following JSON format:
      {{
         "country" : "[country]",
         "reason" : "[reason]"
         
      }}
      """
      
      msg = self.llm.invoke(
         [
            HumanMessage(
               content=[
                  {"type": "text", "text": prompt},
                  {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                  },
               ]
            )
         ]
      )
      
      return msg.content

   def guess_location(self, image_path):
      """Use RAG to guess location of a Google Street View image

      Args:
         image_path (str): Path to image

      Returns:
         dict: dict containing the initial discription, the relevant docs, and the final response
      """

      initial_description = self.describe(image_path)
      reference = self.retrieve(initial_description)
      result = self.generate(reference, image_path)
      
      # extract guess from returned string, which should be in json form
      response = result.replace("`","")
      response = response.replace("json","")
      response = response.replace("\n","")
      try:
         response = json.loads(response)
      except:
         print("failed to convert it to json, check raw output instead")
         return {"initial_description": initial_description, "reference": reference, "country": "", "raw_output": result}
      
      return {"initial_description": initial_description, "reference": reference, "country": response["country"], "reason": response["reason"], "raw_output": result}
      