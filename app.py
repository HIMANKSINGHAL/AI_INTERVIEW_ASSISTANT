import streamlit as st
import pandas as pd
import numpy as np
import pickle
import re
import time
import os

from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(__file__)

st.set_page_config(page_title="AI Technical Interview Assistant", page_icon="🎓", layout="wide")


def tokenize(text):
    return set(re.findall(r"[a-z]+", str(text).lower()))


def compute_features(model_answer, student_answer, keywords, vectorizer):
    m_vec = vectorizer.transform([model_answer])
    s_vec = vectorizer.transform([student_answer])
    tfidf_cosine_sim = cosine_similarity(m_vec, s_vec)[0][0]

    m_tok, s_tok = tokenize(model_answer), tokenize(student_answer)
    union = m_tok | s_tok
    jaccard_sim = len(m_tok & s_tok) / len(union) if union else 0.0

    kw_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    s_lower = student_answer.lower()
    keyword_overlap = sum(1 for k in kw_list if k in s_lower) / len(kw_list) if kw_list else 0.0

    m_len = max(1, len(model_answer.split()))
    s_len = len(student_answer.split())
    length_ratio = min(s_len / m_len, 3.0)
    word_count = s_len

    return np.array([[tfidf_cosine_sim, jaccard_sim, keyword_overlap, length_ratio, word_count]]), keyword_overlap, tfidf_cosine_sim


