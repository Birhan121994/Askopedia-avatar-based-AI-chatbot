"""
Views for the Askopedia AI Assistant.
"""
import json
import os
import asyncio
import tempfile
import requests
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

# Import for TTS
from gtts import gTTS
import edge_tts
import edge_tts.communicate as edge_comm


# Groq API configuration
GROQ_API_KEY = settings.GROQ_API_KEY
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'


def home(request):
    """
    Main page view that renders the AI Assistant interface.
    """
    return render(request, 'index.html')


@csrf_exempt
@require_POST
def chat(request):
    """
    Handle chat messages from the frontend.
    Returns AI-generated response as JSON.
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message')
        language = data.get('language', 'en')
        
        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)
        
        # Get chatbot response from Groq API
        bot_response = get_chatbot_response(user_message, language)
        
        return JsonResponse({'message': bot_response})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(f"Chat error: {e}")
        return JsonResponse({'error': str(e)}, status=500)


def get_chatbot_response(message, language='en'):
    """Get response from Groq API using direct HTTP request"""
    try:
        # System prompts for different languages
        system_prompt = "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
        
        if language == 'am':
            system_prompt = "You are a helpful AI assistant that responds in Amharic. Provide clear, concise, and helpful responses in Amharic."
        
        # Headers for Groq API
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Request payload
        payload = {
            'model': 'openai/gpt-oss-120b',
            'messages': [
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': message
                }
            ],
            'temperature': 0.7,
            'max_tokens': 1024,
            'top_p': 1,
            'stream': False
        }
        
        # Make request to Groq API
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        elif response.status_code == 401:
            print("Invalid Groq API key. Please update your API key.")
            return get_fallback_response(language, "invalid_key")
        else:
            print(f"Groq API error: {response.status_code} - {response.text}")
            
            # Try alternative model
            payload['model'] = 'mixtral-8x7b-32768'
            response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return get_fallback_response(language)
        
    except requests.exceptions.Timeout:
        print("Groq API timeout")
        return get_fallback_response(language, "timeout")
    except requests.exceptions.ConnectionError:
        print("Groq API connection error")
        return get_fallback_response(language, "connection")
    except Exception as e:
        print(f"Groq API error: {e}")
        return get_fallback_response(language)


def get_fallback_response(language='en', error_type='general'):
    """Get fallback response when Groq API fails"""
    if language == 'am':
        if error_type == "invalid_key":
            return "ይቅርታ፣ የ AI አገልግሎት ቁልፍ ልክ ያልሆነ ነው። እባክዎ አስተዳዳሪውን ያነጋግሩ።"
        elif error_type == "timeout":
            return "ይቅርታ፣ ምላሽ ለመስጠት ጊዜው አልፎብናል። እባክዎ ቆይተው እንደገና ይሞክሩ።"
        elif error_type == "connection":
            return "ይቅርታ፣ ከአገልጋዩ ጋር መገናኘት አልተቻለም። የበይነመረብ ግንኙነትዎን ያረጋግጡ።"
        else:
            return "ይቅርታ፣ አሁን ማገልገል አልቻልኩም። እባክዎ ቆይተው እንደገና ይሞክሩ።"
    else:
        if error_type == "invalid_key":
            return "I'm sorry, the AI service is not properly configured. Please contact the administrator."
        elif error_type == "timeout":
            return "I'm sorry, the request timed out. Please try again."
        elif error_type == "connection":
            return "I'm sorry, I couldn't connect to the AI service. Please check your internet connection."
        else:
            return "I'm sorry, I'm having trouble responding right now. Please try again later."


async def generate_edge_tts_audio(text, voice, output_file):
    """Generate audio using Edge TTS with enhanced error handling"""
    try:
        # Clean up text for better TTS
        text = text.replace('**', '').replace('*', '').replace('#', '')
        
        # Create Edge TTS communicate object with proper parameters
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="+0%",
            volume="+0%",
            pitch="+0Hz"
        )
        
        # Save the audio file
        await communicate.save(output_file)
        
        # Verify the file was created successfully
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Edge TTS generated file: {os.path.getsize(output_file)} bytes")
            return True
        else:
            print("Edge TTS generated empty file")
            return False
            
    except Exception as e:
        print(f"Edge TTS generation error: {e}")
        return False


def generate_edge_tts_audio_sync(text, voice, output_file):
    """Generate audio using Edge TTS with synchronous approach"""
    try:
        # Clean up text for better TTS
        text = text.replace('**', '').replace('*', '').replace('#', '')
        
        # Try to use edge-tts with subprocess for better reliability
        import subprocess
        import sys
        
        # Create a temporary Python script to run edge-tts
        script_content = f"""
import asyncio
import edge_tts

async def main():
    communicate = edge_tts.Communicate("{text}", "{voice}")
    await communicate.save("{output_file}")

