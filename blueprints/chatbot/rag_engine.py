"""
AgriHelper RAG Knowledge Engine (KisanMitra AI)
Features:
- Document chunking and semantic vector indexing with NumPy acceleration
- Agricultural bilingual (English + Hinglish) synonym normalization
- Term-frequency inverse document frequency (TF-IDF) + heading-boost retrieval
- Multi-provider LLM generation (Google Gemini + Groq) with robust local agronomy synthesis fallback
- Direct deep-link citations mapping sources to platform tools (/policy, /techniques, /market, /weather)
"""

import os
import re
import math
import requests
from collections import Counter
import numpy as np
from flask import current_app

# Canonical Source Metadata Mapping
SOURCE_METADATA = {
    'government_schemes.txt': {
        'name': 'Government Schemes & DBT Subsidies',
        'url': '/policy',
        'icon': 'fa-landmark',
        'badge': 'Official Schemes'
    },
    'farming_techniques.txt': {
        'name': 'Modern Farming Techniques & Precision Ag',
        'url': '/techniques',
        'icon': 'fa-tractor',
        'badge': 'Field Guide'
    },
    'market_guide.txt': {
        'name': 'APMC Mandi Price Intelligence & e-NAM',
        'url': '/market',
        'icon': 'fa-chart-line',
        'badge': 'Market Data'
    },
    'crop_calendar.txt': {
        'name': 'Indian Crop Calendar & Seasonal Ag Advisory',
        'url': '/weather',
        'icon': 'fa-cloud-sun',
        'badge': 'Agronomy'
    },
    'faq.txt': {
        'name': 'Farmer FAQ & Kisan Call Center Guide',
        'url': '/policy',
        'icon': 'fa-circle-question',
        'badge': 'Helpline'
    }
}

# Agricultural Bilingual Synonyms & Concept Expansions
AGRI_SYNONYMS = {
    'pani': 'water irrigation drip sprinkle',
    'paani': 'water irrigation drip sprinkle',
    'sinchai': 'irrigation drip flood micro',
    'khaad': 'fertilizer npk urea dap manure compost',
    'khad': 'fertilizer npk urea dap manure compost',
    'keeda': 'pest insect disease leaf curl borer',
    'keede': 'pest insect disease leaf curl borer',
    'kitnashak': 'pesticide insecticide neem spray biological',
    'bima': 'pmfby crop insurance claim compensation loss',
    'beema': 'pmfby crop insurance claim compensation loss',
    'subsidy': 'subsidy financial assistance grant scheme dbt',
    'anudan': 'subsidy financial assistance grant scheme dbt',
    'gehu': 'wheat rabi sowing cri tillering',
    'gehun': 'wheat rabi sowing cri tillering',
    'dhan': 'paddy rice kharif nursery standing water',
    'chawal': 'paddy rice kharif nursery',
    'mandi': 'apmc market modal price enam arrival rate',
    'bhav': 'price modal rate msp mandi trading',
    'daam': 'price modal rate msp mandi',
    'mitti': 'soil health card npk ph organic carbon',
    'matti': 'soil health card npk ph organic carbon',
    'kisan': 'farmer agriculture krishi cultivator',
    'khet': 'farm field acre land soil crop',
    'fasal': 'crop harvest sowing yield season',
    'drone': 'uav kisan drone smam aerial spray mapping ndvi',
    'hydroponic': 'hydroponics soilless water nutrient nft dwc'
}

