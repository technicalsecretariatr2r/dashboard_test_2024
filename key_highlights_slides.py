import streamlit as st
import streamlit as st
import fitz  # PyMuPDF
import os

def key_highlights():
    #Slides Horizontal
    file_path_slides = "rtrframework2023_slides.pdf"
    # Function to process and cache the images from the PDF

    @st.cache_data
    def get_pdf_images(file_path):
        doc = fitz.open(file_path)
        all_images = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)  # number of page
            zoom = 2  # increase the resolution
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            image = pix.tobytes("png")
            all_images.append(image)
        return all_images

    def display_pdf_horizontal(all_images, start_page=0):
        # Initialize counter to start_page
        if 'counter' not in st.session_state or st.session_state.counter != start_page:
            st.session_state.counter = start_page

        # Slider for fast navigation
        page_slider = st.slider('Go to Page', 1, len(all_images), st.session_state.counter + 1)
        if page_slider - 1 != st.session_state.counter:
            st.session_state.counter = page_slider - 1

        # Display images in a carousel-like format using columns
        col1, col2, col3 = st.columns([1, 10, 1])
        with col1:
            if st.session_state.counter > 0 and st.button('Prev'):
                st.session_state.counter -= 1
                st.experimental_rerun()
        with col2:
            st.image(all_images[st.session_state.counter], use_column_width=True)
        with col3:
            if st.session_state.counter < len(all_images) - 1 and st.button('Next'):
                st.session_state.counter += 1
                st.experimental_rerun()

        # Update slider position after clicking Next/Prev
        st.session_state['slider'] = st.session_state.counter + 1

    def metric_framework_key_highlights():
        st.write("### KEY HIGHLIGHTS")
        st.markdown("The following presentation provides a comprehensive overview of the RtR Metrics Framework. It is designed to guide you through the critical components and methodologies that underpin this framework. Each slide is meticulously crafted to illustrate the various dimensions and applications of these metrics, ensuring a deeper understanding of their role in effective decision-making. Whether you are a novice or an expert in this field, these slides will offer valuable insights and a structured approach to the RtR Metrics Framework.")

        # Mapping of sections to page numbers
        sections_to_pages = {
            "Introduction": 0,
            "Race to Resilience Campaign Context": 2,
            "Campaign's Metrics Framework": 8,
            "The Pathway Throught the Race": 17,
            "Data Explorer and General Results": 23,
            "Final Remarks": 27
        }

        # Selector for sections
        section = st.selectbox('Go to Section', list(sections_to_pages.keys()))

        all_images = get_pdf_images(file_path_slides)
        display_pdf_horizontal(all_images, start_page=sections_to_pages[section])
        
key_highlights()
