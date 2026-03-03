"""
Módulo: Sobre o App
Explicações sobre segmentação, fontes de dados, metodologia e estrutura.
"""

import streamlit as st
from ui_components import render_module_header


def render():
    render_module_header(
        icon="ℹ️",
        title="Sobre o App",
        subtitle="Fontes de dados, metodologia, segmentação e referências",
    )

    # ─────────────────────────────────────────
    # CUSTOM CSS
    # ─────────────────────────────────────────
    st.markdown("""
    <style>
    .sobre-section {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(34, 211, 238, 0.12);
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 20px;
    }
    .sobre-section h3 {
        color: #22d3ee;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        margin: 0 0 14px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(34, 211, 238, 0.15);
    }
    .sobre-section p, .sobre-section li {
        color: #cbd5e1;
        font-size: 0.92rem;
        line-height: 1.7;
    }
    .sobre-section ul {
        padding-left: 20px;
        margin: 8px 0;
    }
    .sobre-section li {
        margin-bottom: 6px;
    }
    .seg-card {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(34, 211, 238, 0.10);
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .seg-badge {
        display: inline-block;
        font-family: 'Space Mono', monospace;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 6px;
        margin-right: 10px;
    }
    .seg-badge-s1 { background: #0891b2; color: #fff; }
    .seg-badge-s2 { background: #059669; color: #fff; }
    .seg-badge-s3 { background: #d97706; color: #fff; }
    .seg-badge-s4 { background: #7c3aed; color: #fff; }
    .seg-badge-n1 { background: #e11d48; color: #fff; }
    .seg-badge-n2 { background: #f97316; color: #fff; }
    .seg-badge-n4 { background: #38bdf8; color: #0a0f1a; }
    .seg-desc {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: 6px;
        line-height: 1.6;
    }
    .nota-box {
        background: rgba(34, 211, 238, 0.06);
        border-left: 3px solid #22d3ee;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 12px 0;
        color: #94a3b8;
        font-size: 0.88rem;
        line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SEÇÃO 1: FONTE DE DADOS
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sobre-section">
        <h3>📡 Fonte de Dados</h3>
        <p>
            Os dados utilizados neste aplicativo são obtidos diretamente do
            <strong>Portal de Dados Abertos do Banco Central do Brasil</strong>
            por meio de duas APIs:
        </p>
        <ul>
            <li><strong>IF.data</strong> — dados contábeis das instituições financeiras
                (balanço patrimonial, resultado, carteira de crédito, dados regionais).
                Esses dados são <strong>trimestrais</strong>, publicados com referência
                aos meses de março, junho, setembro e dezembro de cada ano.</li>
            <li><strong>TaxaJuros</strong> — taxas de juros praticadas pelas
                instituições financeiras em diversas modalidades de crédito.
                Esses dados possuem frequência <strong>diária</strong> (maioria das modalidades)
                ou <strong>mensal</strong> (financiamento imobiliário).</li>
        </ul>
        <div class="nota-box">
            <strong>Periodicidade:</strong> Os dados do IF.data refletem a posição contábil
            do último dia de cada trimestre. Por exemplo, dados de "Set/2025" refletem
            a posição em 30/09/2025. A publicação ocorre com defasagem de aproximadamente
            2 a 3 meses após o fechamento do trimestre.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SEÇÃO 2: SEGMENTAÇÃO
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sobre-section">
        <h3>🏛️ Segmentação das Instituições Financeiras</h3>
        <p>
            As instituições são classificadas pelo Banco Central em dois esquemas
            complementares, conforme a <strong>Resolução nº 4.553/2017</strong>:
        </p>
    </div>
    """, unsafe_allow_html=True)

    # SR Segments
    st.markdown("#### Segmentos SR (Resolução nº 4.553/2017)")

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-s1">S1</span>
        <strong style="color:#e2e8f0;">Segmento 1</strong>
        <div class="seg-desc">
            Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio
            e caixas econômicas que (i) tenham porte (Exposição / Produto Interno Bruto)
            superior a 10%; ou (ii) exerçam atividade internacional relevante
            (ativos no exterior superiores a US$ 10 bilhões).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-s2">S2</span>
        <strong style="color:#e2e8f0;">Segmento 2</strong>
        <div class="seg-desc">
            (i) Bancos múltiplos, bancos comerciais, bancos de investimento, bancos de câmbio
            e caixas econômicas de porte inferior a 10% e igual ou superior a 1%; e
            (ii) demais instituições autorizadas a funcionar pelo Banco Central do Brasil
            de porte igual ou superior a 1% do PIB.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-s3">S3</span>
        <strong style="color:#e2e8f0;">Segmento 3</strong>
        <div class="seg-desc">
            Instituições de porte inferior a 1% e igual ou superior a 0,1%.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-s4">S4</span>
        <strong style="color:#e2e8f0;">Segmento 4</strong>
        <div class="seg-desc">
            Instituições de porte inferior a 0,1%.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # TCB Segments
    st.markdown("#### Categorias TCB (Não-bancários)")

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-n1">N1</span>
        <strong style="color:#e2e8f0;">Não bancário de Crédito</strong>
        <div class="seg-desc">
            Instituições não bancárias que operam predominantemente com crédito
            (financeiras, SCDs, SEPs etc.).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-n2">N2</span>
        <strong style="color:#e2e8f0;">Não bancário do Mercado de Capitais</strong>
        <div class="seg-desc">
            Instituições não bancárias que operam predominantemente no mercado de capitais
            (corretoras, distribuidoras etc.).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="seg-card">
        <span class="seg-badge seg-badge-n4">N4</span>
        <strong style="color:#e2e8f0;">Instituições de Pagamento</strong>
        <div class="seg-desc">
            Instituições de pagamento autorizadas pelo Banco Central
            (emissores de moeda eletrônica, credenciadoras etc.).
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nota-box">
        <strong>Filtro utilizado:</strong> O aplicativo exibe instituições com visão
        <strong>PRUDENCIAL</strong> (consolidada), aplicando filtros de materialidade:
        Ativo Total ≥ R$ 100 milhões e Patrimônio Líquido ≥ R$ 20 milhões.
        A seleção de segmentos padrão é S1 e S2, mas pode ser alterada em cada módulo.
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # SEÇÃO 3: METODOLOGIA
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sobre-section">
        <h3>📐 Metodologia e Notas</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Anualização do Resultado (Módulo 2):**

    As variáveis de resultado (receitas, despesas, lucro) são apresentadas
    na forma **anualizada**. Para isso, somam-se os valores
    dos 4 últimos trimestres disponíveis. Por exemplo, se o trimestre
    mais recente é Set/2025, o resultado anualizado corresponde à soma
    de Dez/2024 + Mar/2025 + Jun/2025 + Set/2025.
    Essa abordagem permite comparar o desempenho de instituições em
    base anual, independentemente de sazonalidades trimestrais.

    **Valores monetários:**

    Todos os valores do IF.data são expressos em **Reais (R$)**,
    na unidade original da API (valores inteiros, sem divisão por mil).
    A formatação de exibição converte automaticamente para milhões (mi)
    ou bilhões (bi) conforme a magnitude.

    **Índices Financeiros (Módulo 7):**

    Os índices são calculados a partir da combinação de variáveis do balanço
    e do resultado. O Índice de Basileia é reportado diretamente pela API.
    Os demais (ROE, ROA, Eficiência, Inadimplência etc.) são derivados
    dos dados contábeis disponíveis.

    **Taxas de Juros (Módulo 5):**

    As taxas são reportadas pelas próprias instituições financeiras ao
    Banco Central, em base diária ou mensal conforme a modalidade.
    As taxas são expressas em **% ao ano**.
    Os rankings consideram apenas a data mais recente disponível.

    **Cartograma (Módulo 8):**

    O cartograma utiliza círculos proporcionais (Dorling) posicionados
    nos centróides aproximados de cada região brasileira.
    A área de cada círculo é proporcional ao volume total de crédito
    na região correspondente.
    """)

    # ─────────────────────────────────────────
    # SEÇÃO 4: PERGUNTAS FREQUENTES
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sobre-section">
        <h3>❓ Perguntas Frequentes</h3>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    **Por que algumas instituições não aparecem?**

    O aplicativo aplica filtros de materialidade (Ativo Total ≥ R$ 100 mi,
    PL ≥ R$ 20 mi) e exibe apenas instituições com visão PRUDENCIAL.
    Instituições muito pequenas ou sem dados para o trimestre selecionado
    não serão exibidas.

    **Os dados estão desatualizados?**

    Os dados do IF.data são publicados com defasagem de 2-3 meses.
    O aplicativo busca automaticamente o trimestre mais recente disponível.
    Dados de taxas de juros são mais atuais (diários ou mensais).

    **O que significa "visão PRUDENCIAL"?**

    É a visão consolidada das instituições, agrupando todas as
    entidades de um mesmo conglomerado financeiro. Essa é a forma
    mais adequada de comparar o tamanho e desempenho dos bancos,
    pois evita a dupla contagem entre subsidiárias.

    **Posso baixar os dados?**

    Sim. O Módulo 5 (Taxas de Juros) possui uma aba de download.
    Os demais módulos exibem tabelas interativas que podem ser
    copiadas. Todos os dados são públicos e acessíveis via
    [dadosabertos.bcb.gov.br](https://dadosabertos.bcb.gov.br/).
    """)

    # ─────────────────────────────────────────
    # FOOTER
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="footer">
        Dados:
        <a href="https://dadosabertos.bcb.gov.br/" target="_blank">dadosabertos.bcb.gov.br</a>
        · IF.Data API · TaxaJuros API · python-bcb
    </div>
    """, unsafe_allow_html=True)
