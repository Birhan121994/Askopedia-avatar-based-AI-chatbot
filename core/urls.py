"""
URL patterns for the Askopedia AI Assistant.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Main page
    path('', views.home, name='home'),
    
    # Chat endpoint
    path('chat/', views.chat, name='chat'),
    
    # TTS endpoint
    path('edge-tts/', views.edge_tts_view, name='edge_tts'),

    path('transcribe-audio/', views.transcribe_audio, name='transcribe_audio'),
    
    # Test Groq API endpoint
    path('test-groq/', views.test_groq_api, name='test_groq'),
]