asyncio.run(main())
"""
        
        # Write script to temporary file
        script_path = output_file + '_script.py'
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Run the script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Clean up script file
        if os.path.exists(script_path):
            os.remove(script_path)
        
        # Check if audio file was created
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"Edge TTS (subprocess) generated file: {os.path.getsize(output_file)} bytes")
            return True
        else:
            print(f"Edge TTS (subprocess) failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Edge TTS (subprocess) error: {e}")
        return False


def generate_google_tts_audio(text, output_file, language='en'):
    """Generate audio using Google TTS as fallback"""
    try:
        # Clean up text for better TTS
        text = text.replace('**', '').replace('*', '').replace('#', '')
        
        # Determine language code
        lang_code = 'am' if language == 'am' else 'en'
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(output_file)
        return True
    except Exception as e:
        print(f"Google TTS error: {e}")
        return False


def edge_tts_view(request):
    """TTS endpoint with Edge TTS as priority"""
    text = request.GET.get('text', '')
    voice = request.GET.get('voice', 'en-US-AriaNeural')
    lang = request.GET.get('lang', 'en')
    
    if not text:
        return HttpResponse("No text provided", status=400)
    
    temp_path = None
    tts_service_used = "Unknown"
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        print("=" * 60)
        print("TTS REQUEST:")
        print(f"Text: {text[:100]}...")
        print(f"Voice: {voice}")
        print(f"Language: {lang}")
        print("-" * 60)
        
        # TRY EDGE TTS FIRST (PRIORITY)
        print("1. Attempting Edge TTS (primary)...")
        edge_success = asyncio.run(generate_edge_tts_audio(text, voice, temp_path))
        
        if edge_success:
            print("✓ Edge TTS successful!")
            tts_service_used = "Edge TTS"
        else:
            print("✗ Edge TTS failed, trying subprocess method...")
            edge_success = generate_edge_tts_audio_sync(text, voice, temp_path)
            
            if edge_success:
                print("✓ Edge TTS (subprocess) successful!")
                tts_service_used = "Edge TTS (subprocess)"
            else:
                print("✗ Edge TTS (subprocess) failed, falling back to Google TTS...")
                google_success = generate_google_tts_audio(text, temp_path, lang)
                
                if google_success:
                    print("✓ Google TTS successful (fallback)")
                    tts_service_used = "Google TTS (fallback)"
                else:
                    print("✗ All TTS methods failed!")
                    if temp_path and os.path.exists(temp_path):
                        os.unlink(temp_path)
                    return HttpResponse("Error generating speech", status=500)
        
        # Serve the audio file
        if temp_path and os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            
            if file_size > 0:
                print(f"Audio generated: {file_size} bytes")
                print(f"Service used: {tts_service_used}")
                print("=" * 60)
                
                with open(temp_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='audio/mpeg')
                    response['Content-Disposition'] = 'attachment; filename="speech.mp3"'
                    response['Content-Length'] = file_size
                    response['Cache-Control'] = 'no-cache'
                    response['X-TTS-Service'] = tts_service_used
                
                # Clean up temporary file
                os.unlink(temp_path)
                
                return response
            else:
                print("✗ Audio file is empty!")
                os.unlink(temp_path)
                return HttpResponse("Error: Audio file is empty", status=500)
        else:
            print("✗ Audio file not generated!")
            return HttpResponse("Error: Audio file not generated", status=500)
        
    except Exception as e:
        print(f"✗ TTS error: {e}")
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
            except:
                pass
        return HttpResponse(f"Error generating speech: {str(e)}", status=500)


def test_groq_api(request):
    """Test endpoint to check Groq API connection"""
    try:
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'llama-3.3-70b-versatile',
            'messages': [{'role': 'user', 'content': 'Hello'}],
            'max_tokens': 10
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            return JsonResponse({
                'status': 'ok',
                'message': 'Groq API connection successful',
                'response': result['choices'][0]['message']['content']
            })
        elif response.status_code == 401:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid Groq API key. Please get a valid key from https://console.groq.com/'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'Groq API returned {response.status_code}: {response.text}'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@csrf_exempt
@require_POST
def transcribe_audio(request):
    """Transcribe audio using Groq's Whisper API with Amharic support"""
    try:
        if 'audio' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided'}, status=400)
        
        audio_file = request.FILES['audio']
        language = request.POST.get('language', 'en')
        
        # Save temporary audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        try:
            # Use Groq's Whisper API for transcription
            headers = {
                'Authorization': f'Bearer {GROQ_API_KEY}',
            }
            
            # Prepare the files for upload
            with open(temp_path, 'rb') as f:
                files = {
                    'file': ('audio.webm', f, 'audio/webm'),
                    'model': (None, 'whisper-large-v3'),
                }
                
                # Add language hint if specified
                data = {}
                if language == 'am':
                    data['language'] = 'am'
                    data['prompt'] = 'This is Amharic speech. Transcribe in Amharic script (አማርኛ).'
                elif language == 'en':
                    data['language'] = 'en'
                
                response = requests.post(
                    'https://api.groq.com/openai/v1/audio/transcriptions',
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )
            
            if response.status_code == 200:
                result = response.json()
                transcribed_text = result.get('text', '').strip()
                
                print(f"Transcription successful: {transcribed_text}")
                
                return JsonResponse({
                    'text': transcribed_text,
                    'language': language
                })
            else:
                print(f"Whisper API error: {response.status_code} - {response.text}")
                
                # Fallback to OpenAI API if available
                openai_key = getattr(settings, 'OPENAI_API_KEY', None)
                if openai_key:
                    with open(temp_path, 'rb') as f:
                        files = {
                            'file': ('audio.webm', f, 'audio/webm'),
                            'model': (None, 'whisper-1'),
                            'language': (None, 'am' if language == 'am' else 'en')
                        }
                        
                        openai_headers = {
                            'Authorization': f'Bearer {openai_key}',
                        }
                        
                        openai_response = requests.post(
                            'https://api.openai.com/v1/audio/transcriptions',
                            headers=openai_headers,
                            files=files,
                            timeout=30
                        )
                    
                    if openai_response.status_code == 200:
                        result = openai_response.json()
                        transcribed_text = result.get('text', '').strip()
                        
                        return JsonResponse({
                            'text': transcribed_text,
                            'language': language
                        })
                
                return JsonResponse({
                    'error': 'Transcription failed. Please try again.'
                }, status=500)
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            
    except Exception as e:
        print(f"Transcription error: {e}")
        return JsonResponse({'error': str(e)}, status=500)