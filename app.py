import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import mplfinance as mpl
import numpy as np
import plotly.express as px 
import io 
import openpyxl as oxl


htmlview="""
<style>
.st-emotion-cache-jwhd0x{
        border:2px dotted black;
        border-radius: 20px;
        background-color:#F2F7F2;
        box-shadow: 0px 0px 15px 3px rgb(201, 254, 254);
        text-align: center;
        }

.st-emotion-cache-wfksaw {
        padding:20px;
        width:150px;
        text-align: center;
        font-size:15px;
        background-color: #F2F7F2;
        border-radius: 20px;
        box-shadow: 0px 0px 15px 3px rgb(99, 141, 173);
}
.st-emotion-cache-c9q7qe {
        text-size:15px;
}
.st-emotion-cache-79elbk{
        border: 1px;
        padding:15px;
        width:400px;
        text-align: center;
        background-color: rgb(250, 250, 250);
        border-radius: 20px;
        box-shadow: 0px 0px 15px 3px rgb(99, 141, 173);
}
.st-emotion-cache-5qfegl{
        border: 1px;
        padding:20px;
        width:170px;
        text-align: center;
        background-color: rgb(250, 250, 250);
        border-radius: 20px;
        box-shadow: 0px 0px 15px 3px rgb(99, 141, 173);
        
}
.st-emotion-cache-ftjf6z{
        position: relative;
        left: 300px;
}
.st-emotion-cache-1ml8qm {
        width:140px;
        font-size:18px;
        margin-left:-8px;
        text-align:center;
}
.st-emotion-cache-15okssx{
        margin:0px 25px;
}
.st-emotion-cache-c9q7qe{
    font-size:20px;    
}
.st-dm{
        background:none;
}
.d1{
        min-width: 250px;
        max-width: 400px;
        width: 300px;
        padding: 20px 20px;
        background: linear-gradient(rgb(245, 232, 194),#e2c3c3);
        font-family:Georgia, 'Times New Roman', Times, serif;
        font-size:17px;
        border-radius:20px;
        text-align: left;
    }
.st-emotion-cache-155jwzh{
        background: #00246B;
        border-radius:10px 0px 0px 10px;
        font-weight:900;
}
.st-emotion-cache-1ix68xf,.st-emotion-cache-1bf0olv {
        color:#CADCFC;
}
.st-emotion-cache-1up3yna,.st-emotion-cache-4rsbii,.st-emotion-cache-wyoiad  {
        background: #CADCFC;
}
#welcome-to-home-page,#upload-your-file-here,.st-emotion-cache-15okssx,.st-emotion-cache-15okssx {
        color:#00246B;
}
.st-emotion-cache-vl2mil,.st-emotion-cache-1oc4c1q{
        color : black;
}
.st-emotion-cache-6urfhe p{
        color:white;
}
</style>
"""
st.html("""
<style>
div[class*='st-key-add_button'] button{
        position:relative;
        left:230px;
        bottom:170px;
}
div[class*='st-key-fill'] button{
        position:relative;
        left:200px;
        bottom:55px;
}
div[class*='st-key-backword'] button{
        position:relative;
        left:400px;
        bottom:110px;
}
div[class*='st-emotion-cache-0'] button{
        background-color: rgb(250, 250, 250);
        border-radius: 20px;
        box-shadow: 0px 0px 15px 3px rgb(151, 243, 175);
}
</style>
        """)
     
st.markdown(htmlview,unsafe_allow_html=True)
with st.sidebar:
        st.write("Data process📈")

menu=st.sidebar.radio("Options",["Home","Data preview","Data Cleaning","Chart","Analysis","Predict","About"])
if menu=="Home":
        st.title("Welcome to home page.")
        st.header("Upload your file here.")
        file=st.file_uploader("Please upload your file...",type=["xlsx","csv","json"])
        st.markdown("<br><br>",unsafe_allow_html=True)
        
        if file is not None:
                name=file.name
                if name.endswith(".xlsx"):
                        df=pd.read_excel(file)
                if name.endswith(".csv"):
                        df=pd.read_csv(file)
                if name.endswith(".json"):
                        df=pd.read_json(file)
                st.session_state['home']=df
        if 'home' in st.session_state:
                df=st.session_state['home']
                c=df.columns
                a=[]
                for i in c:
                        a.append(df[i].duplicated().sum())
                b=sum(a)
                col=st.columns(4)
                col[0].metric("Rows",f"{df.shape[0]}")
                col[1].metric("Columns",f"{df.shape[1]}")
                col[2].metric("Null value",f"{df.isnull().sum().sum()}")
                col[3].metric("Duplicate value",b)
                st.markdown("<br>",unsafe_allow_html=True)
                st.text("Data frame")
                st.dataframe(df)

