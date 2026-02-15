# Implementation Plan: AI Interviewer

## Overview

This implementation plan breaks down the AI Interviewer system into incremental coding tasks. The approach follows a bottom-up strategy: building core data models and utilities first, then implementing individual components, and finally wiring everything together through the LangGraph orchestrator. Each task builds on previous work to ensure no orphaned code.

## Tasks

- [ ] 1. Set up project structure and dependencies
  - Create Python project with poetry or pip requirements
  - Install core dependencies: langchain, langgraph, fastapi, pydantic, hypothesis (for property testing)
  - Install additional dependencies: openai/anthropic SDK, python-multipart (file uploads), pytest
  - Set up project structure: src/models, src/components, src/api, tests/
  - Configure pytest and hypothesis for testing
  - _Requirements: 11.1, 11.2, 11.3_

- [ ] 2. Implement core data models
  - [ ] 2.1 Create Pydantic models for Profile, ResumeData, Question, Response, Evaluation, SessionSummary
    - Define all data classes using Pydantic BaseModel for validation
    - Include field validators for years_experience (0-50), difficulty (1-10)
    - Add QuestionType enum (THEORY, CODING, BEHAVIORAL)
    - _Requirements: 1.1, 2.3_
  
  - [ ]* 2.2 Write property test for profile validation
    - **Property 1: Profile Validation Completeness**
    - **Validates: Requirements 1.2, 1.5**
  
  - [ ]* 2.3 Write unit tests for data model edge cases
    - Test invalid years_experience values
    - Test difficulty bounds
    - Test required field validation
    - _Requirements: 1.2_

- [ ] 3. Implement Profile Manager component
  - [ ] 3.1 Create ProfileManager class with validation logic
    - Implement collect_profile() method with Pydantic validation
    - Implement validate_profile() returning ValidationResult
    - Handle missing fields and return descriptive errors
    - _Requirements: 1.1, 1.2, 1.5_
  
  - [ ] 3.2 Implement resume parsing with LangChain
    - Use LangChain document loaders for PDF/DOCX parsing
    - Create LLM chain with structured output parser for skill extraction
    - Implement parse_resume() method returning ResumeData
    - Handle parsing errors gracefully with fallback
    - _Requirements: 1.3_
  
  - [ ]* 3.3 Write property test for resume parsing
    - **Property 2: Resume Parsing Produces Structured Data**
    - **Validates: Requirements 1.3**
  
  - [ ]* 3.4 Write unit tests for profile manager
    - Test validation with missing fields
    - Test resume parsing with sample PDF/DOCX files
    - Test error handling for unsupported formats
    - _Requirements: 1.2, 1.3, 1.5_

- [ ] 4. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement Question Generator component
  - [ ] 5.1 Create QuestionGenerator class with LangChain chains
    - Set up LLM client (OpenAI or Anthropic)
    - Create prompt templates for question generation
    - Implement generate_question() with structured output parsing
    - Include profile context (job role, experience, skills) in prompts
    - _Requirements: 2.1, 2.5_
  
  - [ ] 5.2 Implement question type selection logic
    - Implement select_question_type() to balance theory/coding/behavioral
    - Track question history to ensure diversity
    - _Requirements: 2.3_
  
  - [ ] 5.3 Implement difficulty adjustment logic
    - Implement adjust_difficulty() based on performance history
    - Map experience levels to difficulty ranges (junior: 1-5, mid: 3-8, senior: 6-10)
    - Ensure difficulty stays within bounds
    - _Requirements: 2.5, 10.1, 10.2, 10.4_
  
  - [ ]* 5.4 Write property test for question generation
    - **Property 4: Question Generation Reflects Profile**
    - **Validates: Requirements 2.1, 2.5**
  
  - [ ]* 5.5 Write property test for question type diversity
    - **Property 5: Question Type Diversity**
    - **Validates: Requirements 2.3**
  
  - [ ]* 5.6 Write property test for difficulty bounds
    - **Property 20: Difficulty Bounds Enforcement**
    - **Validates: Requirements 10.4**
  
  - [ ]* 5.7 Write property test for difficulty adaptation
    - **Property 19: Difficulty Adaptation to Performance**
    - **Validates: Requirements 10.1, 10.2**
  
  - [ ]* 5.8 Write unit tests for question generator
    - Test question generation with various profiles
    - Test difficulty adjustment with mock performance history
    - Test question type selection
    - _Requirements: 2.1, 2.3, 2.5_

