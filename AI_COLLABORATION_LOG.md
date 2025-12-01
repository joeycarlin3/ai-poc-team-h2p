# AI Collaboration log - AI Interview Practice Tool
This document logs the primary AI tools used in the development and runtime of the AI Interview Practice Tool, including the core prompts used by the application to generate feedback.

---

## Section 1: Tool Manifest
Gemini in AI Studio
- Why Used: Used for iterative prompt engineering. The studio environment allowed rapid testing of different model configurations and structured output schemas to ensure consistent, high-quality feedback.
- Types of Tasks: Prompt refinement, testing JSON output schemas for structured data extraction, and validating model behavior for scoring.

GitHub Copilot
- Why Used: Integrated directly into the IDE for real-time coding assistance and boilerplate generation.
- Types of Tasks: Generating utility functions (e.g., audio file handling, UI component boilerplate), writing and correcting Markdown documentation, and assisting with complex frontend state management logic.

Gemini API 
- Why Used: This is the primary model used at runtime to power the application. Chosen for its speed, low latency, and robust instruction following required for generating complex, multi-part structured analysis.
- Types of Tasks: Running the core application logic: generating the detailed interview analysis, the score, and the suggested answer simultaneously.

---

## Section 2: Application Prompts (Runtime)
These are the most critical prompts that the application sends to the Gemini model after a user uploads an audio transcription.

### Critical Prompt 1: Full Interview Analysis and Scoring
This prompt is designed to take the transcribed answer and return a comprehensive, structured analysis, including the required score, in a single API call.

Full Prompt Text (System Instruction/Query Combined):
- System Instruction: You are a world-class HR Expert and Interview Coach. Your task is to critically analyze a candidate's answer based on a specific interview question and provide structured feedback and a quantitative score.
- User Query: The interview question was: "{Interview Question}". The candidate's transcribed response is: "{Transcribed Audio Text}".

    - Your analysis must strictly adhere to the following structure:
    - Executive Summary: (1-2 sentences summarizing the overall quality and impression.)
    - Clarity & Structure (Focus): (Detailed feedback on the flow, organization, and focus of the answer.)
    - Content & Relevance: (Detailed feedback on the depth, specificity, and relevance of the examples used.)
    - Tone & Confidence: (Detailed feedback on the language, professionalism, and perceived confidence.)
    - Score out of 10: (Provide a numerical score only, e.g., '7/10', based on industry standards.)

Rationale for Design: This prompt uses a "System Instruction" to define a professional persona ("HR Expert and Interview Coach") to ensure the feedback is authoritative and constructive. It uses numbered list formatting in the prompt to force the model to adhere to a specific, predictable output structure (Executive Summary, Clarity, Content, Tone) that is then easy for the application's frontend to parse and display consistently for the user. Requesting the score as a separate, clearly defined item ensures it is always present and easy to extract.

### Critical Prompt 2: Generating a Suggested Better Answer
This prompt is sent immediately after the analysis to provide a concrete example of improvement, which is a key value proposition of the tool.

Full Prompt Text:
- System Instruction: Act as a professional writing and interviewing expert. Your goal is to rewrite and polish the provided candidate response into an ideal, high-scoring answer that directly addresses the original question with professional language and structure.
- User Query: The original interview question was: "{Interview Question}". The candidate's response was: "{Transcribed Audio Text}". Generate a "Suggested Better Answer" that incorporates strong structure, relevant professional detail, and confident language. Present only the final, polished answer text.

Rationale for Design: This prompt is separate from the analysis prompt to prevent the model's critique (Prompt 1) from biasing its creative generation (Prompt 2). It uses an explicit instruction to "Present only the final, polished answer text" to ensure no introductory or concluding commentary is included, making the output directly usable by the front end.

---

### Section 3: Process Prompts (Development Support)
These prompts were used by the development team to accelerate the coding and planning phases of the project.

- Process Prompt 1: Implementing the Audio Pipeline Prompt: "Write the complete code for an HTML/Tailwind page that handles file drag-and-drop, displays the file name, and uses the ffmpeg library (loaded from CDN) to prepare the audio file for upload. Include necessary event listeners and UI elements."
- Process Prompt 2: User Story Generation for MVP
Prompt: "Generate five critical user stories for the Minimum Viable Product (MVP) of an AI Interview Practice Tool. Focus on the core user journey: 
    1. User selects a question. 
    2. User uploads an answer. 
    3. User receives feedback."
