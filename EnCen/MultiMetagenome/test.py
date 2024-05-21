import streamlit as lit 
import tempfile
import os
import shutil

uploaded_file = lit.file_uploader("", type='.faa')
if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
path
shutil.move(path, '/Users/johndocter/Documents')
shutil.rmtree(temp_dir)

