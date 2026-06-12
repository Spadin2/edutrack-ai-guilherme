# ------------------------------------------------
# IMPORTAÇÃO DE BIBLIOTECAS
# ------------------------------------------------

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# ------------------------------------------------
# CONFIGURAÇÃO DA API XANO
# ------------------------------------------------

# Substitua pela SUA URL real do grupo de API no Xano
BASE_URL = 'https://x8ki-letl-twmt.n7.xano.io/api:MZDCSXDx'

# ------------------------------------------------
# FUNÇÕES DE CONEXÃO E UTILITÁRIOS
# ------------------------------------------------

def get_headers():
    '''
    Gera o cabeçalho com o JSON Web Token (JWT) para autenticação segura.
    '''
    headers = {'Content-Type': 'application/json'}
    if 'auth_token' in st.session_state:
        headers['Authorization'] = f'Bearer {st.session_state.auth_token}'
    return headers

def api_get(endpoint):
    '''
    Lê dados do Xano (filtra automaticamente pelo usuário no servidor).
    '''
    resposta = requests.get(f'{BASE_URL}/{endpoint}', headers=get_headers())
    return resposta.json() if resposta.status_code == 200 else []

def api_post(endpoint, dados):
    '''
    Cria um novo registro vinculado ao aluno logado.
    '''
    return requests.post(f'{BASE_URL}/{endpoint}', json=dados, headers=get_headers())

def api_patch(endpoint, id, dados):
    '''
    Atualiza um registro existente.
    '''
    return requests.patch(f'{BASE_URL}/{endpoint}/{id}', json=dados, headers=get_headers())

def api_delete(endpoint, id):
    '''
    Remove um registro do banco de dados.
    '''
    return requests.delete(f'{BASE_URL}/{endpoint}/{id}', headers=get_headers())

# ------------------------------------------------
# SISTEMA DE AUTENTICAÇÃO
# ------------------------------------------------

def tela_acesso():
    st.title('Portal Acadêmico Personalizado')
    tab_login, tab_cadastro = st.tabs(['Entrar', 'Criar Minha Conta'])

    with tab_login:
        with st.form('login_form'):
            email = st.text_input('E-mail')
            senha = st.text_input('Senha', type='password')
            if st.form_submit_button('Acessar Meu Painel'):
                res = requests.post(f'{BASE_URL}/auth/login', json={'email': email, 'password': senha})
                if res.status_code == 200:
                    st.session_state.auth_token = res.json().get('authToken')
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error('Credenciais inválidas.')

    with tab_cadastro:
        with st.form('cadastro_form'):
            nome = st.text_input('Nome')
            email_c = st.text_input('E-mail')
            pass_c = st.text_input('Senha', type='password')
            if st.form_submit_button('Cadastrar'):
                res = requests.post(f'{BASE_URL}/auth/signup', json={'name': nome, 'email': email_c, 'password': pass_c})
                if res.status_code == 200:
                    st.success('Conta criada! Agora faça o login.')
                else:
                    st.error('Erro ao cadastrar usuário.')

# ------------------------------------------------
# MÓDULOS CRUD PARA PROFESSORES, DISCIPLINAS
# E TAREFAS
# ------------------------------------------------

# GESTÃO DE PROFESSORES

