from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


if not os.getenv("OPENAI_API_KEY"):
    try:
        os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

PERSONAS = {
    "データ分析の専門家": (
        "You are a senior data analyst. "
        "Be precise and structured. Explain in bullet points and, when helpful, provide a short formula or pseudo code."
    ),
    "栄養士": (
        "You are a licensed dietitian. "
        "Answer with practical nutrition advice, portion examples, and cautions. Keep it friendly and actionable."
    ),
    "ECコンサル（ファッション）": (
        "You are an e-commerce consultant specialized in fashion D2C. "
        "Give conversion-oriented, step-by-step suggestions with quick wins and metrics to track."
    ),
}

def ask_expert(input_text: str, persona_key: str) -> str:
    system_prompt = PERSONAS.get(persona_key, "You are a helpful assistant.")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text),
    ]
    result: AIMessage = llm.invoke(messages)
    return result.content if hasattr(result, "content") else str(result)

st.set_page_config(page_title="専門家切替チャット", page_icon="🤖", layout="centered")

st.title("サンプルアプリ：専門家を切り替えて LLM に質問する")
st.caption(
    "テキストを入力し、下のラジオで“どの専門家に振る舞わせるか”を選ぶと、"
    "選択に応じたシステムメッセージが自動で切り替わります。"
)

with st.expander("このアプリの説明 / 使い方", expanded=False):
    st.markdown(
        "- 入力フォームに質問文を入れてください。\n"
        "- ラジオボタンで専門家の種類を選択すると、その専門家として回答します。\n"
        "- [送信] を押すと結果が表示されます。\n"
        "- ※ デプロイ時は Python 3.11 を使用してください。"
    )

user_text = st.text_area("入力テキスト", placeholder="ここに質問や依頼を書いてください", height=140)

expert = st.radio(
    "LLM に振る舞わせる専門家を選択してください",
    options=list(PERSONAS.keys()),
    horizontal=False,
)

if st.button("送信", type="primary", use_container_width=True):
    if not user_text.strip():
        st.error("テキストを入力してください。")
    else:
        with st.spinner("LLM に問い合わせ中..."):
            try:
                answer = ask_expert(user_text.strip(), expert)
                st.divider()
                st.subheader("回答")
                st.write(answer)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

st.divider()
st.caption("環境変数 OPENAI_API_KEY を利用します（.env もしくは Streamlit Cloud の Secrets）。")
