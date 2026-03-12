# LLMChatbot_Argus

Argus is a chatbot trained to answer about greek mythology 👁️. 

## 🚀 Components:
  - **LLM**: Qwen/Qwen2.5-1.5B-Instruct
  - RAG (Retrieval-Augmented Generation)
  - Pinecone
  - Streamlit

## Dual Retrieve & Re-rank
I tried implementing two-step retrieval, combining with different techniques of chunking, in order to produce a better context for the LLM answer. 

Currently, the RAG is implemented with a Phase 1-Recursive Splitting and Phase 2-Character Splitting.
  - **Phase 1** apply the R&R on the documents with Recursive splitting of the docs.
  - **Phase 2** apply R&R on the *top_k* results from phase 1

Two embeddings with the different chunking techniques are pre-processed and kept on Pinecone. The *chat.py* code access the macro namespace first (recursive splitting), then filter the documents returned on the best results on the micro namespace (character splitting). 

### Why?
My reasoning is that I believe that, through this, the model can achieve a better context by revisiting the better ranked documents.
I still need to make more tests and compare results to confirm it. So far, it's just my perception. 

## Future Improvements
There are lot to improve from the current state. I want to test more with the chunking and test with different embedding models. 
Most importantly, I want to test if the results from the Phase 2 are redundant - two or more context from different documents but saying the same thing. I suspect this is biasing the model to answer focused on these repeated contexts, rather than diversyfing the context to provide a better answer. 


*Renata Balbino - 11/03/2026*