- [ ] 6. Implement code execution sandbox
  - [ ] 6.1 Create CodeExecutor class for multi-language support
    - Implement execute_code() for Python, JavaScript, Java, C++, Go
    - Use subprocess with timeout (5 seconds) and memory limits
    - Return ExecutionResult with stdout, stderr, exit code
    - Handle syntax errors and runtime errors
    - _Requirements: 4.4, 4.6, 9.3_
  
  - [ ]* 6.2 Write property test for multi-language execution
    - **Property 18: Multi-Language Code Execution**
    - **Validates: Requirements 9.2, 9.3**
  
  - [ ]* 6.3 Write property test for code execution errors
    - **Property 9: Code Execution Errors Are Reported**
    - **Validates: Requirements 4.6**
  
  - [ ]* 6.4 Write unit tests for code executor
    - Test successful execution in each language
    - Test timeout handling
    - Test syntax error reporting
    - Test runtime error handling
    - _Requirements: 4.4, 4.6, 9.3_

- [ ] 7. Implement Response Evaluator component
  - [ ] 7.1 Create ResponseEvaluator class for theory questions
    - Implement evaluate_theory() using LLM with rubric-based prompting
    - Use structured output parser for Evaluation model
    - Include correctness, completeness, clarity, technical depth scores
    - Generate strengths, improvements, and suggestions lists
    - _Requirements: 3.3, 3.4, 7.2_
  
  - [ ] 7.2 Implement code evaluation logic
    - Implement evaluate_code() combining test execution + LLM review
    - Execute code against test cases using CodeExecutor
    - Use LLM to assess time/space complexity and code quality
    - Return CodeEvaluation with all required fields
    - _Requirements: 4.4, 4.5, 7.3_
  
  - [ ] 7.3 Implement feedback generation
    - Implement generate_feedback() to format evaluation results
    - Ensure feedback is constructive and actionable
    - _Requirements: 3.4, 7.2_
  
  - [ ]* 7.4 Write property test for theory evaluation
    - **Property 6: Theory Evaluation Produces Structured Feedback**
    - **Validates: Requirements 3.3, 3.4, 7.2**
  
  - [ ]* 7.5 Write property test for code evaluation
    - **Property 8: Code Evaluation Includes Complexity Analysis**
    - **Validates: Requirements 4.5, 7.3**
  
  - [ ]* 7.6 Write unit tests for response evaluator
    - Test theory evaluation with sample responses
    - Test code evaluation with correct and incorrect code
    - Test feedback generation
    - _Requirements: 3.3, 3.4, 4.4, 4.5_

- [ ] 8. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement Audio Interface component
  - [ ] 9.1 Create AudioInterface class with TTS and STT
    - Implement text_to_speech() using OpenAI TTS or ElevenLabs
    - Implement speech_to_text() using OpenAI Whisper
    - Return transcription with confidence score
    - _Requirements: 5.1, 5.2_
  
  - [ ] 9.2 Implement transcription validation and fallback
    - Implement validate_transcription() checking confidence threshold (0.85)
    - Generate prompt for low-confidence transcriptions
    - _Requirements: 5.5_
  
  - [ ]* 9.3 Write property test for TTS
    - **Property 10: Text-to-Speech Conversion**
    - **Validates: Requirements 5.1**
  
  - [ ]* 9.4 Write property test for STT
    - **Property 11: Speech-to-Text Transcription**
    - **Validates: Requirements 5.2**
  
  - [ ]* 9.5 Write property test for low confidence handling
    - **Property 12: Low Confidence Transcription Handling**
    - **Validates: Requirements 5.5**
  
  - [ ]* 9.6 Write unit tests for audio interface
    - Test TTS with sample text
    - Test STT with sample audio files
    - Test confidence threshold handling
    - _Requirements: 5.1, 5.2, 5.5_

