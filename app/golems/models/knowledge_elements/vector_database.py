import faiss

from langchain.docstore import InMemoryDocstore
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from app.golems.models.knowledge_elements.extractor_golem import ExtractorGolem
from app.sample_assets.papers import sample_text_chunks

golem = ExtractorGolem()


embedding_size = 1536 # Dimensions of the OpenAIEmbeddings
index = faiss.IndexFlatL2(embedding_size)
embedding_fn = OpenAIEmbeddings().embed_query
vectorstore = FAISS(embedding_fn, index, InMemoryDocstore({}), {})

if __name__ == '__main__':

    for idx, text in enumerate(sample_text_chunks):

        print(idx/len(sample_text_chunks))

        elements = golem.get_element_list(text)
        print(elements)
        vectorstore.add_texts(elements)

        vectorstore.save_local("faiss_index")
