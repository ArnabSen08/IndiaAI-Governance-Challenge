from fastapi import FastAPI
import os, requests

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'Gemini 3 Hackathon Project Running!'}