def modulo_professores():

    st.header('👨‍🏫 Meus Professores')

    # ------------------------------------------------
    # CADASTRO
    # ------------------------------------------------

    with st.expander('➕ Adicionar Professor'):

        nome = st.text_input(
            'Nome do Professor'
        )

        email = st.text_input(
            'E-mail de Contato'
        )

        if st.button('Cadastrar Professor'):

            if nome and email:

                api_post(
                    'professores',
                    {
                        'nome': nome,
                        'email': email
                    }
                )

                st.success(
                    'Professor cadastrado com sucesso!'
                )

                st.rerun()

            else:

                st.warning(
                    'Preencha todos os campos.'
                )

    # ------------------------------------------------
    # LISTA DE PROFESSORES
    # ------------------------------------------------

    dados = api_get('professores')

    if not dados:

        st.info(
            'Nenhum professor cadastrado ainda.'
        )

        return

    df = pd.DataFrame(dados)

    st.subheader(
        '👨‍🏫 Lista de Professores'
    )

    busca = st.text_input(
        '🔍 Pesquisar Professor'
    )

    if busca:

        df = df[
            df['nome']
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    for _, prof in df.iterrows():

        with st.expander(
            f"👨‍🏫 {prof['nome']}"
        ):

            st.write(
                f"📧 E-mail: {prof['email']}"
            )

            st.write(
                f"🆔 ID: {prof['id']}"
            )

    # ------------------------------------------------
    # EDIÇÃO
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '✏️ Editar Professores'
    )

    df_editado = st.data_editor(
        df[['id', 'nome', 'email']],
        use_container_width=True,
        hide_index=True,
        num_rows='dynamic'
    )

    if st.button(
        '💾 Salvar Alterações'
    ):

        for _, row in df_editado.iterrows():

            api_patch(
                'professores',
                row['id'],
                {
                    'nome': row['nome'],
                    'email': row['email']
                }
            )

        st.success(
            'Alterações salvas com sucesso!'
        )

        st.rerun()

    # ------------------------------------------------
    # REMOVER PROFESSOR
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '🗑️ Remover Professor'
    )

    id_remover = st.number_input(
        'ID do Professor',
        min_value=1,
        step=1
    )

    if st.button(
        'Excluir Professor'
    ):

        api_delete(
            'professores',
            id_remover
        )

        st.success(
            'Professor removido com sucesso!'
        )

        st.rerun()

# GESTÃO DE DISCIPLINAS

