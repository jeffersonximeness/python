import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance


OUTPUT_WIDTH = 500

def main():
    st.sidebar.header('PyGram')
    st.sidebar.info('Feito 100% em Python :)')
    st.sidebar.subheader('App para aplicar filtros em imagens, utilizando a bilioteca OpenCV.')

    opcoes_menu = ['Sobre', 'Filtros']
    escolha = st.sidebar.selectbox('Escolha uma opção', opcoes_menu)

    our_image = Image.open('empty.jpg')

    if escolha == 'Sobre':
        st.title('Masterclass - visão computacional')
        st.markdown('Projeto voltado para aplicação de filtros em imagens')

    elif escolha == 'Filtros':
        st.title("Masterclass - Visão Computacional")

        st.subheader('Carregar arquivo de imagem')
        image_file = st.file_uploader('Escolha uma imagem', type = ['jpg', 'png', 'jpeg'])

        if image_file is not None:
            our_image = Image.open(image_file)
            st.sidebar.text('Imagem original')
            st.sidebar.image(our_image, width = 150)

        col1, col2 = st.beta_columns(2)

        filtros = st.sidebar.radio('Filtros', ['Original', 'Grayscale', 'Desenho', 'Sépia', 'Blur', 'Canny', 'Contraste'])

        if filtros == 'Grayscale':
            converted_image = np.array(our_image.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)

            col1.header('Original')
            col1.image(our_image, use_column_width = True)
            col2.header('Grayscale')
            col2.image(gray_image, use_column_width = True)

            if st.button('Save'):
                cv2.imwrite('donwload_photo_gray.jpg', gray_image)


        elif filtros == 'Desenho':
            converted_image = np.array(our_image.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
            inv_gray_image = 255 - gray_image
            blur_image = cv2.GaussianBlur(inv_gray_image, (21, 21), 0, 0)
            sketch_image = cv2.divide(gray_image, blur_image - 255, scale = 256)

            col1.header('Original')
            col1.image(our_image, use_column_width = True)
            col2.header('Grayscale')
            col2.image(sketch_image, use_column_width = True)

            if st.button('Save'):
                cv2.imwrite('donwload_photo_sketch.jpg', sketch_image)

        elif filtros == 'Sépia':
            converted_image = np.array(our_image.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
            kernel =  np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia_image = cv2.filter2D(converted_image, -1, kernel)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Sépia")
            col2.image(sepia_image, channels="BGR", use_column_width=True)

            if st.button('Save'):
                cv2.imwrite('donwload_photo_sepia.jpg', sepia_image)

        elif filtros == 'Blur':
            b_amount = st.sidebar.slider('Kernel (n x n)', 3, 27, 9, step = 2)
            converted_image = np.array(our_image.convert('RGB'))
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
            blur_image = cv2.GaussianBlur(converted_image, (b_amount, b_amount), 0, 0)

            col1.header("Original")
            col1.image(our_image, use_column_width = True)
            col2.header("Blur")
            col2.image(blur_image, channels = "BGR", use_column_width = True)

            if st.button('Save'):
                cv2.imwrite('donwload_photo_blur.jpg', blur_image)

        elif filtros == 'Canny':
            converted_image = np.array(our_image.convert('RGB'))
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
            blur_image = cv2.GaussianBlur(converted_image, (11, 11), 0)
            canny = cv2.Canny(blur_image, 100, 150)

            col1.header('Original')
            col1.image(our_image, use_column_width = True)
            col2.header('Canny Edge Detection')
            col2.image(canny, use_column_width = True)

            if st.button('Save'):
                cv2.imwrite('donwload_photo_canny.jpg', canny)

        elif filtros == 'Contraste':
            c_amount = st.sidebar.slider('Contraste', 0.0, 2.0, 1.0)
            enhancer = ImageEnhance.Contrast(our_image)
            contrast_image = enhancer.enhance(c_amount)

            col1.header("Original")
            col1.image(our_image, use_column_width = True)
            col2.header("Contraste")
            col2.image(contrast_image, use_column_width = True)

        elif filtros == 'Original':
            st.image(our_image, width = OUTPUT_WIDTH)

        else:
            st.image(our_image, width = OUTPUT_WIDTH)

if __name__ == "__main__":
    main()
