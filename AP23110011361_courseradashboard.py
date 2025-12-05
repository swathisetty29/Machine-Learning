import streamlit as st
import pandas as pd
import plotly.express as px

# BACKGROUND + WHITE TEXT
st.markdown("""
<style>
.stApp {
    background-color: black;
    color: white;
}
h1, h2, h3, h4, h5, h6, p, div, span {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

#headline
st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DATA 
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.replace(' ', '_').str.lower()

    # numeric columns
    score_cols = ['math_score', 'reading_score', 'writing_score']
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(subset=score_cols, inplace=True)
    df['avg_score'] = df[score_cols].mean(axis=1)

    return df

DATA_FILE = 'StudentsPerformance.csv'
df_full = load_data(DATA_FILE)

st.title(" Student Academic Performance Analysis")
st.markdown("Use the filters on the left to analyze score trends and distributions.")

# SIDEBAR
st.sidebar.title(" Dashboard Filters")

race_options = df_full['race/ethnicity'].unique().tolist()
selected_race = st.sidebar.multiselect(
    "1️ Select Race/Ethnicity:",
    options=race_options,
    default=race_options
)

prep_options = df_full['test_preparation_course'].unique().tolist()
selected_prep = st.sidebar.multiselect(
    "2️ Test Preparation Status:",
    options=prep_options,
    default=prep_options
)

min_avg = int(df_full['avg_score'].min())
max_avg = int(df_full['avg_score'].max())
avg_score_range = st.sidebar.slider(
    "3️Average Score Range:",
    min_value=min_avg,
    max_value=max_avg,
    value=(50, max_avg)
)

chart_1_type = st.sidebar.selectbox(
    "4️ Select Chart 1 Type:",
    (
        'Bar Chart (Scores by Education)',
        'Histogram (Math Score)',
        'Box Plot (Math Score)',
        'Pie Chart (Test Prep Status)'
    )
)

# APPLY FILTERS 
df_filtered = df_full[
    (df_full['race/ethnicity'].isin(selected_race)) &
    (df_full['test_preparation_course'].isin(selected_prep)) &
    (df_full['avg_score'] >= avg_score_range[0]) &
    (df_full['avg_score'] <= avg_score_range[1])
]

if df_filtered.empty:
    st.warning(" No students match the selected filters. Please adjust your selections.")
    st.stop()

#  KPIs 
st.header(" Key Performance Indicators (KPIs)")

total_students = len(df_filtered)
avg_math = df_filtered['math_score'].mean()
avg_reading = df_filtered['reading_score'].mean()
avg_writing = df_filtered['writing_score'].mean()
overall_avg = df_full['avg_score'].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total Students", value=f"{total_students:,}")

with col2:
    delta_val = avg_math - overall_avg
    st.metric(
        label="Average Math Score",
        value=f"{avg_math:.1f}",
        delta=f"{delta_val:.1f} vs Full Avg"
    )

with col3:
    st.metric(label=" Average Reading Score", value=f"{avg_reading:.1f}")

with col4:
    st.metric(label=" Average Writing Score", value=f"{avg_writing:.1f}")

#VISUALIZATIONS
st.markdown("---")
st.header(" Detailed Performance Visualizations")

chart_col1, chart_col2 = st.columns(2)

# Chart 1: Dynamic Chart
with chart_col1:
    if chart_1_type == 'Bar Chart (Scores by Education)':
        st.subheader("Average Scores by Parental Education")
        df_scores_by_edu = (
            df_filtered
            .groupby('parental_level_of_education')[['math_score', 'reading_score', 'writing_score']]
            .mean()
            .reset_index()
        )
        fig_primary = px.bar(
            df_scores_by_edu.melt(
                id_vars='parental_level_of_education',
                var_name='Subject',
                value_name='Average Score'
            ),
            x='parental_level_of_education',
            y='Average Score',
            color='Subject',
            title="Average Score by Parental Education",
            height=450,
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig_primary.update_layout(xaxis={'tickangle': -25}, template='plotly_dark')

    elif chart_1_type == 'Histogram (Math Score)':
        st.subheader("Distribution of Math Scores")
        fig_primary = px.histogram(
            df_filtered,
            x='math_score',
            color='gender',
            marginal="box",
            opacity=0.7,
            nbins=20,
            title="Frequency of Math Scores by Gender",
            height=450,
            template='plotly_dark'
        )

    elif chart_1_type == 'Box Plot (Math Score)':
        st.subheader("Math Score Quartiles and Outliers")
        fig_primary = px.box(
            df_filtered,
            x='gender',
            y='math_score',
            color='gender',
            notched=True,
            title="Math Score Distribution by Gender",
            height=450,
            template='plotly_dark'
        )

    elif chart_1_type == 'Pie Chart (Test Prep Status)':
        st.subheader("Proportion by Test Preparation Status")
        fig_primary = px.pie(
            df_filtered,
            names='test_preparation_course',
            title="Student Proportion by Test Preparation Status",
            height=450,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            template='plotly_dark'
        )

    st.plotly_chart(fig_primary, use_container_width=True)

# Chart 2: Fixed Scatter Plot
with chart_col2:
    st.subheader("Reading Score vs. Writing Score")
    fig_secondary = px.scatter(
        df_filtered,
        x='reading_score',
        y='writing_score',
        color='gender',
        hover_data=['math_score', 'race/ethnicity'],
        title="Relationship between Reading and Writing Scores",
        height=450,
        template='plotly_dark'
    )
    st.plotly_chart(fig_secondary, use_container_width=True)

#RAW DATA TABLE
st.markdown("---")
with st.expander(" View Filtered Student Data Table"):
   
    df_display = df_filtered.sort_values('avg_score', ascending=False).drop(columns=['avg_score'])
    st.dataframe(df_display, use_container_width=True)