def modulo_disciplinas():

    st.header('📚 Minhas Disciplinas')

    profs = api_get('professores')

    if not profs:

        st.warning(
            'Cadastre um professor antes de criar disciplinas.'
        )

        return

    # ------------------------------------------------
    # CADASTRO
    # ------------------------------------------------

    with st.expander('➕ Nova Disciplina'):

        nome_d = st.text_input(
            'Nome da Matéria'
        )

        carga_horaria = st.number_input(
            'Carga Horária',
            min_value=1,
            value=60
        )

        frequencia_minima = st.number_input(
            'Frequência Mínima (%)',
            min_value=0.0,
            max_value=100.0,
            value=75.0
        )

        opcoes_p = {
            p['nome']: p['id']
            for p in profs
        }

        p_escolhido = st.selectbox(
            'Professor Responsável',
            options=list(opcoes_p.keys())
        )

        if st.button('Salvar Disciplina'):

            api_post(
                'disciplinas',
                {
                    'nome': nome_d,
                    'prof_id': opcoes_p[p_escolhido],
                    'carga_horaria': carga_horaria,
                    'frequencia_minima': frequencia_minima
                }
            )

            st.success(
                'Disciplina cadastrada!'
            )

            st.rerun()

    # ------------------------------------------------
    # LISTAGEM
    # ------------------------------------------------

    disciplinas = api_get('disciplinas')

    if not disciplinas:

        st.info(
            'Nenhuma disciplina cadastrada.'
        )

        return

    df_d = pd.DataFrame(disciplinas)
    df_p = pd.DataFrame(profs)

    df_view = df_d.merge(
        df_p[['id', 'nome']],
        left_on='prof_id',
        right_on='id',
        suffixes=('', '_prof')
    )

    st.subheader(
        '📚 Lista de Disciplinas'
    )

    busca = st.text_input(
        '🔍 Pesquisar Disciplina'
    )

    if busca:

        df_view = df_view[
            df_view['nome']
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    for _, disc in df_view.iterrows():

        with st.expander(
            f"📖 {disc['nome']}"
        ):

            st.write(
                f"👨‍🏫 Professor: {disc['nome_prof']}"
            )

            st.write(
                f"⏰ Carga Horária: {disc['carga_horaria']} horas"
            )

            st.write(
                f"📊 Frequência Mínima: {disc['frequencia_minima']}%"
            )

            st.write(
                f"🆔 ID: {disc['id']}"
            )

    # ------------------------------------------------
    # EDIÇÃO
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '✏️ Editar Disciplinas'
    )

    df_editado = st.data_editor(
        df_view[
            [
                'id',
                'nome',
                'carga_horaria',
                'frequencia_minima'
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        '💾 Salvar Alterações das Disciplinas'
    ):

        for _, row in df_editado.iterrows():

            api_patch(
                'disciplinas',
                row['id'],
                {
                    'nome': row['nome'],
                    'carga_horaria': row['carga_horaria'],
                    'frequencia_minima': row['frequencia_minima']
                }
            )

        st.success(
            'Alterações salvas com sucesso!'
        )

        st.rerun()

    # ------------------------------------------------
    # REMOVER
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '🗑️ Remover Disciplina'
    )

    id_remover = st.number_input(
        'ID da Disciplina',
        min_value=1,
        step=1
    )

    if st.button(
        'Excluir Disciplina'
    ):

        api_delete(
            'disciplinas',
            id_remover
        )

        st.success(
            'Disciplina removida com sucesso!'
        )

        st.rerun()

# GESTÃO DE TAREFAS ---

def modulo_tarefas():

    st.header('📝 Minhas Tarefas e Notas')

    disciplinas = api_get('disciplinas')

    if not disciplinas:

        st.warning(
            'Cadastre uma disciplina primeiro.'
        )

        return

    # ------------------------------------------------
    # CADASTRO
    # ------------------------------------------------

    with st.expander('➕ Lançar Atividade/Nota'):

        nome_t = st.text_input(
            'Nome da Atividade'
        )

        opcoes_d = {
            d['nome']: d['id']
            for d in disciplinas
        }

        d_escolhida = st.selectbox(
            'Selecione a Disciplina',
            options=list(opcoes_d.keys())
        )

        nota = st.number_input(
            'Nota Obtida',
            min_value=0.0,
            max_value=10.0,
            value=0.0
        )

        if st.button('Registrar Nota'):

            api_post(
                'tarefas',
                {
                    'nome': nome_t,
                    'disc_id': opcoes_d[d_escolhida],
                    'nota': nota
                }
            )

            st.success(
                'Nota registrada com sucesso!'
            )

            st.rerun()

    # ------------------------------------------------
    # LEITURA
    # ------------------------------------------------

    tarefas = api_get('tarefas')

    if not tarefas:

        st.info(
            'Nenhuma atividade cadastrada.'
        )

        return

    df_t = pd.DataFrame(tarefas)
    df_d = pd.DataFrame(disciplinas)

    df_view = df_t.merge(
        df_d[['id', 'nome']],
        left_on='disc_id',
        right_on='id',
        suffixes=('', '_disc')
    )

    # ------------------------------------------------
    # ESTATÍSTICAS
    # ------------------------------------------------

    media = df_t['nota'].mean()

    melhor = df_t['nota'].max()

    pior = df_t['nota'].min()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            '📊 Média Geral',
            f'{media:.2f}'
        )

    with col2:
        st.metric(
            '🏆 Melhor Nota',
            f'{melhor:.2f}'
        )

    with col3:
        st.metric(
            '📉 Menor Nota',
            f'{pior:.2f}'
        )

    # ------------------------------------------------
    # PESQUISA
    # ------------------------------------------------

    st.subheader(
        '📚 Lista de Atividades'
    )

    busca = st.text_input(
        '🔍 Pesquisar Atividade'
    )

    if busca:

        df_view = df_view[
            df_view['nome']
            .str.contains(
                busca,
                case=False,
                na=False
            )
        ]

    # ------------------------------------------------
    # CARDS
    # ------------------------------------------------

    for _, tarefa in df_view.iterrows():

        nota = tarefa['nota']

        if nota >= 7:
            status = "🟢 Aprovado"

        elif nota >= 5:
            status = "🟡 Recuperação"

        else:
            status = "🔴 Reprovado"

        with st.expander(
            f"📝 {tarefa['nome']}"
        ):

            st.write(
                f"📚 Disciplina: {tarefa['nome_disc']}"
            )

            st.write(
                f"📊 Nota: {nota}"
            )

            st.write(
                f"📌 Situação: {status}"
            )

            st.write(
                f"🆔 ID: {tarefa['id']}"
            )

    # ------------------------------------------------
    # EXPORTAR CSV
    # ------------------------------------------------

    st.divider()

    csv = df_view.to_csv(
        index=False
    )

    st.download_button(
        label='📥 Exportar Boletim CSV',
        data=csv,
        file_name='boletim.csv',
        mime='text/csv'
    )

    # ------------------------------------------------
    # EDIÇÃO
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '✏️ Editar Notas'
    )

    df_editado = st.data_editor(
        df_view[
            [
                'id',
                'nome',
                'nota'
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    if st.button(
        '💾 Salvar Alterações das Notas'
    ):

        for _, row in df_editado.iterrows():

            api_patch(
                'tarefas',
                row['id'],
                {
                    'nome': row['nome'],
                    'nota': row['nota']
                }
            )

        st.success(
            'Notas atualizadas!'
        )

        st.rerun()

    # ------------------------------------------------
    # REMOVER
    # ------------------------------------------------

    st.divider()

    st.subheader(
        '🗑️ Remover Atividade'
    )

    id_remover = st.number_input(
        'ID da Atividade',
        min_value=1,
        step=1
    )

    if st.button(
        'Excluir Atividade'
    ):

        api_delete(
            'tarefas',
            id_remover
        )

        st.success(
            'Atividade removida com sucesso!'
        )

        st.rerun()

# --- DASHBOARD ---

def modulo_dashboard():

    st.header('📊 Painel Geral')

    tarefas = api_get('tarefas')
    disciplinas = api_get('disciplinas')
    professores = api_get('professores')

    if not tarefas:

        st.info(
            'Cadastre atividades para visualizar indicadores.'
        )

        return

    df_t = pd.DataFrame(tarefas)

    media = df_t['nota'].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            'Média Geral',
            f'{media:.2f}'
        )

    with col2:
        st.metric(
            'Total de Tarefas',
            len(df_t)
        )

    with col3:
        st.metric(
            'Professores',
            len(professores)
        )

    if media >= 7:
        st.success('✅ Situação: Aprovado')

    elif media >= 5:
        st.warning('⚠️ Situação: Recuperação')

    else:
        st.error('❌ Situação: Reprovado')

    st.divider()

    if disciplinas:

        df_d = pd.DataFrame(disciplinas)

        df_plot = df_t.merge(
            df_d,
            left_on='disc_id',
            right_on='id',
            suffixes=('_t', '_d')
        )

        fig = px.bar(
            df_plot,
            x='nome_t',
            y='nota',
            color='nome_d',
            title='Notas por Disciplina'
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        ranking = (
            df_plot
            .groupby('nome_d')['nota']
            .mean()
            .reset_index()
            .sort_values(
                by='nota',
                ascending=False
            )
        )

        st.subheader(
            '🏆 Ranking de Disciplinas'
        )

        st.dataframe(
            ranking,
            use_container_width=True
        )

def pagina_sobre():

    st.title('EduTrack AI')

    st.markdown("""
    ## Tecnologias

    - Python
    - Streamlit
    - Xano
    - API REST
    - Plotly
    - Pandas

    ## Recursos

    ✅ Login JWT

    ✅ CRUD Professores

    ✅ CRUD Disciplinas

    ✅ CRUD Tarefas

    ✅ Dashboard Acadêmico

    ✅ Exportação CSV

    ## Desenvolvido por

    Guilherme Domingues, Gabrielly Grasso e William Bryan
    """)




# ------------------------------------------
# ESTRUTURA PRINCIPAL DE NAVEGAÇÃO
# ------------------------------------------

st.set_page_config(page_title='EduTrack AI', layout='wide')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    tela_acesso()
else:
    with st.sidebar:
        st.title('EduTrack AI')
        menu = st.radio('Gerenciar:', ['Painel Geral', 'Professores', 'Disciplinas', 'Tarefas/Notas', 'Sobre'])
        st.markdown('---')
        if st.button('Sair'):
            st.session_state.clear()
            st.rerun()

    match menu:
        case 'Painel Geral': modulo_dashboard()
        case 'Professores': modulo_professores()
        case 'Disciplinas': modulo_disciplinas()
        case 'Tarefas/Notas': modulo_tarefas()
        case 'Sobre': pagina_sobre()
        


#--Perfil entrou em conflito e não deixou criar disciplinas
