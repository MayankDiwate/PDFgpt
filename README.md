<h1 align="center" style="font-size: 2em;">PDFgpt</h1>

**Description**:  
PDFGPT is a web application that allows users to upload PDF documents and interact with them using natural language queries. Leveraging a combination of AI and language processing, the app can analyze the content of uploaded PDFs and provide users with detailed responses, summaries, or insights from the document. This application uses a React-based frontend, powered by TypeScript and Vite, and a FastAPI backend that integrates LangChain for natural language processing and PostgreSQL for data storage.

---

### Features

- **PDF Upload & Processing**: Users can upload PDFs for analysis.
- **Natural Language Querying**: Query the document with natural language for insights, summaries, or answers.
- **Interactive Chat Interface**: An easy-to-use interface for seamless interactions.
- **Efficient & Scalable**: Built with FastAPI and PostgreSQL to ensure speed and scalability.

### Tech Stack

- **Client**: React, TypeScript, Vite
- **Server**: FastAPI, LangChain
- **Database**: PostgreSQL

---

### Setup and Installation

1. **Clone the repository**:

   ```bash
   git clone <repository_url>
   cd pdfgpt
   ```

2. **Client Setup**:

   - Navigate to the client folder:
     ```bash
     cd client
     ```
   - Install dependencies:
     ```bash
     npm install
     ```
   - Start the development server:
     ```bash
     npm run dev
     ```

3. **Server Setup**:

   - Navigate to the server folder:
     ```bash
     cd ../server
     ```
   - Create a virtual environment and install dependencies:
     ```bash
     python -m venv env
     source env/bin/activate  # For MacOS/Linux
     env\Scripts\activate  # For Windows
     pip install -r requirements.txt
     ```
   - Start the FastAPI server:
     ```bash
     uvicorn main:app --reload
     ```

4. **Database Setup**:

   - Ensure PostgreSQL is installed and running.
   - Create a new PostgreSQL database and update the connection details in the server configuration.

5. **Run the Application**:
   - The client should now be running at `http://localhost:5173` and the server at `http://localhost:8000`.

---

### Usage

1. Open the frontend application and upload a PDF document.
2. Use the chat interface to ask questions or request summaries of the document.

### Future Enhancements

- Add support for multiple document formats.
- Implement user authentication.
- Add analytics for user queries.

---

### Contributing

Feel free to open issues or submit pull requests with improvements or bug fixes.

---

### License

This project is licensed under the MIT License.
