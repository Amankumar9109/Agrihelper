import os
import re
import math
from collections import Counter
from flask import current_app

class RAGEngine:
    def __init__(self, knowledge_dir=None):
        self.knowledge_dir = knowledge_dir
        self.chunks = []
        self.vocabulary = set()
        self.doc_freqs = Counter()
        self.chunk_vectors = []
        self.num_chunks = 0
        self._is_indexed = False

    def load_and_index(self, knowledge_dir=None):
        """Loads all documents from knowledge_dir and builds a TF-IDF semantic vector index."""
        if knowledge_dir:
            self.knowledge_dir = knowledge_dir

        if not self.knowledge_dir or not os.path.exists(self.knowledge_dir):
            return

        self.chunks = []
        stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'and', 'or', 'by', 'from', 'this', 'that', 'these', 'those', 'it', 'its',
            'can', 'will', 'should', 'be', 'as', 'do', 'does', 'how', 'what', 'when', 'where',
            'which', 'who', 'why', 'i', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'they'
        }

        # 1. Read files and extract chunks
        for fname in os.listdir(self.knowledge_dir):
            if not fname.endswith('.txt'):
                continue
            fpath = os.path.join(self.knowledge_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Split by markdown sections or dual newlines
                sections = re.split(r'\n(?=## |\n[A-Z0-9#])', content)
                for sec in sections:
                    clean_sec = sec.strip()
                    if len(clean_sec) > 40:
                        lines = clean_sec.split('\n')
                        title = lines[0].strip('# \t\r')
                        self.chunks.append({
                            'text': clean_sec,
                            'title': title,
                            'source': fname
                        })
            except Exception as e:
                print(f"Error reading knowledge file {fname}: {e}")

        self.num_chunks = len(self.chunks)
        if self.num_chunks == 0:
            return

        # 2. Build TF-IDF Term Weights
        self.doc_freqs = Counter()
        tokenized_chunks = []

        for chunk in self.chunks:
            tokens = self._tokenize(chunk['text'], stopwords)
            tokenized_chunks.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freqs[t] += 1

        self.vocabulary = set(self.doc_freqs.keys())

        # 3. Compute vector for each chunk
        self.chunk_vectors = []
        for tokens in tokenized_chunks:
            tf = Counter(tokens)
            vec = {}
            for t, count in tf.items():
                idf = math.log((self.num_chunks + 1) / (self.doc_freqs[t] + 1)) + 1
                vec[t] = count * idf
            # Normalize vector
            norm = math.sqrt(sum(v * v for v in vec.values()))
            if norm > 0:
                vec = {k: v / norm for k, v in vec.items()}
            self.chunk_vectors.append(vec)

        self._is_indexed = True

    def _tokenize(self, text, stopwords=None):
        words = re.findall(r'[a-zA-Z0-9]+', text.lower())
        if stopwords:
            return [w for w in words if w not in stopwords and len(w) > 2]
        return words

    def retrieve(self, query, top_k=3):
        """Retrieves top_k most relevant text chunks using cosine similarity."""
        if not self._is_indexed or not self.chunk_vectors:
            return []

        q_tokens = self._tokenize(query)
        q_tf = Counter(q_tokens)
        q_vec = {}

        for t, count in q_tf.items():
            if t in self.doc_freqs:
                idf = math.log((self.num_chunks + 1) / (self.doc_freqs[t] + 1)) + 1
                q_vec[t] = count * idf

        q_norm = math.sqrt(sum(v * v for v in q_vec.values()))
        if q_norm == 0:
            return self.chunks[:top_k]

        q_vec = {k: v / q_norm for k, v in q_vec.items()}

        # Compute dot product (cosine similarity)
        scores = []
        for i, c_vec in enumerate(self.chunk_vectors):
            dot = sum(q_vec.get(term, 0) * weight for term, weight in c_vec.items())
            scores.append((dot, i))

        scores.sort(key=lambda x: x[0], reverse=True)
        top_indices = [idx for score, idx in scores[:top_k] if score > 0.05]

        # Fallback to top matches if scores were low
        if not top_indices:
            top_indices = [idx for score, idx in scores[:top_k]]

        return [self.chunks[i] for i in top_indices if i < len(self.chunks)]

    def query(self, user_question):
        """Runs the complete RAG query pipeline and returns an expert response with cited sources."""
        if not self._is_indexed:
            self.load_and_index()

        retrieved_chunks = self.retrieve(user_question, top_k=3)
        sources = list(dict.fromkeys([c['source'] for c in retrieved_chunks]))

        context_text = "\n\n---\n\n".join([f"[{c['title']}]\n{c['text']}" for c in retrieved_chunks])

        # Try LLM APIs if configured (Gemini or Groq)
        llm_reply = self._try_llm_generation(user_question, context_text)
        if llm_reply:
            return {
                'reply': llm_reply,
                'sources': sources
            }

        # Fallback to intelligent local RAG synthesis
        fallback_reply = self._synthesize_answer(user_question, retrieved_chunks)
        return {
            'reply': fallback_reply,
            'sources': sources
        }

    def _try_llm_generation(self, user_question, context):
        """Attempts generation via Gemini or Groq if API keys are configured."""
        # 1. Check Gemini
        gemini_key = os.getenv('GEMINI_API_KEY') or (current_app.config.get('GEMINI_API_KEY') if current_app else None)
        if gemini_key:
            try:
                import requests
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
                prompt = (
                    "You are KisanMitra (AgriBot), an expert Indian agricultural advisor. "
                    "Provide a warm, practical, and farmer-friendly answer to the question using ONLY the context provided below. "
                    "Use structured formatting with bullet points and bold headers. Keep it easy to understand.\n\n"
                    f"Context:\n{context}\n\n"
                    f"Farmer's Question: {user_question}"
                )
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                res = requests.post(url, json=payload, timeout=8)
                if res.status_code == 200:
                    data = res.json()
                    candidates = data.get('candidates', [])
                    if candidates:
                        text = candidates[0]['content']['parts'][0]['text']
                        return text
            except Exception as e:
                print(f"Gemini API generation error: {e}")

        # 2. Check Groq
        groq_key = os.getenv('GROQ_API_KEY') or (current_app.config.get('GROQ_API_KEY') if current_app else None)
        if groq_key:
            try:
                import requests
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}
                messages = [
                    {"role": "system", "content": "You are KisanMitra, an expert Indian agriculture assistant. Answer using the provided context clearly and practically."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_question}"}
                ]
                payload = {"model": "llama-3.3-70b-versatile", "messages": messages, "max_tokens": 600}
                res = requests.post(url, json=payload, headers=headers, timeout=8)
                if res.status_code == 200:
                    data = res.json()
                    return data['choices'][0]['message']['content']
            except Exception as e:
                print(f"Groq API generation error: {e}")

        return None

    def _synthesize_answer(self, user_question, retrieved_chunks):
        """Constructs an expert agronomic response directly from retrieved knowledge passages."""
        if not retrieved_chunks:
            return (
                "Namaste! I am **KisanMitra**, your AgriHelper Assistant.\n\n"
                "I couldn't locate specific documentation for that exact query in our local knowledge base. "
                "Here are a few topics I specialize in:\n"
                "• **Government Schemes** (PM-KISAN, PMFBY, Soil Health Card, e-NAM, KCC)\n"
                "• **Precision Farming** (Drip irrigation, Drones, Hydroponics, Vertical farming)\n"
                "• **Crop Seasons & Fertilizers** (Kharif, Rabi, Zaid, NPK dosages, Pest control)\n"
                "• **APMC Mandi Intelligence** (Modal prices, MSP, market timing)\n\n"
                "For immediate personalized guidance, you can also dial the toll-free **Kisan Call Center: 1800-180-1551**."
            )

        top_chunk = retrieved_chunks[0]
        title = top_chunk['title']
        text = top_chunk['text']

        # Format and structure the reply cleanly
        paragraphs = [p.strip() for p in text.split('\n') if p.strip() and not p.startswith('#')]
        summary = "\n".join(paragraphs[:8])

        reply = (
            f"🌾 **KisanMitra Advisory: {title}**\n\n"
            f"{summary}\n\n"
            f"💡 **Practical Recommendation:**\n"
            f"• Always verify soil conditions and weather forecasts before applying major fertilizer or irrigation doses.\n"
            f"• For round-the-clock free voice support in 22 languages, contact the **Kisan Helpline at 1800-180-1551**."
        )

        return reply
