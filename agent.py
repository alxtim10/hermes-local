import json
from openai import OpenAI
import yfinance as yf
from ddgs import DDGS

# Hubungkan ke endpoint lokal Ollama
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Nilai bebas, dibutuhkan oleh OpenAI client
)

# ==========================
# 1. Definisi Fungsi / Tools
# ==========================
def get_stock_data(ticker: str) -> str:
    """Mengambil data harga penutupan terakhir dan riwayat singkat saham."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if hist.empty:
            return f"Tidak ada data untuk ticker {ticker}."
        last_price = hist["Close"].iloc[-1]
        summary = {
            "ticker": ticker,
            "latest_close": round(float(last_price), 2),
            "5_day_history": [round(float(p), 2) for p in hist["Close"].tolist()]
        }
        return json.dumps(summary)
    except Exception as e:
        return f"Error mengambil data saham: {str(e)}"

def search_market_news(query: str) -> str:
    """Mencari ringkasan berita terkini di web."""
    try:
        ddgs = DDGS()
        results = ddgs.text(query, max_results=3)
        formatted = [{"title": r["title"], "snippet": r["body"]} for r in results]
        return json.dumps(formatted)
    except Exception as e:
        return f"Error mencari berita: {str(e)}"

# Pemetaan nama fungsi ke objek Python
available_tools = {
    "get_stock_data": get_stock_data,
    "search_market_news": search_market_news
}

# ==========================
# 2. Skema Tool untuk Hermes
# ==========================
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_data",
            "description": "Mengambil harga saham terkini dan histori 5 hari terakhir berdasarkan simbol ticker (misal: BBCA.JK, AAPL).",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {"type": "string", "description": "Simbol ticker saham, misal BBCA.JK"}
                },
                "required": ["ticker"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_market_news",
            "description": "Mencari artikel berita pasar finansial atau sentimen terkini berdasarkan kata kunci.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Kata kunci pencarian berita"}
                },
                "required": ["query"]
            }
        }
    }
]

# ==========================
# 3. Agent Execution Loop
# ==========================
def run_agent(user_query: str):
    messages = [
        {
            "role": "system",
            "content": "Kamu adalah analis finansial otonom. Gunakan tools yang tersedia untuk mengumpulkan fakta harga dan berita terbaru sebelum menarik kesimpulan."
        },
        {"role": "user", "content": user_query}
    ]

    print(f"\n[User Query]: {user_query}\n")

    while True:
        response = client.chat.completions.create(
            model="hermes3:8b",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )
        
        response_msg = response.choices[0].message
        messages.append(response_msg)

        # Cek apakah model meminta eksekusi tool
        if response_msg.tool_calls:
            for tool_call in response_msg.tool_calls:
                func_name = tool_call.function.name
                func_args = json.loads(tool_call.function.arguments)
                
                print(f"[Agent Calling Tool]: {func_name} dengan argumen {func_args}")
                
                tool_function = available_tools.get(func_name)
                tool_output = tool_function(**func_args) if tool_function else "Tool tidak ditemukan."

                # Kirim hasil eksekusi tool kembali ke Hermes
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": func_name,
                    "content": tool_output
                })
        else:
            # Jika tidak ada tool yang dipanggil lagi, tampilkan jawaban final
            print("\n[Laporan Final Analisis]:\n")
            print(response_msg.content)
            break

if __name__ == "__main__":
    prompt = "Cek performa saham BBCA.JK terbaru dan cari sentimen berita perbankan terkait, lalu berikan analisis singkat."
    run_agent(prompt)