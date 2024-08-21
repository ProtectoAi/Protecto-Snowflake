import streamlit as st
import snowflake.connector
import requests
import json
import tempfile
import os
import types
import pandas as pd
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.exceptions import SnowparkSQLException
import base64

def render_image(filepath: str):
   """
   filepath: path to the image. Must have a valid file extension.
   """
   mime_type = filepath.split('.')[-1:][0].lower()
   with open(filepath, "rb") as f:
    content_bytes = f.read()
    content_b64encoded = base64.b64encode(content_bytes).decode()
    image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
    image_html = f"""
                <div class="custom-image">
            <img src="{image_string}" alt="Protecto">
        </div>
        """
    st.markdown(image_html, unsafe_allow_html=True)

    
    #st.image(image_string)


# Constants
NETWORK_RULE_NAME = 'protecto_network_rule'
EXTERNAL_ACCESS_INTEGRATION_NAME = 'protecto_access_integration'
PROTECTO_API_URL = "https://trial.protecto.ai/api/vault/mask"


# Snowflake session
session = get_active_session()


###################################
# All Config Settings Here



if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
    
if 'network_rule_created' not in st.session_state:
    st.session_state.network_rule_created = False
    
if 'store_protecto_api_key' not in st.session_state:
    st.session_state.store_protecto_api_key = False

    
if 'store_active_subscription_status' not in st.session_state:
    st.session_state.store_active_subscription_status = False

    
if 'store_is_registered_udfs' not in st.session_state:
    st.session_state.store_is_registered_udfs = False
    
if 'store_is_helper_function' not in st.session_state:
    st.session_state.store_is_helper_function = False


# All Other UI Status
if 'store_edit_protecto_api_key' not in st.session_state:
    st.session_state.store_edit_protecto_api_key = False


data_dict = [
    {
        'Check Network Permission': 'True',
        'Procteto AI Secret': True,
        'Active Subscription': 'True',
        'Registered Function': 'True',
        'Helper Function': 'True'
    }
]





