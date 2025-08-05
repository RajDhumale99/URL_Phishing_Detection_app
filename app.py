import streamlit as st
import machine_learning as ml
import feature_extraction as fe
from bs4 import BeautifulSoup
import requests as re
import matplotlib.pyplot as plt
import pickle

# col1, col2 = st.columns([1, 3])

# Load models
with open("svm_model.pkl", "rb") as f:
    svm_model = pickle.load(f)

with open("rf_model.pkl", "rb") as f:
    rf_model = pickle.load(f)

with open("dt_model.pkl", "rb") as f:
    dt_model = pickle.load(f)

with open("ab_model.pkl", "rb") as f:
    ab_model = pickle.load(f)

with open("nb_model.pkl", "rb") as f:
    nb_model = pickle.load(f)

with open("nn_model.pkl", "rb") as f:
    nn_model = pickle.load(f)

with open("kn_model.pkl", "rb") as f:
    kn_model = pickle.load(f)

st.title('Phishing Website Detection using Machine Learning')
st.write('Detecting phishing websites only using content data. Not URL!')


with st.expander("PROJECT DETAILS"):
    

    st.subheader('Data set')
    st.write('_"phishtank.org"_ & _"tranco-list.eu"_ as data sources.')
    st.write('Totally 41213 websites ==> **_20380_ legitimate** websites | **_20833_ phishing** websites')

    # ----- FOR THE PIE CHART ----- #
    labels = 'phishing', 'legitimate'
    phishing_rate = int(ml.phishing_df.shape[0] / (ml.phishing_df.shape[0] + ml.legitimate_df.shape[0]) * 100)
    legitimate_rate = 100 - phishing_rate
    sizes = [phishing_rate, legitimate_rate]
    explode = (0.1, 0)
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, shadow=True, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)
    # ----- !!!!! ----- #

    st.write('Features + URL + Label ==> Dataframe')
    st.markdown('label is 1 for phishing, 0 for legitimate')
    number = st.slider("Select row number to display", 0, 100)
    st.dataframe(ml.legitimate_df.head(number))


    @st.cache_data
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(ml.df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='phishing_legitimate_structured_data.csv',
        mime='text/csv',
    )

    st.subheader('Features')
    st.write('I used only content-based features. I didn\'t use url-based faetures like length of url etc.'
             'Most of the features extracted using find_all() method of BeautifulSoup module after parsing html.')

    st.subheader('Results')
    st.write('I used 7 different ML classifiers of scikit-learn and tested them implementing k-fold cross validation.'
             'Firstly obtained their confusion matrices, then calculated their accuracy, precision and recall scores.'
             'Comparison table is below:')
    st.table(ml.df_results)
    st.write('NB --> Gaussian Naive Bayes')
    st.write('SVM --> Support Vector Machine')
    st.write('DT --> Decision Tree')
    st.write('RF --> Random Forest')
    st.write('AB --> AdaBoost')
    st.write('NN --> Neural Network')
    st.write('KN --> K-Neighbours')

with st.expander('EXAMPLE PHISHING URLs:'):
    st.write('_https://rtyu38.godaddysites.com/_')
    st.write('_https://payment-error0291433.weebly.com/_')
    st.write('_https://triglhadinw.blogspot.com/_')
with st.expander('EXAMPLE LEGITIMATE URLs:'):
    st.write('_http://getbootstrap.com_')
    st.write('_http://udemy.com_')
    st.write('_http://postgresql.org_')

choice = st.selectbox("Please select your machine learning model",
                 [
                     'Gaussian Naive Bayes', 'Support Vector Machine', 'Decision Tree', 'Random Forest',
                     'AdaBoost', 'Neural Network', 'K-Neighbours'
                 ]
                )

if choice == 'Gaussian Naive Bayes':
    model = nb_model
    st.write('GNB model is selected!')
elif choice == 'Support Vector Machine':
    model = svm_model
    st.write('SVM model is selected!')
elif choice == 'Decision Tree':
    model = dt_model
    st.write('DT model is selected!')
elif choice == 'Random Forest':
    model = rf_model
    st.write('RF model is selected!')
elif choice == 'AdaBoost':
    model = ab_model
    st.write('AB model is selected!')
elif choice == 'Neural Network':
    model = nn_model
    st.write('NN model is selected!')
else:
    model = kn_model
    st.write('KN model is selected!')


url = st.text_input('Enter the URL')
# check the url is valid or not
if st.button('Check!'):
    # Check if the URL is empty
    if not url.strip():
        st.error("Please enter a URL before clicking 'Check!'")
    else:
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            st.warning("URL missing scheme. Automatically adding 'http://' prefix.")
            url = "http://" + url
        try:
            response = re.get(url, verify=False, timeout=4)
            if response.status_code != 200:
                st.error(f"Unable to verify or reach the website: {url}. It may be down or using an invalid SSL certificate.")
            else:
                soup = BeautifulSoup(response.content, "html.parser")
                vector = [fe.create_vector(soup)]  # it should be 2d array, so I added []
                result = model.predict(vector)
                if result[0] == 0:
                    st.success("✅ This web page seems a legitimate!")
                    st.balloons()
                else:
                    st.warning("⚠️ Attention! This web page is a potential PHISHING!")
                    st.snow()

        except re.exceptions.MissingSchema:
            st.error("❌ Invalid URL format. Please ensure it starts with http:// or https://")
        except re.exceptions.ConnectionError:
            st.error("❌ Connection Error. The website could not be reached. Check the domain.")
        except re.exceptions.Timeout:
            st.error("❌ Connection Timed Out. The website is not responding.")
        except re.exceptions.SSLError:
            st.error("⚠️ SSL Certificate issue. Website may be using an invalid certificate.")
        except re.exceptions.RequestException as e:
            print("--> ", e)





