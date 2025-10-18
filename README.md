# AI Interviewer

An intelligent interview simulation system that provides a realistic interview experience with audio interaction and detailed conversation logging.

## Features

### 1. Dynamic Interview Questions
- Supports various interview categories (e.g., Product Metrics)
- Generates context-aware questions
- Simulates real interview scenarios

### 2. Audio Processing
- Records and processes user answers
- Generates audio for interview questions
- Stores audio files in organized directory structure (`audio/`)
  - Question audio: `audio/question.wav`
  - User response audio: `audio/user_answer.wav`

### 3. Subtitle Generation
- Automatically generates subtitles for both questions and answers
- Stores subtitle files in SRT format (`subtitles/`)
  - Question subtitles: `subtitles/question.srt`
  - Answer subtitles: `subtitles/answer.srt`

### 4. Conversation Logging
- Maintains detailed interview logs (`conversation_logs/`)
- Records timestamp, category, questions, and answers
- Tracks references to audio and subtitle files
- Structured data storage for analysis and review

### 5. Configuration
- Customizable settings via `config.py`
- Flexible interview parameters
- Easy to modify and extend

## Project Structure

```
ai-interviewer/
├── config.py              # Configuration settings
├── interviewer.py         # Main interview logic
├── requirements.txt       # Project dependencies
├── audio/                 # Audio file storage
├── conversation_logs/     # Interview session logs
└── subtitles/            # Generated subtitle files
```

## Getting Started

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the interview settings in `config.py`

3. Run the interviewer:
```bash
python interviewer.py
```

## Dependencies
- See `requirements.txt` for a complete list of dependencies

## Usage
The system will:
1. Present interview questions with audio
2. Record and process user responses
3. Generate subtitles for better accessibility
4. Log the entire conversation for later review

## Note
This project is designed to help users practice and improve their interview skills through AI-powered interactions, with a focus on providing a comprehensive and realistic interview experience.