import streamlit as st
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model # type: ignore
import scraper as scrap

# Load the pre-trained model
model = load_model('./dogbreed_10epoch_weights.h5')

# List of dog breeds
dog_breeds = ['Boston-Bull', 'Dingo', 'Pekinese', 'Bluetick', 'Golden-Retriever',
              'Bedlington-Terrier', 'Borzoi', 'Basenji', 'Scottish-Deerhound',
              'Shetland-Sheepdog', 'Walker-Hound', 'Maltese-Dog',
              'Norfolk-Terrier', 'African-Hunting-Dog',
              'Wire-Haired-Fox-Terrier', 'Redbone', 'Lakeland-Terrier', 'Boxer',
              'Doberman', 'Otterhound', 'Standard-Schnauzer',
              'Irish-Water-Spaniel', 'Black-And-Tan-Coonhound', 'Cairn',
              'Affenpinscher', 'Labrador-Retriever', 'Ibizan-Hound',
              'English-Setter', 'Weimaraner', 'Giant-Schnauzer', 'Groenendael',
              'Dhole', 'Toy-Poodle', 'Border-Terrier', 'Tibetan-Terrier',
              'Norwegian-Elkhound', 'Shih-Tzu', 'Irish-Terrier', 'Kuvasz',
              'German-Shepherd', 'Greater-Swiss-Mountain-Dog', 'Basset',
              'Australian-Terrier', 'Schipperke', 'Rhodesian-Ridgeback',
              'Irish-Setter', 'Appenzeller', 'Bloodhound', 'Samoyed',
              'Miniature-Schnauzer', 'Brittany-Spaniel', 'Kelpie', 'Papillon',
              'Border-Collie', 'Entlebucher', 'Collie', 'Malamute',
              'Welsh-Springer-Spaniel', 'Chihuahua', 'Saluki', 'Pug', 'Malinois',
              'Komondor', 'Airedale', 'Leonberg', 'Mexican-Hairless',
              'Bull-Mastiff', 'Bernese-Mountain-Dog',
              'American-Staffordshire-Terrier', 'Lhasa', 'Cardigan',
              'Italian-Greyhound', 'Clumber', 'Scotch-Terrier', 'Afghan-Hound',
              'Old-English-Sheepdog', 'Saint-Bernard', 'Miniature-Pinscher',
              'Eskimo-Dog', 'Irish-Wolfhound', 'Brabancon-Griffon',
              'Toy-Terrier', 'Chow', 'Flat-Coated-Retriever', 'Norwich-Terrier',
              'Soft-Coated-Wheaten-Terrier', 'Staffordshire-Bullterrier',
              'English-Foxhound', 'Gordon-Setter', 'Siberian-Husky',
              'Newfoundland', 'Briard', 'Chesapeake-Bay-Retriever',
              'Dandie-Dinmont', 'Great-Pyrenees', 'Beagle', 'Vizsla',
              'West-Highland-White-Terrier', 'Kerry-Blue-Terrier', 'Whippet',
              'Sealyham-Terrier', 'Standard-Poodle', 'Keeshond',
              'Japanese-Spaniel', 'Miniature-Poodle', 'Pomeranian',
              'Curly-Coated-Retriever', 'Yorkshire-Terrier', 'Pembroke',
              'Great-Dane', 'Blenheim-Spaniel', 'Silky-Terrier',
              'Sussex-Spaniel', 'German-Short-Haired-Pointer', 'French-Bulldog',
              'Bouvier-Des-Flandres', 'Tibetan-Mastiff', 'English-Springer',
              'Cocker-Spaniel', 'Rottweiler']

def preprocess_image(uploaded_file):
    img = Image.open(uploaded_file)
    img = img.resize((224, 224))
    img_arr = np.array(img)
    img_arr = np.expand_dims(img_arr, axis=0) / 255.0
    return img_arr

def classifier(img_arr):
    pred_d = model.predict(img_arr)
    pred_labels = np.argmax(pred_d)
    st.write(pred_d)  # Print the prediction probabilities
    return pred_labels

def app():
    st.title('Dog Breed Recognition System')
    st.markdown('## Breed Identifier')
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
        img_arr = preprocess_image(uploaded_file)
        label = classifier(img_arr)
        
        breed_name = dog_breeds[label].replace('_', ' ').replace('-', ' ').title()
        st.write(f"The Breed of the Dog is {breed_name}")
        
        st.markdown('## Description of your Buddy')
        st.write(scrap.info(dog_breeds[label]))
        
        
        st.markdown('## Vital Stats')
        prop = scrap.stats(dog_breeds[label])
        st.write(f'Dog Breed Group: {prop[0]}')
        st.write(f'Height: {prop[1]}')
        st.write(f'Weight: {prop[2]}')
        st.write(f'Life Span: {prop[3]}')
        
        st.markdown('## Bring Happiness To Your Home By Adopting')
        st.write(f"[Click Here To Adopt a {breed_name}] (https://marketplace.akc.org/puppies/{breed_name.replace(' ', '-')})")
        
        st.markdown('## Get A Name Of Your New Buddy')
        gender_list = ['Male', 'Female']
        gender = st.selectbox("Select A Gender From The Dropdown", gender_list)
        name_list = scrap.name(gender)
        for i in range(0, 4):
            st.write(f"Name Option {i+1}: {name_list[i]}")

if __name__ == '__main__':
    app()
