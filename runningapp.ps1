# Navigate to the parent directory of 'Etapa 44 RtR Data Explorer 2024 Update'
cd "C:\Users\franc\DRIVE\CR2-RtR\Etapa 44 RtR Data Explorer 2024 Update"

# Navigate into the virtual environment directory
cd ".\venv_rtr_postcop29"

# Activate the virtual environment
.\Scripts\Activate

# Navigate back to the parent directory
cd ..

# Navigate into the 'RtRDataExplorer_POST_COP29' directory
cd ".\RtRDataExplorer_POST_COP29"

# Run the Streamlit application
streamlit run ".\etl_process.py"
