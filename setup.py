from setuptools import setup, find_packages

setup(
    name='mcqGenerator',
    version='0.1',
    author='Atishay Jain',
    author_email='atishayj288@@gmail.com',
    packages=find_packages(),
    install_requires=[
        'openai',
        'google',
        'langchain',
        'langchain_google_genai',
        'streamlit',
        'python-dotenv',
        'PyPDF2']
        
    
    
)