- [ ] 10. Implement Session Manager for persistence
  - [ ] 10.1 Create SessionManager class with database operations
    - Set up database connection (SQLite for development, PostgreSQL for production)
    - Implement save_session() serializing InterviewState to JSON
    - Implement load_session() deserializing from database
    - Implement save_history() for completed sessions
    - Implement get_history() retrieving past sessions by candidate ID
    - _Requirements: 1.4, 6.1, 8.5_
  
  - [ ]* 10.2 Write property test for session state persistence
    - **Property 3: Session State Persistence**
    - **Validates: Requirements 1.4, 6.4, 10.3**
  
  - [ ]* 10.3 Write property test for session ID uniqueness
    - **Property 13: Session ID Uniqueness**
    - **Validates: Requirements 6.1**
  
  - [ ]* 10.4 Write property test for session history persistence
    - **Property 17: Session History Persistence**
    - **Validates: Requirements 8.5**
  
  - [ ]* 10.5 Write unit tests for session manager
    - Test session save and load
    - Test session ID generation
    - Test history storage and retrieval
    - _Requirements: 1.4, 6.1, 8.5_

- [ ] 11. Implement LangGraph Interview Orchestrator
  - [ ] 11.1 Define InterviewState TypedDict
    - Create InterviewState with all required fields
    - Include profile, current_question, response_history, difficulty_level, question_count, session_status, performance_metrics
    - _Requirements: 6.1, 6.4, 10.3_
  
  - [ ] 11.2 Create LangGraph StateGraph with nodes
    - Define nodes: profile_collection, question_generation, response_evaluation, feedback_delivery, summary_generation
    - Implement each node as a function that updates InterviewState
    - _Requirements: 11.3_
  
  - [ ] 11.3 Define state transitions and edges
    - Add conditional edges based on user actions (continue, pause, end)
    - Add conditional edges based on performance (difficulty adjustment)
    - Wire nodes together following the state machine diagram
    - _Requirements: 11.3_
  
  - [ ] 11.4 Implement session management methods
    - Implement create_session() initializing new InterviewState
    - Implement process_event() handling user actions
    - Implement pause_session() saving state via SessionManager
    - Implement resume_session() loading state via SessionManager
    - _Requirements: 6.1, 6.2, 6.5_
  
  - [ ] 11.5 Integrate all components into orchestrator
    - Wire ProfileManager into profile_collection node
    - Wire QuestionGenerator into question_generation node
    - Wire ResponseEvaluator into response_evaluation node
    - Wire AudioInterface for audio mode support
    - _Requirements: 11.3_
  
  - [ ]* 11.6 Write property test for pause-resume
    - **Property 14: Pause-Resume State Preservation**
    - **Validates: Requirements 6.2, 6.5**
  
  - [ ]* 11.7 Write property test for session termination
    - **Property 15: Session Termination Produces Summary**
    - **Validates: Requirements 6.3, 8.1**
  
  - [ ]* 11.8 Write property test for difficulty adjustment explanation
    - **Property 21: Difficulty Adjustment Explanation**
    - **Validates: Requirements 10.5**
  
  - [ ]* 11.9 Write unit tests for orchestrator
    - Test session creation
    - Test state transitions
    - Test pause and resume
    - Test session termination
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [ ] 12. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 13. Implement summary generation and analytics
  - [ ] 13.1 Create SummaryGenerator component
    - Implement generate_summary() analyzing response_history
    - Calculate metrics: questions answered, correctness rate, average response time
    - Identify strengths and knowledge gaps using LLM analysis
    - Generate recommended topics for study
    - Include performance comparison data
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  
  - [ ]* 13.2 Write property test for summary content
    - **Property 16: Summary Contains Required Metrics**
    - **Validates: Requirements 8.2, 8.3, 8.4**
  
  - [ ]* 13.3 Write unit tests for summary generator
    - Test summary generation with various session histories
    - Test metric calculations
    - Test recommendation generation
    - _Requirements: 8.1, 8.2, 8.3, 8.4_