st.markdown("""
    <style>
    /* Target the label of the selectbox */
    div[data-testid="stSelectbox"] > label {
        color: #FFFFFF !important; /* Change this to any color you want */
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# Session state initialization
if 'page' not in st.session_state:
    st.session_state.page = 'home'



def create_landing_page():

    col1, col2, col3 = st.columns([1,8,1])
    
    with col2:

        # Custom CSS for styling
        st.markdown("""
        <style>
        .main {
            background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
         .protecto-vault {
            font-family: Arial, sans-serif;
            font-size: 72px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            background-color: #F0F0F5;
            border-radius: 10px;
            margin-bottom: 0;
            background-clip: text;
            color: black;
            margin-top: 0;
        }
        .stButton > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
            border-radius: 11px;         /* Rounded corners */
            padding: 10px 20px;         /* Comfortable padding */
            font-size: 16px;            /* Readable font size */
            font-weight: bold;          /* Bold text */
            cursor: pointer;            /* Hand cursor on hover */
            width: 100%;
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        
        /* Hover effect */
        .stButton > button:hover {
              background-color: white;    /* White background */
            color: #6c5ce7;             /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        /* Solid button style */
        .stButton.solid > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
        }

        
        /* Active effect */
        .stButton > button:active {
            background-color: #4a3f9f;  /* Even darker when clicked */
        }
        
        /* Style for the "Start a Free Trial" button to match the image */
        .stButton.start-trial > button {
            background-color: transparent;
            color: #6c5ce7;
            border: 2px solid #6c5ce7;
        }
        /* Outline button style */
        .stButton.outline > button {
            background-color: white;    /* White background */
            color: #6c5ce7;             /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        
        .stButton.start-trial > button:hover {
            background-color: rgba(108, 92, 231, 0.1);  /* Light purple background on hover */
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown("""<p style='text-align: center; color: grey; font-size: 1.5em; margin-bottom: 0; '>Make Your Enterprise Data</p>""", unsafe_allow_html=True)
        st.markdown("""<div class="protecto-vault">Protecto Vault</div>""", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: grey; font-size: 2.5em;'>Secure approach to data security and privacy</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: black; font-size: 1.0em;  margin-bottom: 65px;'>Protecto identifies and masks sensitive data while maintaining context and semantic meaning, ensuring accuracy in your LLMs/Gen AI apps.</p>", unsafe_allow_html=True)
        # create_status()
        # Buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            
            button_html = """
            <div style='margin-top: 10px;'> 
            <a style='
            margin-top: 9px;
            display:flex;
            align-items:center;
            justify-content:center;
            color: #FFFFFF;   
            background-color: #6c5ce7; 
            border-radius: 11px;        
            padding: 12px;         
            text-decoration: none;
            font-size: 16px;                
            cursor: pointer;           
            width: 100%;
            transition: background-color 0.3s ease;' 
            href="https://www.protecto.ai/schedule-a-demo" class="github-button" target="_blank"">
                BOOK DEMO
            </a>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
        with col2:
            button_html = """
            <div style='margin-top: 10px;'> 
            <a style='
            margin-top: 9px;
            align-items:center;
            justify-content:center;
            display:flex;
            color: #FFFFFF;   
            background-color: #6c5ce7; 
            border-radius: 11px;        
            padding: 12px;         
            text-decoration: none;
            font-size: 16px;                
            cursor: pointer;           
            width: 100%;
            transition: background-color 0.3s ease;' 
            href="https://trial.protecto.ai/trial/tokenization/mask-unmask" class="github-button" target="_blank"">
                START TRAIL
            </a>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)
        with col3:
            button_html = """
            <div style='margin-top: 10px;'> 
            <a style='
            margin-top: 9px;
            display:flex;
            align-items:center;
            justify-content:center;
            color: #FFFFFF;   
            background-color: #6c5ce7; 
            border-radius: 11px;        
            padding: 12px;         
            text-decoration: none;
            font-size: 16px;                
            cursor: pointer;           
            width: 100%;
            transition: background-color 0.3s ease;' 
            href="https://developer.protecto.ai/docs/welcome-to-protecto/" class="github-button" target="_blank"">
                PROTECTO API
            </a>
            </div>
            """
            st.markdown(button_html, unsafe_allow_html=True)


        css = """
        <style>
            .custom-image {
                margin-top: 30px;  /* Adjust the top margin */
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .custom-image img {
                border-radius: 10px;  /* Add rounded corners */
                max-width: 100%;  /* Ensure the image scales with the column width */
            }
            .custom-caption {
                margin-top: 10px;
                font-size: 1.2em;
                color: grey;
            }
        </style>
        """
        
        # Inject the CSS into the Streamlit app
        st.markdown(css, unsafe_allow_html=True)
        image_path = os.path.join("assets", "home.webp")
        render_image(image_path)
    #     image_html = """
    #         <div class="custom-image">
    #     <img src="home.webp" alt="Protecto">
    #   </div>
    #    """
    #     st.markdown(image_html, unsafe_allow_html=True)
        
    # Background effect (simplified)
    st.markdown("""
    <div style='position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2;'>
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <circle cx="10%" cy="10%" r="5" fill="#FFA500" />
            <circle cx="90%" cy="20%" r="3" fill="#FFD700" />
            <circle cx="30%" cy="80%" r="4" fill="#40E0D0" />
            <circle cx="70%" cy="90%" r="6" fill="#40E0D0" />
        </svg>
    </div>
    """, unsafe_allow_html=True)





def home_page():
    create_landing_page()
    

def engage_help_page():
    
    st.markdown("""
        <style>
            .main {
            color: black !important;
            background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
            background-repeat: no-repeat;
            background-attachment: fixed;
            }
             .protecto-vault {
                color: black;  
                font-family: Arial, sans-serif;
                font-size: 72px;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                background-color: #F0F0F5;
                border-radius: 10px;
                margin-bottom: 0;
                background-clip: text;
                margin-top: 0;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""<div style='color: black; text-align: center; font-size: 70px; font-weight: bold;'>Protecto Vault</div>""", unsafe_allow_html=True)
    st.markdown("""<div style='margin-top: 10px;'></div>""", unsafe_allow_html=True)


    # Adding custom CSS for the expander label
    st.markdown("""
        <style>
        .section-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background-color: #2E2E3E;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .section-title {
            color: #707CED;
            font-size: 20px;
            font-weight: bold;
            margin: 0;
        }
        .stExpander {
            color: black !important;
        }
        .stSelectbox {
            color: black !important;
        }
        </style>
        """, unsafe_allow_html=True)
    st.markdown("""<p style='color: black; margin-bottom: 0; font-size: 25px; text-align: center; font-weight: bold;'>Select API Type</p>""", unsafe_allow_html=True)
    option = st.selectbox(
        "",
        ("Tokenization", "DataScan", "Custom PII Identification"),
    )
    if option == "Tokenization":
            
        st.markdown("<h6 style='color: black; text-align: center; margin-top: 15px'>Tokenization Packages </h6>", unsafe_allow_html=True)
        st.markdown("""<div style='color: black;'>""", unsafe_allow_html=True)
        with st.expander("See explanation", expanded=True):
            # Sample data to be displayed
    
      
            functions_data = [
                {"name": "PROTECTO_MASK", "description": "Masks the provided data values", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#1-protecto_mask"},
                {"name": "PROTECTO_UNMASK", "description": "Unmasks the provided masked token", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#2-protecto_unmask"},
                {"name": "PROTECTO_ASYNC_MASK", "description": "Asynchronously masks the provided data values", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#3-protecto_async_mask"},
                {"name": "PROTECTO_ASYNC_MASK_RESULT", "description": "Retrieves the result of an asynchronous mask operation", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#4-protecto_async_mask_result"},
                {"name": "PROTECTO_ASYNC_UNMASK", "description": "Asynchronously unmasks the provided masked values", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#5-protecto_async_unmask"},
                {"name": "PROTECTO_ASYNC_UNMASK_RESULT", "description": "Retrieves the result of an asynchronous unmask operation.", "action": "Docs", "link": "https://github.com/viveksrinivasanss/Protecto-Snowflake/blob/main/docs/tokenization.md#6-protecto_async_unmask_result"}

            ]
            
            # Custom CSS for styling
            st.markdown("""
                <style>
                 
    
                </style>
                """, unsafe_allow_html=True)
            
            
            # Header row
            header_col1, header_col2, header_col3 = st.columns([3, 3, 1])
            header_col1.markdown("""<h5 style='color: black; font-size: 16px;'>Function Name</h5>""", unsafe_allow_html=True)
            header_col2.markdown("""<h5 style='color: black; font-size: 16px;'>Description</h5>""", unsafe_allow_html=True)
            header_col3.markdown("""<h5 style='color: black; font-size: 16px;'>Action</h5>""", unsafe_allow_html=True)
            
            # Function rows
            for function in functions_data:
                # Create a new row for each function
                col1, col2, col3 = st.columns([2, 3, 1])
    
                st.markdown("""<div style='background-color: black;'>""", unsafe_allow_html=True)
                # Display the function name and description
                col1.markdown(f"""<p style='color: #2f2f2f;'>{function["name"]}</p>""", unsafe_allow_html=True)
                col2.markdown(f"""<p style='color: #2f2f2f;'>{function["description"]}</p>""", unsafe_allow_html=True)
                st.markdown("""</div>""", unsafe_allow_html=True)
                
                # Create a button for the action
                col3.markdown(f"""<a href={function["link"]} class="github-button" target="_blank" style='text-decoration: none; background-color: #6c5ce7; color: white; border: none; border-radius: 4px; padding: 8px 17px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; transition: background-color 0.3s ease;'>{function["action"]}</a>""", unsafe_allow_html=True)
          
            st.markdown(
       """
        <style>
     .main {
            background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: black;
        }
    
        /* Protecto Vault title */
        .protecto-vault {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            margin-bottom: 0px;
            background-image: linear-gradient(to right, #707CED, #FFD700);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            color: transparent;
        }
    
        /* Main title */
        .main-title {
            font-size: 24px;
            font-weight: bold;
            color: #FFFFFF;
            text-align: center;
            margin-bottom: 5px;
        }
    
        /* Subtitle */
        .subtitle {
            font-size: 16px;
            color: #A0AEC0;
            text-align: center;
            margin-left: 20px;
            margin-right: 20px;
        }
    
        /* Section title */
        .section-title {
            text-align: center;
            color: #707CED;
            font-size: 40px;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
        }
    
        /* Configuration button */
        .config-btn {
            text-align: center;
        }
    
        
    
        /* Input fields and select boxes */
        input, select {
            background-color: #2E2E3E;
            color: #FFFFFF;
            border: 1px solid #707CED;
            border-radius: 5px;
            padding: 5px 10px;
        }
    
      
        </style>
        """, unsafe_allow_html=True)
            
        if option != "Tokenization":
            st.markdown("""<div style='margin-top: 10px;'></div>""", unsafe_allow_html=True)
            st.markdown("<h6 style='color: black; text-align: center;'>DataScan API </h6>", unsafe_allow_html=True)
            with st.expander("See explanation"):
                st.markdown("""<h5 style='color: black; font-size: 14px;'>Coming Soon</h5>""", unsafe_allow_html=True)
                
            st.markdown("""<div style='margin-top: 10px;'></div>""", unsafe_allow_html=True)
            st.markdown("<h6 style='color: black; text-align: center;'>Custom PII Identification API's </h6>", unsafe_allow_html=True)
            with st.expander("See explanation"):
                st.markdown("""<h5 style='color: black; font-size: 14px;'>Coming Soon</h5>""", unsafe_allow_html=True)
                
            st.markdown("""</div>""", unsafe_allow_html=True)
            css = """
                <style>
                    .custom-image {
                        margin-top: 30px;  /* Adjust the top margin */
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    .custom-image img {
                        border-radius: 10px;  /* Add rounded corners */
                        max-width: 100%;  /* Ensure the image scales with the column width */
                    }
                    .custom-caption {
                        margin-top: 10px;
                        font-size: 1.2em;
                        color: grey;
                    }
                </style>
                """
                
            # Inject the CSS into the Streamlit app
            st.markdown(css, unsafe_allow_html=True)
            image_html = """
                <div class="custom-image">
                    <img src="https://cdn.prod.website-files.com/62be995b7dfee4507a69ddff/666bd26d15e9b1ad0c43ffef_Protecto%20Vault%20for%20Gen%20AI.webp" alt="Protecto">
                </div>
                """
            st.markdown(image_html, unsafe_allow_html=True)

    else:
        st.markdown("""<h5 style='color: black; font-size: 14px;'>Coming Soon</h5>""", unsafe_allow_html=True)
        





# The Setup Page
def setup_page():

    st.markdown(
   """
    <style>
    .main {
      
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    
    /* Protecto Vault title */
    .protecto-vault {
        color: black;
        font-size: 55px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        margin-bottom: 0px;
        background-clip: text;
    }

    /* Main title */
    .main-title {
        font-size: 24px;
        font-weight: bold;
        color: #171D45;
        text-align: center;
        margin-bottom: 5px;
    }

    /* Subtitle */
    .subtitle {
        font-size: 16px;
        color: #171D45;
        text-align: center;
        margin-left: 20px;
        margin-right: 20px;
    }

    /* Section title */
    .section-title {
        text-align: center;
        color: #707CED;
        font-size: 20px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }


  

    /* Input fields and select boxes */
    input, select {
        background-color: #2E2E3E;
        color: #FFFFFF;
        border: 1px solid #707CED;
        border-radius: 5px;
        padding: 6px 10px;
    }

    /* Code blocks */
    pre, code {
        background-color: #2E2E3E;
        color: #FFFFFF;
        border-radius: 5px;
        padding: 10px;
        font-family: monospace;
    }




    </style>
    """, unsafe_allow_html=True)
    
    html_content = """
    <div class="protecto-vault">Setup Steps</div>
    """
    
    html_content_des = """
    <div class="title-container">
        <div class="subtitle">Setup Your Account Using Following Steps</div>
    </div>
    """
    full_html = html_content
    # st.markdown("<h1 class='main-title'>Protecto</h1>", unsafe_allow_html=True)
    st.markdown(full_html, unsafe_allow_html=True)
    st.markdown(html_content_des, unsafe_allow_html=True)
    st.markdown("""
    <style>
        .section-container {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 10px 20px;
            background-color: #2E2E3E;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .section-title {
            color: #707CED;
            font-size: 20px;
            font-weight: bold;
            margin: 0;
        }
        .custom-button {
            background-image: linear-gradient(to right, #707CED, #FFD700);
            color: #1E1E2E;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }
        .custom-button:hover {
            opacity: 0.8;
        }
        .custom-disabled-button {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: none;
            border-radius: 20px;
            padding: 10px 20px;
            font-weight: bold;
            cursor: not-allowed;
        }
        .tick-mark {
            margin-right: 8px;
            font-size: 18px;
        }
        .documentation {
            margin-bottom: 10px;
            font-style: italic;
            color: #555;
            text-align: center;
    }
        
    </style>
    """, unsafe_allow_html=True)

    protecto_api_key_input, protecto_api_key_generate_btn = st.columns([5, 2])
    st.markdown("""
    <style>
    .stButton > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
            border-radius: 4px;         /* Rounded corners */
            padding: 8px 17px;         /* Comfortable padding */
            font-size: 16px;            /* Readable font size */
            font-weight: bold;          /* Bold text */
            cursor: pointer;            /* Hand cursor on hover */
            width: 100%;
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        
        /* Hover effect */
        .stButton > button:hover {
            background-color: white;    /* White background */
            color: #6c5ce7;       
            padding: 8px 15px;   /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        /* Solid button style */
        .stButton.solid > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
        }

        
        /* Active effect */
        .stButton > button:active {
            background-color: #4a3f9f;  /* Even darker when clicked */
        }
        
        /* Style for the "Start a Free Trial" button to match the image */
        .stButton.start-trial > button {
            background-color: transparent;
            color: #6c5ce7;
            border: 2px solid #6c5ce7;
        }
        /* Outline button style */
        .stButton.outline > button {
            background-color: white;    /* White background */
            color: #6c5ce7;             /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        
        .stButton.start-trial > button:hover {
            background-color: rgba(108, 92, 231, 0.1);  /* Light purple background on hover */
        }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div style="margin-top: 26.5px; border-radius: 5px;"></div>', unsafe_allow_html=True)
    st.markdown("<p style='font-size: 14px; margin-bottom: 0; text-align: left; font-size: 18px; color: black;'>Step 1. Get Protecto API Key</p>", unsafe_allow_html=True)
    # Adding the generate button
    url_to_open = """https://trial.protecto.ai"""
    st.markdown("""
        <style>

        .docs-container {
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: purple(10px);
            margin-top: 0;
            width: 100%;
        }
                
        .main-title-docs {
            color: white;        
            font-weight: bold;
            font-size: 24px;
            text-align: center;
        }

        .subtitle-docs {
            color: white;  
            text-align: center;  
            margin-bottom: 20px;
        }
                
      .github-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #24292e;
        color: white;
        padding: 10px 10px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        transition: background-color 0.3s;
        text-align: center;
        margin: 0 auto;  /* This centers the button horizontally */
    }
    .github-button:hover {
        background-color: #5c5c5c;
        text-decoration: none;
    }
    .github-icon {
        margin-right: 10px;
    }
    .btn-github {
        margin: 0;
        padding: 0;
    }

        </style>
        """, unsafe_allow_html=True)
    the_website, to_protecto = st.columns([5,2])
    Path = f'''{url_to_open}'''
    the_website.code(Path, language="python")
    button_html = """
            <div style='margin-top: 0px;'> 
            <a style='
            display:flex;
            align-items:center;
            justify-content:center;
            color: #FFFFFF;   
            background-color: #6c5ce7; 
            border-radius: 4px;        
            padding: 12px;
            font-weight: normal;
            text-decoration: none;
            font-size: 14px;                
            cursor: pointer;           
            width: 100%;
            transition: background-color 0.3s ease;' 
            href="https://trial.protecto.ai" class="github-button" target="_blank"">
                Visit
            </a>
            </div>
            """
    to_protecto.markdown(button_html, unsafe_allow_html=True)
    
    
    
    st.markdown("<p style='font-size: 14px; margin-bottom: 0px; color: black; text-align: left; font-size: 18px; margin-top: 30px;'>Step 2. Create Protecto Secret </p>", unsafe_allow_html=True)
    
    protecto_api_key_input, protecto_api_key_generate_btn = st.columns([5, 2])
    st.markdown("""
    <style>
    .st-emotion-cache-1vo7ujy {
             color: white; 
        }
    .stButton > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
            border-radius: 4px;         /* Rounded corners */
            padding: 8px 17px;         /* Comfortable padding */
            font-size: 16px;            /* Readable font size */
            font-weight: bold;          /* Bold text */
            cursor: pointer;            /* Hand cursor on hover */
            width: 100%;
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        
        /* Hover effect */
        .stButton > button:hover {
            background-color: white;    /* White background */
            color: #6c5ce7;       
            padding: 8px 15px;   /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        /* Solid button style */
        .stButton.solid > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
        }

        
        /* Active effect */
        .stButton > button:active {
            background-color: #4a3f9f;  /* Even darker when clicked */
        }
        
        /* Style for the "Start a Free Trial" button to match the image */
        .stButton.start-trial > button {
            background-color: transparent;
            color: #6c5ce7;
            border: 2px solid #6c5ce7;
        }
        /* Outline button style */
        .stButton.outline > button {
            background-color: white;    /* White background */
            color: #6c5ce7;             /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        
        .stButton.start-trial > button:hover {
            background-color: rgba(108, 92, 231, 0.1);  /* Light purple background on hover */
        }
        </style>
    """, unsafe_allow_html=True)
    
    

    role_to_be_granted = protecto_api_key_input.text_input(label="", label_visibility="hidden", placeholder="Enter Protecto Auth Key", key="text-input-generation")
    protecto_api_key_generate_btn.markdown('<div style="margin-top: 26.5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

    # Adding the generate button
    generate_btn_click = protecto_api_key_generate_btn.button("Generate", key="api-key-generation")
    if generate_btn_click and role_to_be_granted:
        code_snippet = f"""\n
        USE DATABASE protecto_vault;
        USE SCHEMA vault_schema;
        CREATE OR REPLACE SECRET protecto_secret
        TYPE = GENERIC_STRING
        SECRET_STRING = '{role_to_be_granted}';"""

        st.code(code_snippet, language="python")

       
    st.markdown("""<div class="documentation">
    Execute as ACCOUNTADMIN
    </div>""", unsafe_allow_html=True)

    st.markdown("<p style='font-size: 14px; margin-bottom: 0px; color: black; text-align: left; font-size: 18px; margin-top: 30px;'>Step 3. Assign To New Role</p>", unsafe_allow_html=True)
    
    role_input, role_generate_btn = st.columns([5, 2])
    st.markdown("""
    <style>
    .stButton > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
            border-radius: 4px;         /* Rounded corners */
            padding: 8px 17px;         /* Comfortable padding */
            font-size: 16px;            /* Readable font size */
            font-weight: bold;          /* Bold text */
            cursor: pointer;            /* Hand cursor on hover */
            width: 100%;
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        
        /* Hover effect */
        .stButton > button:hover {
            background-color: white;    /* White background */
            color: #6c5ce7;       
            padding: 8px 15px;   /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        /* Solid button style */
        .stButton.solid > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
        }

        
        /* Active effect */
        .stButton > button:active {
            background-color: #4a3f9f;  /* Even darker when clicked */
        }
        
        /* Style for the "Start a Free Trial" button to match the image */
        .stButton.start-trial > button {
            background-color: transparent;
            color: #6c5ce7;
            border: 2px solid #6c5ce7;
        }
        /* Outline button style */
        .stButton.outline > button {
            background-color: white;    /* White background */
            color: #6c5ce7;             /* Purple text */
            border: 2px solid #6c5ce7;  /* Purple border */
        }
        
        .stButton.start-trial > button:hover {
            background-color: rgba(108, 92, 231, 0.1);  /* Light purple background on hover */
        }
        </style>
    """, unsafe_allow_html=True)
    
    role_to_be_granted = role_input.text_input(label="Step 3. Assign To New Role", label_visibility="hidden", placeholder="Enter Role Name")
    role_generate_btn.markdown('<div style="margin-top: 26.5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

    # Adding the generate button
    generate_btn_click = role_generate_btn.button("Generate")
    
    
    if generate_btn_click and role_to_be_granted:
        code_snippet = f"""\n
        # To Grant Access to {role_to_be_granted}
        GRANT ROLE Protecto_role TO ROLE {role_to_be_granted};"""
        st.code(code_snippet, language="python")
   
    st.markdown("""<div class="documentation" style=''>
    Execute as ACCOUNTADMIN
    </div>""", unsafe_allow_html=True)
    
    css = """
        <style>
            .custom-image {
                margin-top: 30px;  /* Adjust the top margin */
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .custom-image img {
                border-radius: 10px;  /* Add rounded corners */
                max-width: 100%;  /* Ensure the image scales with the column width */
            }
            .custom-caption {
                margin-top: 10px;
                font-size: 1.2em;
                color: grey;
            }
        </style>
        """
        
    # Inject the CSS into the Streamlit app
    st.markdown(css, unsafe_allow_html=True)

    

    image_html = f"""
    <div style='text-align: center;'>
        <img src="https://i.ibb.co/Pzcyv87/Screenshot-2024-08-06-at-11-00-11-AM.png" style="width: 100%; height: 300px; object-fit: cover;">
    </div>
    """
            
    st.markdown("""<p style='font-size: 14px; margin-bottom: 0px; color: black; text-align: left; font-size: 18px; margin-top: 30px;'>Step 4. Signin to <a style='text-decoration: none;' href="https://www.snowflake.com/en/" target="_blank">Snowflake</a>  ➜  Create a New SQL Notebook \n  ➜  Execute the Script</p>""", unsafe_allow_html=True)


    css = """
        <style>
            .custom-image {
                margin-top: 30px;  /* Adjust the top margin */
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
            }
            .custom-image img {
                border-radius: 10px;  /* Add rounded corners */
                max-width: 100%;  /* Ensure the image scales with the column width */
            }
            .custom-caption {
                margin-top: 10px;
                font-size: 1.2em;
                color: grey;
            }
        </style>
        """
        
    # Inject the CSS into the Streamlit app
    st.markdown(css, unsafe_allow_html=True)
    image_path = os.path.join("assets", "worksheet.png")
    render_image(image_path)
    # image_html = """
    #   <div class="custom-image">
    #     <img src="https://i.postimg.cc/GmfJxggY/Group-427318928.png" alt="Protecto">
    #   </div>
    # """
    
    
    # # Display the video in Streamlit
    # st.markdown(image_html, unsafe_allow_html=True)
    
    
   
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    .button-container {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    .custom-disabled-button {
        display: inline-flex;
        align-items: center;button
        justify-content: center;
        padding: 10px 20px;
        background-color: #000000;
        color: #FFFFFF;
        border: none;
        border-radius: 4px;
        font-size: 16px;
        cursor: not-allowed;
        transition: background-color 0.3s;
        border-radius: 50px;
    }
    .tick-mark {
        margin-right: 8px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    st.markdown("""
    <style>
    .network-rule-button {
    padding: 15px 32px;
    text-align: center;
    background-color: #4CAF50;
    border: none;
    color: white;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 5px;
    }
    
    .network-rule-button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    
    .network-rule-button.remove {
        background-color: #f44336;
    }
    
    .network-rule-button.remove:hover {
        background-color: #d32f2f;
    }

    .section-title { 
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)

                
           
def document_page():
    st.markdown("""<h1 style='font-family: Arial, sans-serif;font-size: 55px; font-weight: bold; text-align: center; padding: 10px;  border-radius: 10px; margin-bottom: 0px; color: black;'>Documentation</h1>""", unsafe_allow_html=True)
    st.markdown("""
        <style>
      .main {
        background: linear-gradient(180deg, #f7f7ff, #e0e7ff);
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
        .docs-container {
            background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
            border-radius: 10px;
            padding: 30px;
            backdrop-filter: blur(10px);
            margin: 20px 0;
        }
                
        .main-title-docs {
            color: white;        
            font-weight: bold;
            font-size: 24px;
            text-align: center;
        }

        .subtitle-docs {
            color: white;  
            text-align: center;  
            margin-bottom: 20px;
        }
                
      .github-button {
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #24292e;
        color: white;
        padding: 10px 10px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        transition: background-color 0.3s;
        text-align: center;
        margin: 0 auto;  /* This centers the button horizontally */
    }
    .github-button:hover {
        background-color: #5c5c5c;
    }
    .github-icon {
        margin-right: 10px;
    }
    .btn-github {
        margin: 0;
        padding: 0;
    }

        </style>
        """, unsafe_allow_html=True)

    # HTML content for the docs section
    html_content = """
    <div class="docs-container">
        <div class="main-title-docs">Refer the Documentation</div>
        <div class="subtitle-docs">Unlock the full potential of your data while effortlessly ensuring data privacy and security - all with the simplicity of an API.</div>
           <a href="https://github.com/viveksrinivasanss/Protecto-Snowflake" class="github-button" target="_blank">
            <svg class="github-icon" height="32" aria-hidden="true" viewBox="0 0 16 16" version="1.1" width="32" data-view-component="true">
                <path fill="white" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
            </svg>
            <p class="btn-github">Do Docs</p>
        </a>
    </div>
    """
        
    st.markdown(html_content, unsafe_allow_html=True)
   
def main():
    st.markdown("""
    <style>
        /* Custom background for sidebar */
        [data-testid=stSidebar] {
            background-color: #000221;
            background-attachment: fixed;
            background-size: cover;
        }
        
        /* Ensure content in sidebar is visible */
        [data-testid=stSidebar] > div:first-child {
            background-color: #000221;
            padding: 2rem 1rem;
            height: 100vh;
        }

        /* Logo image styling */
        .sidebar-logo {
            display: flex;
            justify-content: center;
            padding-bottom: 1rem;
        }
        .sidebar-logo img {
            width: 130px;
            height: 80px;
            object-fit: contain;
        }

       .stButton > button {
            background-color: #6c5ce7;  /* Purple background */
            color: white;               /* White text */
            border: none;               /* Remove default border */
            border-radius: 5px;         /* Rounded corners */
            padding: 10px 20px;         /* Comfortable padding */
            font-size: 16px;            /* Readable font size */
            font-weight: bold;          /* Bold text */
            cursor: pointer;            /* Hand cursor on hover */
            transition: background-color 0.3s ease;  /* Smooth transition for hover effect */
        }
        .stButton > button:hover {
            background-color: #5649c0;
        }
        .stButton > button:active {
            transform: translateY(2px);
        }
        
        /* Style for buttons */
        .stButton-one > button {
            width: 100%;
            border: 1px solid #E0E0E0;
            border-radius: 4px;
            padding: 10px 15px;
            transition: all 0.3s;
            background-color: rgba(255, 255, 255, 0.7);
            color: #4B68FF;
            font-size: 18px;
            font-weight: 500;
            margin-bottom: 10px;
        }
        .stButton-one > button:hover {
            background-color: rgba(75, 104, 255, 0.1);
        }
        .stButton-one > button:active {
            background-color: #4B68FF;
            color: white;
        }
        
    
    </style>
    """, unsafe_allow_html=True)
   
    custom_sidebar_css = """
    <style>
        .sidebar .stButton > button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-bottom: 10px;
            transition: background-color 0.3s;
        }
        .sidebar .stButton > button:hover {
            background-color: #45a049;
        }
        .sidebar-logo {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """
    
    # Inject custom CSS
    st.markdown(custom_sidebar_css, unsafe_allow_html=True)
    
    
    # Initialize session state for current page
    def change_page(page):
        st.session_state.current_page = page

    # Sidebar content
    with st.sidebar:
        # Add logo

        filepath = os.path.join("assets", "logo.png")
        mime_type = filepath.split('.')[-1:][0].lower()
        with open(filepath, "rb") as f:
            content_bytes = f.read()
            content_b64encoded = base64.b64encode(content_bytes).decode()
            image_string = f'data:image/{mime_type};base64,{content_b64encoded}'
            image_html = f"""
                        <div class="custom-image">
                    <img src="{image_string}"alt="Logo" width="190" height="140"></div>>
                </div>
                """
        st.markdown(image_html, unsafe_allow_html=True)

        #st.markdown('<div class="sidebar-logo"><img src="https://i.postimg.cc/NyJc67wq/oie-DBP9i-CBL61-C8.png" alt="Logo" width="190" height="140"></div>', unsafe_allow_html=True)
        
        # Create buttons for navigation
        st.markdown('<div class="sidebar-nav-sidebar-here">', unsafe_allow_html=True)
        
        pages = ['Home', 'Setup', 'Vault', 'Docs']
        for page in pages:
            
            active_class = 'active' if st.session_state.current_page == page else ''
            
            if st.button(page, key=f"nav-{page}", help=f"Navigate to {page}", 
                         use_container_width=True, 
                         type="secondary" if st.session_state.current_page != page else "primary"):
                st.session_state.current_page = page
                change_page(page)
                # st.toast(f"""Selected Page: {page}""", icon = "⚡️")
                # st.toast(f"""Page: {st.session_state.current_page} -> {active_class}""", icon = "⚡️")
        
        st.markdown('</div>', unsafe_allow_html=True)
    

    # JavaScript for handling button clicks
    st.markdown("""
    <script>
    function handleClick(page) {
        // Update session state
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            name: 'current_page',
            value: page
        }, '*');
        
        // Trigger re-run
        window.parent.postMessage({type: 'streamlit:forceRerun'}, '*');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Main content area
    # st.write(f"Current page: {st.session_state.current_page}")

    # Display the selected page
    if st.session_state.current_page == 'Home':
        home_page()
    elif st.session_state.current_page == 'Setup':
        setup_page()
    elif st.session_state.current_page == 'Vault':
        engage_help_page()
    elif st.session_state.current_page == 'Docs':
        document_page()



if __name__ == "__main__":
    main()