class RAGEngine:
    def __init__(self, knowledge_dir=None):
        self.knowledge_dir = knowledge_dir
        self.chunks = []
        self.vocabulary = []
        self.vocab_map = {}
        self.doc_freqs = Counter()
        self.chunk_vectors = []
        self.vector_matrix = None
        self.num_chunks = 0
        self._is_indexed = False

    def load_and_index(self, knowledge_dir=None):
        """Loads all documents from knowledge_dir and builds a NumPy-accelerated TF-IDF vector index."""
        if knowledge_dir:
            self.knowledge_dir = knowledge_dir

        if not self.knowledge_dir or not os.path.exists(self.knowledge_dir):
            return

        self.chunks = []
        stopwords = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 'to', 'for', 'of',
            'with', 'and', 'or', 'by', 'from', 'this', 'that', 'these', 'those', 'it', 'its',
            'can', 'will', 'should', 'be', 'as', 'do', 'does', 'how', 'what', 'when', 'where',
            'which', 'who', 'why', 'i', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'they',
            'me', 'him', 'her', 'us', 'them', 'if', 'then', 'else', 'so', 'up', 'out'
        }

        # 1. Read files and extract chunks
        for fname in sorted(os.listdir(self.knowledge_dir)):
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
                    if len(clean_sec) > 35:
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

        # 2. Build Vocabulary & Document Frequencies
        self.doc_freqs = Counter()
        tokenized_chunks = []

        for chunk in self.chunks:
            tokens = self._tokenize(chunk['text'], stopwords)
            tokenized_chunks.append(tokens)
            unique_tokens = set(tokens)
            for t in unique_tokens:
                self.doc_freqs[t] += 1

        self.vocabulary = sorted(list(self.doc_freqs.keys()))
        self.vocab_map = {term: idx for idx, term in enumerate(self.vocabulary)}
        vocab_size = len(self.vocabulary)

        # 3. Build Dense NumPy Vector Matrix (Normalized TF-IDF)
        matrix = np.zeros((self.num_chunks, vocab_size), dtype=np.float32)

        self.chunk_vectors = []
        for i, tokens in enumerate(tokenized_chunks):
            tf = Counter(tokens)
            vec_dict = {}
            for t, count in tf.items():
                if t in self.vocab_map:
                    col_idx = self.vocab_map[t]
                    idf = math.log((self.num_chunks + 1.0) / (self.doc_freqs[t] + 1.0)) + 1.0
                    weight = count * idf
                    matrix[i, col_idx] = weight
                    vec_dict[t] = weight

            # Normalize row vector
            row_norm = np.linalg.norm(matrix[i])
            if row_norm > 0:
                matrix[i] /= row_norm
                vec_dict = {k: v / row_norm for k, v in vec_dict.items()}

            self.chunk_vectors.append(vec_dict)

        self.vector_matrix = matrix
        self._is_indexed = True

    def _tokenize(self, text, stopwords=None):
        """Tokenizes text, strips punctuation, and optionally filters stopwords."""
        words = re.findall(r'[a-zA-Z0-9]+', text.lower())
        if stopwords:
            return [w for w in words if w not in stopwords and len(w) > 1]
        return words

    def _expand_query(self, query):
        """Augments user question with domain-specific agricultural synonyms and Hinglish mappings."""
        words = query.lower().split()
        expanded_parts = [query]
        for w in words:
            clean_w = re.sub(r'[^a-zA-Z0-9]', '', w)
            if clean_w in AGRI_SYNONYMS:
                expanded_parts.append(AGRI_SYNONYMS[clean_w])
        return " ".join(expanded_parts)

    def retrieve(self, query, top_k=3):
        """
        Retrieves top_k most relevant text chunks using cosine similarity
        with NumPy vector dot-product acceleration and entity boosting.
        """
        if not self._is_indexed or self.vector_matrix is None or len(self.vocabulary) == 0:
            return []

        expanded_query = self._expand_query(query)
        q_tokens = self._tokenize(expanded_query)
        q_tf = Counter(q_tokens)

        vocab_size = len(self.vocabulary)
        q_vec = np.zeros(vocab_size, dtype=np.float32)

        for t, count in q_tf.items():
            if t in self.vocab_map:
                col_idx = self.vocab_map[t]
                idf = math.log((self.num_chunks + 1.0) / (self.doc_freqs[t] + 1.0)) + 1.0
                q_vec[col_idx] = count * idf

        q_norm = np.linalg.norm(q_vec)
        if q_norm > 0:
            q_vec /= q_norm
            scores = np.dot(self.vector_matrix, q_vec)
        else:
            scores = np.zeros(self.num_chunks, dtype=np.float32)

        # Entity Keyword Boosting
        q_lower = query.lower()
        for idx, chunk in enumerate(self.chunks):
            title_lower = chunk['title'].lower()
            text_lower = chunk['text'].lower()
            source = chunk['source']

            # Exact acronym matching
            if 'pm-kisan' in q_lower or 'pmkisan' in q_lower:
                if 'pm-kisan' in title_lower or 'kisan samman' in title_lower:
                    scores[idx] += 0.45
            if 'pmfby' in q_lower or 'fasal bima' in q_lower or 'crop insurance' in q_lower:
                if 'pmfby' in title_lower or 'fasal bima' in title_lower:
                    scores[idx] += 0.45
            if 'soil health' in q_lower or 'shc' in q_lower or 'soil test' in q_lower:
                if 'soil health' in title_lower or 'shc' in title_lower:
                    scores[idx] += 0.45
            if 'drip' in q_lower or 'micro-irrigation' in q_lower or 'drip irrigation' in q_lower:
                if 'drip' in title_lower or 'micro-irrigation' in title_lower:
                    scores[idx] += 0.45
            if 'drone' in q_lower or 'uav' in q_lower:
                if 'drone' in title_lower or 'unmanned aerial' in title_lower:
                    scores[idx] += 0.45
            if 'hydroponic' in q_lower or 'soilless' in q_lower:
                if 'hydroponic' in title_lower or 'soilless' in title_lower:
                    scores[idx] += 0.45
            if 'wheat' in q_lower and 'sowing' in q_lower:
                if 'wheat' in title_lower or 'rabi' in title_lower:
                    scores[idx] += 0.35
            if 'kisan call center' in q_lower or 'helpline' in q_lower or 'toll free' in q_lower:
                if 'helpline' in text_lower or 'kisan call center' in text_lower:
                    scores[idx] += 0.50

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append(self.chunks[idx])

        return results

    def query(self, user_question):
        """
        Runs the complete RAG query pipeline and returns an agronomic response
        with cited source files and clickable platform links.
        """
        if not self._is_indexed:
            self.load_and_index()

        retrieved_chunks = self.retrieve(user_question, top_k=3)
        sources = list(dict.fromkeys([c['source'] for c in retrieved_chunks]))

        # Format rich citation links
        source_links = []
        for s in sources:
            meta = SOURCE_METADATA.get(s, {
                'name': s.replace('.txt', '').replace('_', ' ').title(),
                'url': '/policy',
                'icon': 'fa-file-lines',
                'badge': 'Knowledge Base'
            })
            source_links.append({
                'file': s,
                'name': meta['name'],
                'url': meta['url'],
                'icon': meta['icon'],
                'badge': meta['badge']
            })

        context_text = "\n\n---\n\n".join([f"[{c['title']}]\n{c['text']}" for c in retrieved_chunks])

        # Attempt LLM APIs if configured (Gemini or Groq)
        llm_reply = self._try_llm_generation(user_question, context_text)
        if llm_reply:
            return {
                'reply': llm_reply,
                'sources': sources,
                'source_links': source_links
            }

        # High-precision local agronomy synthesis fallback
        fallback_reply = self._synthesize_answer(user_question, retrieved_chunks)
        return {
            'reply': fallback_reply,
            'sources': sources,
            'source_links': source_links
        }

    def _try_llm_generation(self, user_question, context):
        """Attempts real-time generation via Groq or Gemini if API keys are configured."""
        prompt = (
            "You are KisanMitra (AgriBot), India's premier digital agricultural advisor.\n"
            "Answer the farmer's question in a warm, respectful, and practical tone using the knowledge context provided below.\n\n"
            "Formatting & Tone Guidelines:\n"
            "• Use structured markdown with bold headings and bullet points.\n"
            "• Clearly highlight critical numbers, fertilizer dosages (NPK), seed varieties, subsidies, and deadlines.\n"
            "• Mention the toll-free Kisan Call Center helpline (1800-180-1551) where applicable.\n"
            "• If the context does not fully answer the question, supplement with accurate agronomic knowledge suitable for Indian conditions.\n\n"
            f"Knowledge Base Context:\n{context}\n\n"
            f"Farmer's Question: {user_question}"
        )

        # 1. Groq Cloud LLM (High-speed LPU inference)
        groq_key = os.getenv('GROQ_API_KEY') or (current_app.config.get('GROQ_API_KEY') if current_app else None)
        if groq_key:
            groq_models = ["qwen/qwen3.8-27b", "openai/gpt-oss-120b", "openai/gpt-oss-20b", "llama-3.3-70b-versatile"]
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {groq_key.strip()}", "Content-Type": "application/json"}

            for g_model in groq_models:
                try:
                    payload = {
                        "model": g_model,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are KisanMitra, an expert Indian agricultural advisor. Answer farmers clearly, accurately, and practically."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 800,
                        "temperature": 0.3
                    }
                    res = requests.post(url, json=payload, headers=headers, timeout=10)
                    if res.status_code == 200:
                        data = res.json()
                        reply = data['choices'][0]['message']['content']
                        if reply and len(reply.strip()) > 20:
                            return reply.strip()
                except Exception as e:
                    if current_app:
                        current_app.logger.warning(f"Groq API ({g_model}) error: {e}")

        # 2. Google Gemini
        gemini_key = os.getenv('GEMINI_API_KEY') or (current_app.config.get('GEMINI_API_KEY') if current_app else None)
        if gemini_key:
            gemini_models = ["gemini-flash-latest", "gemini-2.5-flash", "gemini-3.8-flash"]
            for m_name in gemini_models:
                try:
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={gemini_key.strip()}"
                    payload = {"contents": [{"parts": [{"text": prompt}]}]}
                    res = requests.post(url, json=payload, timeout=10)
                    if res.status_code == 200:
                        data = res.json()
                        candidates = data.get('candidates', [])
                        if candidates:
                            reply = candidates[0]['content']['parts'][0]['text']
                            if reply and len(reply.strip()) > 20:
                                return reply.strip()
                except Exception as e:
                    if current_app:
                        current_app.logger.warning(f"Gemini API ({m_name}) error: {e}")

        return None

    def _synthesize_answer(self, user_question, retrieved_chunks):
        """Constructs an expert agronomic response directly from retrieved knowledge passages."""
        if not retrieved_chunks:
            return (
                "Namaste! I am **KisanMitra**, your AgriHelper Assistant.\n\n"
                "I couldn't locate specific documentation for that exact query in our local knowledge base. "
                "Here are a few topics I specialize in:\n"
                "• **Government Schemes & Subsidies** (PM-KISAN, PMFBY, Soil Health Card, e-NAM, KCC)\n"
                "• **Precision Modern Farming** (Drip irrigation, Drones, Hydroponics, Vertical farming)\n"
                "• **Crop Seasons & Fertilizers** (Kharif, Rabi, Zaid, NPK dosages, Pest control)\n"
                "• **APMC Mandi Intelligence** (Modal prices, MSP, market timing)\n\n"
                "For immediate round-the-clock voice guidance in 22 languages, dial the toll-free **Kisan Call Center: 1800-180-1551**."
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
