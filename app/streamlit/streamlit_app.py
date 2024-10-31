import streamlit as st
import requests
import pandas as pd
import psycopg2
# from psycopg2.extras import execute_values
import uuid

st.set_page_config(page_title="Simple Search Engine", layout="wide")


def setup_db_connection():
    try:
        return psycopg2.connect(
            "dbname=db user=postgres password=docker host=db"
        )
    except psycopg2.Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None


def insert_document(query, session_id, related_docs, selected_doc):

    try:
        connection = setup_db_connection()
        sql_excutor = connection.cursor()

        insert_doc_query = """
            INSERT INTO user_logs (session_id, search_query, related_docs,selected_doc)
            VALUES (%s,%s,%s,%s)
        """

        sql_excutor.execute(
            insert_doc_query, (session_id, query, related_docs, selected_doc))

        # this persists database changes
        connection.commit()

        sql_excutor.close()
        connection.close()
        st.success("Search results stored in the database.")

    except Exception as e:
        st.error(f"error in inserting documents ")


def truncate_text(text, max_length=50):
    return text[:max_length] + "..." if len(text) > max_length else text


def display_document(docs, selected_index, doc_type):
    st.write(f"{doc_type} Document:")
    st.write(docs[selected_index])


st.title("Simple Search Engine")

col1, col2 = st.columns(2)

with col1:
    query = st.text_input("Enter your search query", max_chars=200)

search_button = st.button("Search")

most_similar = st.button("Submit (Most Similar)")

# Initialize session state
if "search_performed" not in st.session_state:
    st.session_state.search_performed = False

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if search_button and query:
    try:
        response = requests.post(
            "http://mlops-fastapi-1:8000/search", json={"query": query})

        print({"query": query})

        if response.status_code == 200:
            st.session_state.search_performed = True
            data = response.json()

            print(data)

            # Store the response data in session state
            st.session_state.rel_docs = data["rel_docs"]
            st.session_state.rel_docs_sim = data["rel_docs_sim"]
        else:
            st.error(
                f"Error: Unable to retrieve documents. Status code: {response.status_code}")
            st.write(f"Response content: {response.text}")
    except Exception as e:
        st.error(f"Error occurred: {str(e)}")

if st.session_state.search_performed:
    df_similar = pd.DataFrame({
        "Document": [truncate_text(doc) for doc in st.session_state.rel_docs],
        # Using rel_docs_sim instead of distances
        "Cosine Similarity": st.session_state.rel_docs_sim,
    }).reset_index(drop=True)

    with col1:
        st.subheader("Most Similar Results:")
        if len(df_similar) > 0:
            selected_similar = st.selectbox(
                "Select a similar document to view full text:",
                options=list(range(len(df_similar))),
                format_func=lambda x: df_similar.loc[x, "Document"],
                key="similar_select",
            )
            st.table(df_similar.style.format({"Cosine Similarity": "{:.4f}"}))
        else:
            st.write("No similar documents found.")

    with col2:
        st.subheader("Selected Document:")
        if len(df_similar) > 0 and selected_similar is not None:
            display_document(st.session_state.rel_docs,
                             selected_similar, "Similar")
    if most_similar and query and selected_similar is not None:
        # insert_document(query, st.session_state.session_id, df_similar.loc[selected_similar, "Document"])
        insert_document(query, st.session_state.session_id,
                        related_docs=st.session_state.rel_docs, selected_doc=selected_similar)


else:
    st.write("Enter a query and click 'Search' to see results.")
