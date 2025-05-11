# 📝 Text Summarization

An end-to-end system that generates context-aware, concise summaries with dynamic length control across PDF, DOC, TXT and raw-text inputs.  
Leveraging **DistilBART-CNN-6-6** fine-tuned on 1.2 Lakh XSum + CNN/DailyMail samples, this app delivers high-quality abstractive summaries via a Dockerized Flask backend and a responsive Vite + Tailwind frontend.

---

## 🚀 Key Highlights

- 🤖 **Model**: DistilBART-CNN-6-6 fine-tuned on 120 K combined XSum + CNN/DM dataset  
- 🎯 **Dynamic Length Control**: Adjust summary length via `compression_ratio` (0.1–0.8)  
- 📄 **Multi-Format Support**: Raw text, PDF, DOCX, TXT  
- 🐳 **Dockerized Backend**: Flask app with unit-tested, integrated APIs  
- ☁️ **Deployment**: Hosted on Hugging Face Spaces (model) and Cloud Run (API)  
- ✨ **Responsive Frontend**: Built with Vite + TailwindCSS for seamless UX  

---

## 📁 Repository Structure
```

summarization-app/
│
├── backend/
│ ├── model/ # fine-tuned DistilBART weights & config
│ ├── tokenizer/ # tokenizer files
│ ├── app.py # Flask server & API endpoints
│ ├── tests/ # unit + integration tests
│ ├── requirements.txt # Python dependencies
│ └── Dockerfile # container spec
│
├── frontend/
│ ├── public/ # static assets (icons, index.html template)
│ ├── src/
│ │ ├── index.html # Tailwind-styled UI with form & <div id="summaryOutput">
│ │ ├── script.js # handles file/text upload & fetch to /summarize
│ │ └── styles.css # custom Tailwind overrides
│ ├── package.json # frontend dependencies & scripts
│ ├── tailwind.config.js
│ └── postcss.config.js
│
├── .gitignore
└── README.md

```



---

## 🔧 Installation & Local Development

### Prerequisites

- Python 3.8+  
- Node.js 16+ & npm (or yarn)  
- Docker (optional)

### 1. Clone & Navigate

```bash
git clone https://github.com/yourusername/summarization-app.git
cd summarization-app
```

2. Backend
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate     # macOS/Linux
.venv\Scripts\activate      # Windows PowerShell
pip install -r requirements.txt
pytest                        # run unit & integration tests
python app.py                 # starts on http://0.0.0.0:7860
```
3. Frontend
```bash
cd ../frontend
npm install
npm run dev                   # opens at http://localhost:5173
```


🐳 Docker
Build and run the backend in one command:

```bash
cd backend
docker build -t summarizer-backend .
docker run -p 7860:7860 summarizer-backend
Add your own frontend container or serve static files behind a reverse proxy as needed.
```



## 🤝 Contributing

1.Fork the repo

2.Create a branch (git checkout -b feature/my-feature)

3.Commit (git commit -m "Add feature")

4.Push (git push origin feature/my-feature)

5.Open a PR

## 📄 License
Released under the MIT License. See LICENSE for details.

## 🔗 Demo & Contact

- **Live Demo:** [Text Summarization](https://summerizationio.vercel.app/)  
- **Contact:** [baishnab1708@gmail.com](mailto:baishnab1708@gmail.com)  