def evaluate_answer(model, scaler, vectorizer, label_encoder, model_answer, student_answer, keywords):
    feats, kw_overlap, sim = compute_features(model_answer, student_answer, keywords, vectorizer)
    feats_scaled = scaler.transform(feats)

    pred_encoded = model.predict(feats_scaled)[0]
    pred_label = label_encoder.inverse_transform([pred_encoded])[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(feats_scaled)[0]
        confidence = round(max(proba) * 100, 1)

    estimated_score = int(round((sim * 0.6 + kw_overlap * 0.4) * 100))
    missing_kws = [k.strip() for k in keywords.split(",") if k.strip().lower() not in student_answer.lower()]

    return {
        "label": pred_label,
        "confidence": confidence,
        "estimated_score": estimated_score,
        "missing_keywords": missing_kws,
    }


@st.cache_resource
def load_artifacts():
    with open(os.path.join(BASE_DIR, "best_model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(BASE_DIR, "label_encoder.pkl"), "rb") as f:
        label_encoder = pickle.load(f)
    with open(os.path.join(BASE_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    with open(os.path.join(BASE_DIR, "tfidf_vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
    with open(os.path.join(BASE_DIR, "best_model_name.txt")) as f:
        best_model_name = f.read().strip()
    comparison_df = pd.read_csv(os.path.join(BASE_DIR, "model_comparison.csv"))
    return model, label_encoder, scaler, vectorizer, best_model_name, comparison_df


@st.cache_data
def load_question_bank():
    df = pd.read_csv(os.path.join(BASE_DIR, "interview_dataset_clean.csv"))
    qbank = df.drop_duplicates(subset=["question"])[
        ["field", "question", "model_answer", "keywords", "difficulty"]
    ].reset_index(drop=True)
    return qbank


model, label_encoder, scaler, vectorizer, best_model_name, comparison_df = load_artifacts()
qbank = load_question_bank()

st.sidebar.title("🎓 AI Interview Assistant")
page = st.sidebar.radio(
    "Navigate",
    ["Practice Mode", "Mock Interview", "Model Performance"]
)

FIELDS = sorted(qbank["field"].unique().tolist())

if page == "Practice Mode":
    st.title("Practice Mode")
    col1, col2 = st.columns([1, 1])
    with col1:
        selected_field = st.selectbox("Choose a topic", FIELDS)

    if "current_q" not in st.session_state or st.session_state.get("field") != selected_field:
        st.session_state["field"] = selected_field
        st.session_state["current_q"] = qbank[qbank["field"] == selected_field].sample(1).iloc[0]

    if st.button("🔄 Get a new question"):
        st.session_state["current_q"] = qbank[qbank["field"] == selected_field].sample(1).iloc[0]
        st.session_state.pop("last_result", None)

    q_row = st.session_state["current_q"]

    st.markdown("### ❓ Question")
    st.info(f"**[{q_row['difficulty']}]** {q_row['question']}")

    user_answer = st.text_area("Your answer:", height=150, placeholder="Type your answer here...")

    if st.button("Submit Answer", type="primary"):
        if not user_answer.strip():
            st.warning("Please type an answer before submitting.")
        else:
            res = evaluate_answer(
                model, scaler, vectorizer, label_encoder,
                q_row["model_answer"], user_answer, q_row["keywords"],
            )
            res["model_answer"] = q_row["model_answer"]
            st.session_state["last_result"] = res

    if "last_result" in st.session_state:
        res = st.session_state["last_result"]
        st.markdown("---")
        st.markdown("### 📊 Evaluation")

        rc1, rc2, rc3 = st.columns(3)
        rc1.metric("Rating", res["label"])
        rc2.metric("Estimated Score", f"{res['estimated_score']} / 100")
        if res["confidence"]:
            rc3.metric("Model Confidence", f"{res['confidence']}%")

        label_colors = {"Excellent": "success", "Good": "info", "Average": "warning", "Poor": "error"}
        getattr(st, label_colors.get(res["label"], "info"))(f"Overall rating: **{res['label']}**")

        st.markdown("#### 💡 Suggestions")
        if res["label"] == "Excellent":
            st.write("Great answer! You covered the concept clearly and accurately.")
        else:
            if res["missing_keywords"]:
                st.write(f"- Consider mentioning these key terms: **{', '.join(res['missing_keywords'])}**")
            if res["estimated_score"] < 70:
                st.write("- Try to explain the concept more completely, similar in depth to a textbook definition.")
            st.write(f"- **Model answer for reference:** {res['model_answer']}")

elif page == "Mock Interview":
    st.title("🎙️ Mock Interview")
    if "iv" not in st.session_state:
        st.session_state["iv"] = None

    if st.session_state["iv"] is None:
        c1, c2 = st.columns(2)
        with c1:
            iv_field = st.selectbox("Interview topic", FIELDS, key="iv_field_select")
        with c2:
            n_questions = st.select_slider("Number of questions", options=[3, 5, 8], value=5)

        if st.button("Start Mock Interview", type="primary"):
            pool = qbank[qbank["field"] == iv_field]
            n = min(n_questions, len(pool))
            questions = pool.sample(n).to_dict("records")
            st.session_state["iv"] = {
                "field": iv_field, "questions": questions, "idx": 0,
                "results": [], "q_start_time": time.time(),
            }
            st.rerun()

    else:
        iv = st.session_state["iv"]

        if iv["idx"] < len(iv["questions"]):
            q = iv["questions"][iv["idx"]]
            st.progress((iv["idx"]) / len(iv["questions"]))
            st.markdown(f"**Question {iv['idx'] + 1} of {len(iv['questions'])}** — Topic: {iv['field']}")
            st.info(f"**[{q['difficulty']}]** {q['question']}")

            answer_key = f"iv_answer_{iv['idx']}"
            user_answer = st.text_area("Your answer:", height=150, key=answer_key)

            if st.button("Submit & Continue", type="primary"):
                elapsed = round(time.time() - iv["q_start_time"], 1)
                if not user_answer.strip():
                    st.warning("Please type an answer before continuing.")
                else:
                    res = evaluate_answer(
                        model, scaler, vectorizer, label_encoder,
                        q["model_answer"], user_answer, q["keywords"],
                    )
                    res.update({
                        "question": q["question"], "difficulty": q["difficulty"],
                        "time_taken": elapsed, "model_answer": q["model_answer"],
                    })
                    iv["results"].append(res)
                    iv["idx"] += 1
                    iv["q_start_time"] = time.time()
                    st.rerun()

            if st.button("End Interview Early"):
                iv["idx"] = len(iv["questions"])
                st.rerun()

        else:
            st.success("Interview complete! Here's your performance report.")
            results = iv["results"]

            if not results:
                st.warning("No questions were answered.")
            else:
                report_df = pd.DataFrame([{
                    "Question": r["question"][:60] + ("..." if len(r["question"]) > 60 else ""),
                    "Difficulty": r["difficulty"],
                    "Rating": r["label"],
                    "Score": r["estimated_score"],
                    "Time (sec)": r["time_taken"],
                } for r in results])

                avg_score = round(report_df["Score"].mean(), 1)
                total_time = round(report_df["Time (sec)"].sum(), 1)

                if avg_score >= 85:
                    verdict, verdict_color = "Strong Hire", "success"
                elif avg_score >= 65:
                    verdict, verdict_color = "Hire", "success"
                elif avg_score >= 45:
                    verdict, verdict_color = "Borderline — More Practice Needed", "warning"
                else:
                    verdict, verdict_color = "Not Ready Yet", "error"

                m1, m2, m3 = st.columns(3)
                m1.metric("Average Score", f"{avg_score} / 100")
                m2.metric("Questions Answered", len(results))
                m3.metric("Total Time", f"{total_time}s")

                getattr(st, verdict_color)(f"**Overall Verdict: {verdict}**")

                st.markdown("#### 📋 Question-by-Question Breakdown")
                st.dataframe(report_df, use_container_width=True)
                st.bar_chart(report_df.set_index("Question")["Score"])

                all_missing = [kw for r in results for kw in r["missing_keywords"]]
                if all_missing:
                    st.markdown("#### 🎯 Areas to Revise")
                    top_missing = pd.Series(all_missing).value_counts().head(8)
                    st.write(", ".join(top_missing.index.tolist()))

            if st.button("🔁 Start a New Mock Interview"):
                st.session_state["iv"] = None
                st.rerun()

elif page == "Model Performance":
    st.title("🤖 ML Model Comparison")
    st.dataframe(
        comparison_df.style.highlight_max(subset=["Accuracy", "F1_Score"]),
        use_container_width=True,
    )
