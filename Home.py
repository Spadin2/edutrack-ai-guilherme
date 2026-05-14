import streamlit as st

# Configuração da Página (Título na aba do navegador)
st.set_page_config(page_title="Edutrack AI", page_icon= "🎓")

#Título Principal
st.title(" 🎓 EduTrack AI")

#SideBar
st.sidebar.header("Menu")
menu_option = st.sidebar.radio("Navegar", ["Dashboard", "Disciplinas", "Tarefas"])

#Conteúdo Dinâmico
if menu_option == "Dashboard":
    st.write("Bem-vindo ao seu assistente Acadêmico!")
    st.info("Conecte ao Xano para ver seus dados reais")
    col1, col2 = st.columns(2)
    col1.metric("Disciplinas Ativas","0")
    col2.metric("Tarefas Pendentes","0")
    
elif menu_option == "Disciplinas":
    st.subheader("Minhas Disciplinas")
    st.write("Aqui listaremos as máterias cadastradas no backend.")

elif menu_option == "Tarefas":
    st.subheader("Gerenciamento de Tarefas")
    st.checkbox("Estudar Streamlit")