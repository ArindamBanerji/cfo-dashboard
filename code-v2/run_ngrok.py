from pyngrok import ngrok 
# !ngrok authtoken ["cr_2i80nCqqQsXqA1Nw2BRNAhCLHa0"]
# !nohup streamlit run cfo-dashboard-streamlit-complete.py & 

url = ngrok.connect(port = 8501)
url #generates our URL

# !streamlit run --server.port 80 cfo-dashboard-streamlit-complete.py >/dev/null #used for starting our server