elif menu=="Data preview":
        if 'home' not in st.session_state:
                st.warning("Please upload file.")
                st.stop()
        df=st.session_state['home']
        t1,t2,t3,t4=st.tabs(["Dataframe","Data-type","Statistics","Column info"])
        with t1:
                n=st.slider("Rows",5,min(df.shape[0],df.shape[0]),df.shape[0])
                data=st.segmented_control("Select",["Top","Bottom","Random"])
                if data=="Top":
                        st.dataframe(df.head(n))
                elif data=="Bottom":
                        st.dataframe(df.tail(n))
                elif data=="Random":
                        st.dataframe(df.sample(n=n))
        with t2:
                columns=df.columns
                a=[]
                for i in columns:
                        a.append(df[i].duplicated().sum())
                st.dataframe({
                        'datatype': df.dtypes,
                        'Null values':df.isnull().sum(),
                        'Duplicate values': a
                })
        with t3:
                st.dataframe(df.describe())
        with t4:
                col_name=st.selectbox("Column name",(df.columns))
                if col_name:
                        st.markdown(f"""<div class="d1">
        <b>Column name :</b> {col_name} <br>
        <b>data type :</b> {df[col_name].dtypes} <br>
        <b>Non-null : </b> {df[col_name].notnull().sum()} <br>
        <b>Null-value : </b> {df[col_name].isnull().sum()}<br>
        <b>Unique value : </b> {df[col_name].nunique()} <br>
        <b>Duplicates : </b> {df[col_name].duplicated().sum()}<br>
        </div>""",unsafe_allow_html=True)
                        
                        
elif menu=="Data Cleaning":
        if 'home' not in st.session_state:
                st.warning("Please upload file.")
                st.stop()
        df=st.session_state['home']
        t1,t2,t3,t4=st.tabs(["Handle data","Change Data-Type","Manage Duplicate","Add column"])
        with t1:
                data=[]
                for i in df.columns:
                        if df[i].isnull().sum() != 0:
                                data.append(i) 
                box=st.selectbox("Select column",data)
                if st.button("Remove")and box:
                        df=df.dropna(subset=box)
                        st.session_state['home']=df
                        st.success("Null data remove successfully.")
                elif st.button("Forward fill",key="fill")and box:
                        df=df.ffill()
                        st.session_state['home']=df
                        st.success("Forward fill successfully.")
                elif st.button("Backword fill",key="backword")and box:
                        df=df.bfill()
                        st.session_state['home']=df
                        st.success("Backword fill successfully.")
                else:
                        st.warning("Please select column.")
        with t2:
                try:
                        values=st.selectbox("Columns",df.select_dtypes(["int","float"]).columns)
                        st.markdown(f"""
                                    <div style='width:250px; border:2px dashed black; background:#f3fac4; padding:20px;border-radius:20px;color:#00246B'>
                                    <b> Current column type : </b> {df[values].dtypes}
                                    </div>""",unsafe_allow_html=True)
                        st.markdown("<br>",unsafe_allow_html=True)
                        data=st.selectbox("Data-type",["int8","int16","int32","float16","float32"])
                        if st.button("Apply") and data:
                                df[values]=df[values].astype(data)
                                st.success("Done.")
                except:
                        st.write("No columns")
        with t3:
                data=[]
                for j in df.columns:
                        if df[j].duplicated().sum()!=0:
                                data.append(j)
                box11=st.selectbox("Select",data)        
                if st.button("Remove Duplicate") and box11:
                        df=df.drop_duplicates(subset=box11)
                        st.session_state['home']=df
                        st.success("Remove duplicates succcessfully.")
        with t4:
                d=st.segmented_control("Columns Operations",["➕Add Columns","Operation","🖋️Rename","🗑️Drop"],width=500) 
                if d=="➕Add Columns":
                        name=st.text_input("Enter new column name : ")
                        value=st.selectbox("Add",["Number","Text"])
                        if value=="Number" and name:
                                v1=st.number_input("Enter the value:")
                                df[name]=v1
                        elif value=="Text":
                                v2=st.text_input("Enter your text value : ",color="white")
                                df[name]=v2
                        if name and value:
                                st.button("ADD")
                                st.session_state['home']=df
                        
                if d=="Operation":
                        name=st.text_input("Enter the column name ...")
                        st.markdown("<br>",unsafe_allow_html=True)
                        value=st.multiselect("Columns",df.select_dtypes(["int","float"]).columns)
                        operator=st.selectbox("Operator",["Add","Subtraction","Multiply","Divide"])
                        if name and st.button("Add column"):
                                df[name]=0
                                if operator=="Add":
                                        for i in value:
                                                df[name]+=df[i]   
                                elif operator=="Divide":
                                        a=1
                                        for i in value:
                                                if a == 1:
                                                        df[name]=df[i]
                                                        a=2
                                                else:
                                                        df[name]/=df[i]
                                elif operator=="Multiply":
                                        for i in value:
                                                df[name]*=df[i]
                                elif operator=="Subtraction":
                                        for i in value:
                                                df[name]-=df[i]
                                st.session_state['home']=df
                                st.success("Column added succssfully.")
                elif d=="🖋️Rename":
                        df=st.session_state['home']
                        c1=df.columns
                        c2=st.selectbox("select",(c1))
                        new=st.text_input("Enter rename column name : ")
                        if st.button("Add"):
                                df.rename(columns={c2:new},inplace=True)
                                st.session_state['home']=df
                                st.success("Column name changed succssfully.")
                elif d=="🗑️Drop":
                        df=st.session_state['home']
                        v1=df.columns
                        v2=st.selectbox("select column",(v1))
                        if st.button("Drop"):
                                del df[v2]
                                st.session_state['home']=df
                                st.success("Column drop succssfully.")
