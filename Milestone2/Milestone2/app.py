import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go # For Radar Chart
from skill_analyzer_core import extract_skills_multi_method, calculate_similarity_matrix
from typing import List, Dict


from pdfminer.high_level import extract_text as extract_text_from_pdf
import docx
import io 


CHART_COLORS = {
    "Technical": '#1565c0', 
    "Soft": '#ff8f00', 
    "Matched": '#388e3c', 
    "Needed": '#d32f2f', 
    "Extra": '#005080'
}
RESUME_COLOR = '#00bcd4'
JD_COLOR = '#ff4b4b'


st.set_page_config(
    page_title="AI Skill Gap Analyzer",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
.skill-tag {
    display: inline-block; 
    padding: 6px 12px; 
    margin: 4px; 
    border-radius: 20px; 
    font-weight: 500; 
    transition: transform 0.2s; /* Subtle hover effect */
    box-shadow: 1px 1px 3px rgba(0,0,0,0.2);
}
.skill-tag:hover {
    transform: translateY(-2px);
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
}
.tech-tag {background-color: #e3f2fd; color: #1565c0; border: 1px solid #90caf9;}
.soft-tag {background-color: #fff3e0; color: #ff8f00; border: 1px solid #ffcc80;}
.match-tag {background-color: #e8f5e9; color: #388e3c; border: 1px solid #a5d6a7;}
.gap-tag {background-color: #ffebee; color: #d32f2f; border: 1px solid #ef9a9a;}

/* Streamlit Metric Enhancement */
div[data-testid="stMetric"] {
    background-color: #1e1e1e; /* Dark background */
    border-radius: 10px;
    padding: 10px 15px;
}
</style>
""", unsafe_allow_html=True)




def display_skills_as_tags(skills_data: List[Dict], tag_class: str = None):
    """Displays skill data as styled HTML tags with tooltips."""
    html_str = ""
    for item in skills_data:
        skill = item['skill']
        skill_type = item['type']
        
        
        tooltip = f"{skill_type} Skill"
        
        base_class = tag_class or (f"{skill_type[:4].lower()}-tag" if skill_type in ('Technical', 'Soft') else 'skill-tag')
        
        html_str += f'<span class="skill-tag {base_class}" title="{tooltip}">{skill} ({skill_type})</span>'
    st.markdown(html_str, unsafe_allow_html=True)


def get_table_download_link(df: pd.DataFrame, filename: str, text: str):
    """Generates a link to download the DataFrame as a CSV."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="font-size: 14px; text-decoration: none; background-color: #388e3c; color: white; padding: 8px 15px; border-radius: 5px; display: inline-block;">{text}</a>'
    return href


def extract_text_from_upload(uploaded_file):
    """
    Reads the content of the uploaded file, supporting TXT, PDF, and DOCX.
    """
    if uploaded_file is None:
        return None
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    text = ""

    try:
        file_buffer = io.BytesIO(uploaded_file.read())
        file_buffer.seek(0)

        if file_extension == 'txt':
            text = file_buffer.getvalue().decode("utf-8")
        
        elif file_extension == 'pdf':
            text = extract_text_from_pdf(file_buffer)

        elif file_extension == 'docx':
            doc = docx.Document(file_buffer)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
        
        else:
            st.warning(f"Unsupported file type: .{file_extension}. Extraction skipped.")
            return None
        
        if not text.strip():
            st.warning(f"File {uploaded_file.name} was successfully read, but no readable text was extracted.")
            return None

        return text

    except Exception as e:
        st.error(f"Text Extraction FAILED for {uploaded_file.name}. Error: {e}")
        return None



def create_skill_type_distribution_chart(data_list: List[Dict], title: str):
    """CHART 1 & 2: Creates a Plotly Bar Chart for Technical vs Soft skill distribution."""
    if not data_list:
        st.warning(f"No skills extracted for {title}")
        return

    df = pd.DataFrame(data_list)
    distribution_df = df.groupby('type').size().reset_index(name='Count')
    distribution_df = distribution_df.sort_values('Count', ascending=False)

    total = distribution_df['Count'].sum()
    if total > 0:
        distribution_df['Percent'] = (distribution_df['Count'] / total * 100).round(1)
    else:
        distribution_df['Percent'] = 0

    # Limit color map to only the types present to avoid unexpected mapping behavior
    color_map = {k: v for k, v in CHART_COLORS.items() if k in distribution_df['type'].unique()}

    # Show both count and percent in the bar text and provide a clean hover template
    fig = px.bar(
        distribution_df,
        x='type',
        y='Count',
        color='type',
        color_discrete_map=color_map,
        title=title,
        text=distribution_df['Count'].astype(str) + ' (' + distribution_df['Percent'].astype(str) + '%)'
    )

    # Attach percent as customdata for hovertemplate
    fig.update_traces(
        textposition='outside',
        customdata=distribution_df[['Percent']].values,
        hovertemplate='%{x}<br>Count: %{y}<br>Percent: %{customdata[0]}%'
    )

    fig.update_layout(xaxis_title="", yaxis_title="Number of Skills", showlegend=False, yaxis=dict(rangemode='tozero'))
    st.plotly_chart(fig, use_container_width=True)

def create_skill_gap_chart(matched, needed, extra):
    """CHART 3: Creates a chart visualizing the counts of Matched, Needed, and Extra skills."""
    df_gap = pd.DataFrame({
        'Category': ['Matched', 'Needed', 'Extra'],
        'Count': [len(matched), len(needed), len(extra)]
    })
    
    fig = px.bar(df_gap, x='Category', y='Count', color='Category', color_discrete_map=CHART_COLORS, title="Overall Skill Gap and Overlap", text='Count')
    fig.update_layout(xaxis_title="", yaxis_title="Skill Count", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def create_top_skills_chart(data_list: List[Dict], title: str, top_n: int = 8):
    """CHART 4: Creates a bar chart for the top N most frequent skills."""
    if not data_list:
        st.warning(f"No skills extracted for {title}")
        return

    all_extracted_skills = [item['skill'] for item in data_list]
    skill_counts = pd.Series(all_extracted_skills).value_counts().reset_index()
    skill_counts.columns = ['skill', 'Count']
    top_skills_df = skill_counts.head(top_n)

    type_map = {item['skill']: item['type'] for item in data_list}
    top_skills_df['type'] = top_skills_df['skill'].map(type_map)

    fig = px.bar(
        top_skills_df,
        x='Count',
        y='skill',
        color='type',
        color_discrete_map=CHART_COLORS,
        title=f"Top {top_n} Skills - {title}",
        orientation='h'
    )
    fig.update_layout(xaxis_title="Frequency / Count", yaxis_title="", showlegend=True, height=350)
    st.plotly_chart(fig, use_container_width=True)

def create_radar_chart(resume_data: List[Dict], jd_data: List[Dict]):
    """NEW FEATURE: Creates a Radar Chart comparing skill type distribution."""
    
    def get_skill_distribution(data):
        if not data:
            return {}
        df = pd.DataFrame(data)
        return df.groupby('type').size().to_dict()

    res_dist = get_skill_distribution(resume_data)
    jd_dist = get_skill_distribution(jd_data)
    
    # Build categories preserving preferred order (Technical, Soft) first
    union_types = list(dict.fromkeys(list(res_dist.keys()) + list(jd_dist.keys())))
    preferred = ['Technical', 'Soft']
    categories = [t for t in preferred if t in union_types] + [t for t in union_types if t not in preferred]

    # If no categories found, default to Technical/Soft
    if not categories:
        categories = ['Technical', 'Soft']

    # Compute per-dataset percentage distribution (each sums to 100)
    def to_percent_distribution(count_map, categories):
        total = sum(count_map.values()) if count_map else 0
        if total == 0:
            return [0.0 for _ in categories]
        return [round((count_map.get(c, 0) / total) * 100, 1) for c in categories]

    r_percent = to_percent_distribution(res_dist, categories)
    jd_percent = to_percent_distribution(jd_dist, categories)

    # Close the loop for radar
    r_plot = r_percent + [r_percent[0]]
    jd_plot = jd_percent + [jd_percent[0]]
    theta = categories + [categories[0]]

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=r_plot,
        theta=theta,
        fill='toself',
        name='Resume',
        marker_color=RESUME_COLOR,
        line_color=RESUME_COLOR,
        hovertemplate='%{theta}: %{r}%<extra>Resume</extra>'
    ))
    fig.add_trace(go.Scatterpolar(
        r=jd_plot,
        theta=theta,
        fill='toself',
        name='Job Description',
        marker_color=JD_COLOR,
        line_color=JD_COLOR,
        hovertemplate='%{theta}: %{r}%<extra>Job Description</extra>'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tick0=0,
                dtick=20,
                showticklabels=True
            )
        ),
        showlegend=True,
        title='Skill Balance Comparison (Radar Chart)'
    )

    st.plotly_chart(fig, use_container_width=True)


# main start from here

def main():
    st.title("🧠 AI-Powered Skill Gap Analyzer")
    st.subheader("Milestone 2: Multi-Method Extraction & BERT Embeddings")
    st.markdown("---")

    # Sidebar
    st.sidebar.header("📂 Upload Documents")
    
    allowed_types = ['txt', 'pdf', 'docx']
    
    resume_file = st.sidebar.file_uploader("Upload **Resume** (.txt, .pdf, .docx)", type=allowed_types, key='resume_upload')
    jd_file = st.sidebar.file_uploader("Upload **Job Description (JD)** (.txt, .pdf, .docx)", type=allowed_types, key='jd_upload')
    
    # --- Extract Text ---
    resume_text = extract_text_from_upload(resume_file)
    jd_text = extract_text_from_upload(jd_file)

    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚀 Analyze Skills", type="primary"):
        if not resume_text or not jd_text:
            st.error("Please upload both a Resume file and a Job Description file to continue.")
            return

        with st.spinner('Running Multi-Method NLP Pipeline and Generating BERT Embeddings...'):
            # --- 1. Skill Extraction ---
            resume_data = extract_skills_multi_method(resume_text, "resume")
            jd_data = extract_skills_multi_method(jd_text, "jd")

            resume_skills = [item['skill'] for item in resume_data]
            jd_skills = [item['skill'] for item in jd_data]
            
            # --- Analysis for Metrics and Charts ---
            set_resume = set(resume_skills)
            set_jd = set(jd_skills)
            common_skills = sorted(list(set_resume.intersection(set_jd)))
            needed_skills = sorted(list(set_jd.difference(set_resume)))
            extra_skills = sorted(list(set_resume.difference(set_jd)))
            
            common_data = [{"skill": s, "type": next((d['type'] for d in resume_data if d['skill'] == s), 'Unknown')} for s in common_skills]
            needed_data = [{"skill": s, "type": next((d['type'] for d in jd_data if d['skill'] == s), 'Unknown')} for s in needed_skills]


            # --- 2. Comprehensive Visualizations (Including NEW Radar Chart) ---
            st.header("📈 Skill Visualizations")
            
            # NEW: Radar Chart for Skill Balance Comparison
            st.subheader("1. Skill Balance Comparison ")
            create_radar_chart(resume_data, jd_data)
            
            # CHART 1 & 2: Skill Type Distribution
            st.subheader("2. Skill Type Distribution")
            col_chart_res, col_chart_jd = st.columns(2)
            with col_chart_res:
                create_skill_type_distribution_chart(resume_data, "Resume Skill Distribution")
            with col_chart_jd:
                create_skill_type_distribution_chart(jd_data, "Job Description Distribution")

            st.markdown("---")
            
            # CHART 3: Overall Skill Gap
            st.subheader("3. Overall Skill Gap and Overlap")
            create_skill_gap_chart(common_skills, needed_skills, extra_skills)
            
            st.markdown("---")
            
            # CHART 4: Top N Skills Comparison
            st.subheader("4. Top Skills Comparison")
            col_top_res, col_top_jd = st.columns(2)
            with col_top_res:
                create_top_skills_chart(resume_data, "Resume", top_n=8)
            with col_top_jd:
                create_top_skills_chart(jd_data, "Job Description", top_n=8)

            st.markdown("---")

            # --- 3. Enhanced Skill Gap and Overlap Metrics ---
            st.header("📊 Skill Gap and Overlap Metrics ")
            
            col_c, col_n, col_e = st.columns(3)

            with col_c:
                st.metric("✅ Skills Matched", value=len(common_skills))
                st.markdown("**Common Skills:**")
                display_skills_as_tags(common_data, 'match-tag')
                
            with col_n:
                st.metric("⚠️ Skill Gap (Needed)", value=len(needed_skills))
                st.markdown("**Required Skills Missing:**")
                display_skills_as_tags(needed_data, 'gap-tag')

            with col_e:
                st.metric("🌟 Extra Skills on Resume", value=len(extra_skills))
                st.markdown("**Skills Not Required by JD:**")
                
                if len(extra_skills) < 15:
                    st.markdown(f"*{', '.join(extra_skills)}*")
                else:
                     st.markdown(f"*{', '.join(extra_skills[:15])} + {len(extra_skills) - 15} more...*")


            # --- 4. BERT Similarity Visualization ---
            st.header("🧠 BERT Semantic Similarity Matrix")
            st.info("Uses Sentence-BERT to determine how closely related each resume skill is to each JD skill.")
            
            similarity_df = calculate_similarity_matrix(resume_skills, jd_skills)
            
            st.dataframe(
                similarity_df.style.background_gradient(cmap='Blues', axis=None).format(precision=2),
                use_container_width=True
            )
            
            # --- 5. Data Export ---
            st.header("💾 Data Export Options")
            
            export_df = pd.DataFrame({
                "Source": ["Resume"] * len(resume_data) + ["Job Description"] * len(jd_data),
                "Skill Name": resume_skills + jd_skills,
                "Skill Type": [d['type'] for d in resume_data] + [d['type'] for d in jd_data],
                "Analysis": ["Present"] * len(resume_data) + ["Required"] * len(jd_data)
            })

            col_csv, col_md = st.columns(2)
            with col_csv:
                
                st.markdown(get_table_download_link(export_df, "extracted_skills_report.csv", "⬇️ Download All Extracted Skills (CSV)"), unsafe_allow_html=True)
            with col_md:
                
                st.markdown('<div style="background-color: #616161; color: white; padding: 8px 15px; border-radius: 5px; opacity: 0.7; text-align: center;">Download Analysis Report (JSON/PDF )</div>', unsafe_allow_html=True)


# --- 6. Custom NER/Annotation Interface Placeholder ---
st.sidebar.markdown("---")
st.sidebar.header("🛠️ Custom NER Training")
st.sidebar.markdown("""
**1. Annotation Interface **: Requires a dedicated tool (Prodigy/doccano) to label data.
**2. Custom NER Training Capability**: Requires a script to fine-tune a spaCy or BERT model using the labeled data.
""")


if __name__ == "__main__":
    main()