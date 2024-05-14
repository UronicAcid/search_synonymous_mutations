import streamlit as st
import pandas as pd
import numpy as np
import base64

# 示例数据生成函数
df = pd.read_csv("screening_results_feature.csv")

# 下载链接生成函数
def get_table_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="results.csv">Export results as csv</a>'
    return href

# 页面内容函数
def main_page():
    st.markdown("<h1 style='text-align: center;'>Hearing Silence</h1>", unsafe_allow_html=True)
    st.header("Welcome to our research project on the synonymous mutations!")
    st.subheader("Disturb the sound of silence")
    st.write("Synonymous mutations are generally deemed functionally silent and evolutionarily neutral, yet their functional roles and regulatory mechanisms in the human genome have not been systematically explored. Herein, employing the PEmax system, we designed a library containing 297,900 epegRNAs targeting 94,993 synonymous mutations and 39,336 nonsynonymous mutations on 3,644 protein-coding genes and conducted a comprehensive screen to unveil synonymous mutations affecting cell fitness.")
    st.image("figure 1a.tif", use_column_width=True)
    st.subheader("Whisper in the sound of silence")
    st.write("Our findings delineate that the majority of synonymous mutations in the human genome remain neutral, even when they occur in essential genes. Other nonsynonymous mutations, including missense mutations, exhibit more significant effects on cell fitness. But a minority of synonymous mutations can produce phenotypes. These functional synonymous mutations affect a range of biological processes, including mRNA splicing, folding, transcription, and translation.")
    st.image("figure 1c.tif", use_column_width=True)


def search_page():
    st.markdown("<h1 style='text-align: center;'>Querying deleterious synonymous mutations</h1>", unsafe_allow_html=True)
    gene_name = st.text_input("Enter Gene Name", "")
    cell_line = st.selectbox("Select Cell Line", ["HCT116",  "K562"])
    
    # 使用HTML和CSS通过Markdown来居中按钮
    button_html = """
    <style>
    div.stButton > button:first-child {
        margin: 0 auto;
        display: block;
    }
    </style>
    <div style='text-align: center;'>
        <button class="css-qbe2hs edgvbvh1" onclick="document.querySelector('.stButton > button').click();">Search</button>
    </div>
    """
    st.markdown(button_html, unsafe_allow_html=True)
    
    df = my_data
    filtered_df = df[(df["gene"] == gene_name) | (df["cellline"] == cell_line)]
    
    # 使用条件判断是否已经点击了按钮
    if st.session_state.get('button_clicked', False):
        st.write("Results:")
        st.dataframe(filtered_df)
        st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

    # 定义按钮点击事件的处理逻辑
    if st.button('Search'):
        st.session_state['button_clicked'] = True



def search_page():
    st.markdown("<h1 style='text-align: center;'>Querying deleterious synonymous mutations</h1>", unsafe_allow_html=True)
    # 获取DataFrame中所有唯一的基因名称，并按字母顺序排序
    unique_genes = df['gene'].unique()
    unique_genes.sort()  # 可选，如果你想按字母顺序排序的话

    # 使用selectbox代替text_input让用户选择基因名称
    gene_name = st.selectbox("Enter Gene Name", options=unique_genes)
    cell_line = st.selectbox("Select Cell Line", ["HCT116",  "K562"])
    filtered_df = df[(df["gene"] == gene_name) & (df["cellline"] == cell_line)]
    st.write(" ")
    # 添加一个按钮来控制是否显示结果和下载链接
    if st.button('Search'):
        st.dataframe(filtered_df)
        st.markdown(get_table_download_link(filtered_df), unsafe_allow_html=True)

def predict_page():
    st.write("We developed a machine learning model called DS Finder (Deleterious Synonymous mutations Finder), significantly outperformed existing prediction models. DS Finder considers cell type, tissue type, and gene background when making predictions. You can use our algorithm to predict deleterious synonymous mutations of interest. Give it a try!")
    st.markdown("[Visit our github page](https://github.com/UronicAcid/DS-Finder)", unsafe_allow_html=True)
    
def contact_us_page():
    st.header("Contact Us")
    st.write("Email：weilab AT pku.edu.cn")
    st.write("地址：北京市海淀区颐和园路5号 北京大学综合科研2号楼207室")
    st.write("邮编：100871")
    st.markdown("[Visit our lab page](https://weilab.pku.edu.cn/)", unsafe_allow_html=True)
    st.markdown("---")
    st.write("Xuran Niu: crispr_nxr AT 163.com")
    st.write("Wei Tang: tangwei AT stu.pku.edu.cn")
    

# 侧边栏导航设置
#st.sidebar.title("")
page = st.sidebar.radio("", ["Home Page", "Search: Touch the sound of silence", "Predict: Echo in the wells of silence", "Contact Us: Remain within the sound of silence"])

# 页面导航逻辑
if page == "Home Page":
    main_page()
elif page == "Search: Touch the sound of silence":
    search_page()
elif page == "Predict: Echo in the wells of silence":
    predict_page()
elif page == "Contact Us: Remain within the sound of silence":
    contact_us_page()
