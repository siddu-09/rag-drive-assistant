import asyncio
import os

import streamlit as st

from app.services.query_service import QueryService
from app.services.sync_service import SyncService


def run_async(coro):
    return asyncio.run(coro)


st.set_page_config(page_title="RAG Drive Assistant", layout="wide")

st.title("RAG Drive Assistant")
st.write("Sync a Google Drive folder, then ask questions about its documents.")

sync_service = SyncService()
query_service = QueryService()

default_folder_id = os.getenv("GDRIVE_FOLDER_ID", "")
folder_id = st.text_input("Google Drive folder ID", value=default_folder_id)

left_column, right_column = st.columns([1, 2])

with left_column:
    if st.button("Sync Drive"):
        if not folder_id:
            st.error("Provide a Google Drive folder ID first.")
        else:
            with st.spinner("Syncing documents from Google Drive..."):
                try:
                    result = run_async(sync_service.sync(folder_id))
                    st.success(f"Synced {result['doc_count']} documents and {result['chunk_count']} chunks.")
                except Exception as exc:
                    st.error(f"Sync failed: {exc}")

with right_column:
    st.caption("Required secrets: `GROQ_API_KEY` and either `GOOGLE_CREDENTIALS_JSON` or `credentials.json`.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Ask a question about the synced documents...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    with st.spinner("Searching and generating an answer..."):
        try:
            result = run_async(query_service.query(query))
            answer = result.get("answer", "No response")
            sources = result.get("sources", [])
        except Exception as exc:
            answer = f"Error: {exc}"
            sources = []

    st.session_state.messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)

        if sources:
            with st.expander("Sources"):
                for source in sources:
                    st.write(source)