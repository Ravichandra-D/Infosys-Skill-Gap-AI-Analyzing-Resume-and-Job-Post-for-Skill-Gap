import streamlit as st
from modules.processor import DocumentProcessor

def main():
    """Main entry point of the app"""
    try:
        # Initialize and run processor
        processor = DocumentProcessor()
        processor.run_pipeline()

        # Sidebar information
        with st.sidebar:
            st.header("ℹ️ Information")
            st.markdown("""
            **Supported Formats:**
            - PDF
            - DOCX
            - TXT

            **File Size Limit:** 10MB per file

            **Steps:**
            1. Upload & validate files
            2. Extract text
            3. Clean text
            4. Display results & download
            """)

            st.header("📋 Status")
            if st.session_state.get('processed_docs'):
                total = len(st.session_state.processed_docs)
                successful = sum(1 for doc in st.session_state.processed_docs if doc['success'])
                st.success(f"Processed: {successful}/{total} documents")
            else:
                st.info("No documents processed yet")

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.error("Please refresh and try again.")

if __name__ == "__main__":
    main()
