import streamlit as st
import pandas as pd
import numpy as np
import base64
import subprocess
import os
import argparse
import pickle

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
    # 页面标题和介绍
    st.markdown("<h1 style='text-align: center;'>DS Finder</h1>", unsafe_allow_html=True)
    st.image("figure 6a1.tif", use_column_width=True)
    st.write("We developed a machine learning model called **DS Finder** (**D**eleterious **S**ynonymous mutations **Finder**), significantly outperformed existing prediction models. DS Finder considers cell type, tissue type, and gene background when making predictions. You can use our algorithm to predict deleterious synonymous mutations of interest. Give it a try!")
    st.markdown("[Visit our github page](https://github.com/UronicAcid/DS-Finder)", unsafe_allow_html=True)
    
    # 定义必填的特征
    required_columns = [
        'expression_log', 'gene_effect', 'original_codon_freq', 'mutated_codon_freq',
        'mutated_codon_norm_freq', 'codon_freq_norm_change', 'splicing_score',
        'silva_X.GERP..', 'silva_dRSCU', 'absplice_tissue', 'CADD_RawScore',
        'position', 'gene_aa_num', 'wildtype_energy', 'energy_change',
        'energy_change_abs_ratio', 'silva_CpG_exon', 'silva_X.CpG.', 'DS_DL',
        'DS_DG', 'mutated_codon_index3', 'original_codon_index3'
    ]
    
    # 用户输入每个特征的值
    feature_values = {}
    #for feature in required_columns[:-2]:  # Exclude 'mutated_codon_index3' and 'original_codon_index3'
    #    feature_values[feature] = st.number_input(f"{feature}:", value=0.0, min_value=0.0, max_value=1.0)
    
    feature_values['position'] = st.number_input("position:", value=46, min_value=0)
    feature_values['gene_aa_num'] = st.number_input("gene_aa_num:", value=656, min_value=0)
    feature_values['expression_log'] = st.number_input("Expression (log):", value=7.1, min_value=0.0)
    feature_values['gene_effect'] = st.number_input("Gene effect:", value=-0.06, min_value=-10.0, max_value=10.0)
    feature_values['original_codon_freq'] = st.number_input("Original_codon_freq:", value=34.23, min_value=0.0)
    feature_values['mutated_codon_freq'] = st.number_input("Mutated_codon_freq:", value=312.34, min_value=0.0)
    feature_values['mutated_codon_norm_freq'] = st.number_input("Mutated_codon_freq (normalized):", value=0.25, min_value=0.0)
    feature_values['codon_freq_norm_change'] = st.number_input("Codon_freq_change (normalized):", value=-0.5)
    feature_values['silva_dRSCU'] = st.number_input("dRSCU:", value=0.529)
    feature_values['splicing_score'] = st.number_input("Splicing_score:", value=0.02, min_value=0.0, max_value=1.0)
    feature_values['DS_DL'] = st.number_input("DS_DL:", value=0.02)
    feature_values['DS_DG'] = st.number_input("DS_DG:", value=0)
    feature_values['absplice_tissue'] = st.number_input("absplice_tissue:", value=0.038, min_value=0.0, max_value=1.0)
    feature_values['wildtype_energy'] = st.number_input("wildtype_energy:", value=-913.0, max_value=0.0)
    feature_values['energy_change'] = st.number_input("energy_change:", value=2.9)
    feature_values['energy_change_abs_ratio'] = st.number_input("energy_change_abs_ratio:", value=0.003, min_value=0.0)
    feature_values['CADD_RawScore'] = st.number_input("CADD_RawScore:", value=2.81)
    feature_values['silva_X.GERP..'] = st.number_input("GERP:", value=4.98)
    feature_values['silva_CpG_exon'] = st.number_input("silva_CpG_exon:", value=0.7708)
    feature_values['silva_X.CpG.'] = st.number_input("silva_CpG_exon:", value=0)

    
    # 'mutated_codon_index3' 和 'original_codon_index3' 使用 st.selectbox 选择
    codon_choices = ['A', 'T', 'C', 'G']
    feature_values['mutated_codon_index3'] = st.selectbox("Mutated_codon_index3:", codon_choices)
    feature_values['original_codon_index3'] = st.selectbox("Original_codon_index3:", codon_choices)

    
    # 模型选择下拉菜单
    model_options = [
        "HCT116"
    ]
    selected_model = st.selectbox("Select a model:", model_options)
    
    # 按钮触发预测
    if st.button("Predict"):
        # 将输入的数据转换为DataFrame
        input_df = pd.DataFrame([feature_values])
        
        # 保存输入的数据到临时CSV文件
        temp_dataset_path = 'temp_test_dataset.csv'
        input_df.to_csv(temp_dataset_path, index=False)

        # 模型路径
        model_dir = 'model'  # 模型文件存储的目录
        if selected_model == "HCT116":
            model_full_name= "241110_catboost_model_trained_on_HCT116_D35_depleted_seed2_ratio10.sav"
        model_path = os.path.join(model_dir, model_full_name)
                
        # 输出路径
        output_path = 'temp_output.csv'
        
        # 预测脚本路径
        prediction_script_path = 'DS-Finder-main/prediction.py'
        
        # 构造命令行参数
        command = [
            'python', prediction_script_path,
            '--model_path', 'DS-Finder-main/' + model_path,
            '--dataset_path', temp_dataset_path,
            '--output_path', output_path
        ]
        
        try:
            # 调用命令行脚本进行预测
            subprocess.run(command, check=True)
            
            # 读取预测结果并显示
            output_df = pd.read_csv(output_path)
            st.write("Prediction Result:")
            st.write(output_df['predicted_y_score'])

        except subprocess.CalledProcessError as e:
            st.error(f"Error during prediction: {e}")
        finally:
            # 清理临时文件
            os.remove(temp_dataset_path)
            if os.path.exists(output_path):
                os.remove(output_path)

def contact_us_page():
    st.markdown("<h1 style='text-align: center;'>Contact Us</h1>", unsafe_allow_html=True)
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