elif menu=="Chart":
        if 'home' not in st.session_state:
                st.warning("please upload file.")
                st.stop()
        df=st.session_state['home']
        num_row=df.select_dtypes(["int","float"]).columns
        select_row=st.selectbox("Columns",num_row)
        chart=st.selectbox("Charts",["Line","Histogram","Bar","Pie chart","Area","Boxplot","Bubble chart","Heat-map"])
        if chart == "Line":
                fig=px.line(df[select_row],markers="o",labels="Line plot")
                st.plotly_chart(fig)
        elif chart == "Histogram":
                fig=px.histogram(df[select_row])
                st.plotly_chart(fig)
        elif chart == "Bar":
                fig=px.bar(df[select_row])
                st.plotly_chart(fig)
        elif chart=="Pie chart":
                fig,ax=plt.subplots()
                ax.pie(df[select_row])
                st.pyplot(fig)
        elif chart == "Area":
                fig=px.area(df[select_row])
                st.plotly_chart(fig)
        elif chart == "Boxplot":
                fig,ax=plt.subplots()
                ax.boxplot(df[select_row])
                st.pyplot(fig)
        elif chart == "Bubble chart":
                fig=px.scatter(df[select_row])
                st.plotly_chart(fig)
        elif chart == "Heat-map":
                fig=px.density_heatmap(df[select_row])
                st.plotly_chart(fig)
        elif chart == "Scatter plot":
                fig=px.scatter(df[select_row])
                st.plotly_chart(fig)
        else:
                st.warning("Please upload file.")
                st.stop()
                
elif menu=="Analysis":
        if 'home' not in st.session_state:
                st.warning("please upload file.")
                st.stop()
        df=st.session_state['home']
        a1,a2=st.tabs(["Download","Group"])
        with a1:
                c1=df.columns
                select=st.multiselect("Values",(c1))
                if select:
                                st.dataframe(df[select])
                                df=df[select]
                download_data=st.segmented_control("Select Download File",["CSV","EXCEL","JSON"])
                
                if download_data == "CSV":
                                file=df.to_csv(index=False).encode("utf-8")
                                if st.download_button(label="Download CSV",data=file,file_name="new_data.csv",mime="text/csv"):
                                                st.success("Downloaded successfully.")
                elif download_data=="EXCEL":
                                buffer=io.BytesIO()
                                with pd.ExcelWriter(buffer,engine="openpyxl") as file:
                                                df.to_excel(file,index=False,sheet_name="sheet1")
                                value=buffer.getvalue()
                                if st.download_button(label="Download EXCEL",data=value,file_name="new_excel.xlsx",mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"):
                                                st.success("Downloaded successfully.")
                elif download_data=="JSON":
                                file=df.to_json(index=False).encode("utf-8")
                                if st.download_button(label="Download JSON",data=file,file_name="new_json.json",mime="appliction/json"):
                                                st.success("Downloaded Successfully ")
        with a2:
                g1=df.columns
                s1=st.selectbox("Columns",g1)
                s2=st.multiselect("Groupby columns",g1)
                g=st.slider("Group values",5,min(df.shape[0],df.shape[0]),df.shape[0])
                if st.button("Apply") and s2:
                        g2=df.groupby(s1)[s2]
                        x=0
                        for i in g2:
                                if x <= g:
                                        st.write(i)
                                        x=x+1
                        # st.write(g2)
                     