- [ ] 14. Implement FastAPI backend server
  - [ ] 14.1 Create API endpoints for interview flow
    - POST /sessions - Create new interview session
    - POST /sessions/{id}/profile - Submit profile
    - GET /sessions/{id}/question - Get next question
    - POST /sessions/{id}/response - Submit response
    - POST /sessions/{id}/pause - Pause session
    - POST /sessions/{id}/resume - Resume session
    - POST /sessions/{id}/end - End session and get summary
    - GET /sessions/{id}/history - Get candidate history
    - _Requirements: 6.1, 6.2, 6.3, 6.5, 8.5_
  
  - [ ] 14.2 Implement file upload for resume
    - Add multipart/form-data support for resume upload
    - Validate file types (PDF, DOCX)
    - Pass file to ProfileManager for parsing
    - _Requirements: 1.1, 1.3_
  
  - [ ] 14.3 Implement audio endpoints
    - POST /sessions/{id}/audio/question - Get question as audio
    - POST /sessions/{id}/audio/response - Submit audio response
    - Return transcription with confidence score
    - _Requirements: 5.1, 5.2_
  
  - [ ] 14.4 Add error handling middleware
    - Handle ValidationError, FileFormatError, ParsingError
    - Handle TimeoutError, MemoryError, SyntaxError
    - Handle LLM API errors with retry logic
    - Return appropriate HTTP status codes and error messages
    - _Requirements: 1.5, 4.6_
  
  - [ ]* 14.5 Write integration tests for API endpoints
    - Test complete interview flow via API
    - Test pause and resume via API
    - Test audio mode via API
    - Test error handling
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

- [ ] 15. Implement frontend web interface
  - [ ] 15.1 Create React/Vue app with routing
    - Set up frontend project with Vite or Create React App
    - Create routes: /start, /interview, /summary
    - Implement basic layout and navigation
    - _Requirements: 1.1_
  
  - [ ] 15.2 Create profile input form
    - Build form for job role, years of experience, target company
    - Add file upload for resume
    - Display validation errors from backend
    - _Requirements: 1.1, 1.2, 1.5_
  
  - [ ] 15.3 Integrate Monaco Editor for coding questions
    - Install @monaco-editor/react
    - Configure editor with language selection dropdown
    - Support syntax highlighting for Python, JavaScript, Java, C++, Go
    - Add code submission button
    - _Requirements: 4.1, 4.2, 4.3, 9.1, 9.2_
  
  - [ ] 15.4 Create text input interface for theory questions
    - Build text area for theory responses
    - Add character count and formatting options
    - Display question and allow editing before submission
    - _Requirements: 3.1, 3.2_
  
  - [ ] 15.5 Implement audio interface controls
    - Add toggle for audio mode
    - Add microphone recording button
    - Display real-time transcription
    - Add audio playback for questions
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ] 15.6 Create feedback display component
    - Display evaluation scores (correctness, completeness, clarity, technical depth)
    - Show strengths, improvements, and suggestions
    - For code: show test results, complexity analysis, code quality
    - _Requirements: 3.4, 4.5, 7.2, 7.3_
  
  - [ ] 15.7 Implement session controls
    - Add pause button with state preservation
    - Add resume functionality
    - Add end interview button
    - Display question counter and timer
    - _Requirements: 6.2, 6.3, 6.4, 6.5_
  
  - [ ] 15.8 Create summary and analytics view
    - Display performance summary with all metrics
    - Show strengths and knowledge gaps
    - Display recommended topics
    - Show performance comparison chart
    - Add link to view past interview history
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 16. Final integration and end-to-end testing
  - [ ] 16.1 Wire frontend to backend API
    - Connect all frontend components to API endpoints
    - Implement error handling and loading states
    - Add retry logic for transient failures
    - _Requirements: All_
  
  - [ ]* 16.2 Run all property tests
    - Execute full property test suite with 100 iterations each
    - Verify all 21 correctness properties pass
    - _Requirements: All testable requirements_
  
  - [ ]* 16.3 Run end-to-end integration tests
    - Test complete interview flow: profile → questions → responses → summary
    - Test pause and resume mid-interview
    - Test multi-modal interaction: text → audio → code
    - Test difficulty adaptation across multiple questions
    - Test error scenarios and recovery
    - _Requirements: All_

- [ ] 17. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties (21 total)
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end flows
- The implementation follows a bottom-up approach: data models → components → orchestrator → API → frontend
