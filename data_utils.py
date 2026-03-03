"""
Laboratório de Dados Públicos - BCB
Funções de coleta de dados, cache e processamento.

Architecture: Parquet-first, API-fallback.
  1. Try to read from data/*.parquet (pre-fetched by GitHub Action)
  2. If not found, fetch from API live (slower, but works anywhere)
"""

import pandas as pd
import numpy as np
import streamlit as st
from datetime import date
from pathlib import Path
from config import (
    TCB_OVERRIDE, VALID_SR, MIN_ATIVO_TOTAL, MIN_PL,
    RELATORIO_RESUMO, get_short_name,
)

DATA_DIR = Path(__file__).resolve().parent / "data"


def _parquet_path(name: str) -> Path:
    return DATA_DIR / name


def _has_parquet(name: str) -> bool:
    return _parquet_path(name).is_file()


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_valores(anomes: int, tipo: int, relatorio: int) -> pd.DataFrame:
    """Fetch IfDataValores. Tries local Parquet first, then API."""
    fname = f"valores_{anomes}_t{tipo}_r{relatorio}.parquet"
    if _has_parquet(fname):
        try:
            df = pd.read_parquet(_parquet_path(fname))
            if not df.empty:
                return df
        except Exception:
            pass
    from bcb.odata import IFDATA
    ifdata = IFDATA()
    ep = ifdata.get_endpoint("IfDataValores")
    try:
        df = ep.get(AnoMes=anomes, TipoInstituicao=tipo, Relatorio=relatorio)
        return df if df is not None else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_cadastro(anomes: int) -> pd.DataFrame:
    """Fetch IfDataCadastro. Tries local Parquet first, then API."""
    fname = f"cadastro_{anomes}.parquet"
    if _has_parquet(fname):
        try:
            df = pd.read_parquet(_parquet_path(fname))
            if not df.empty:
                return df
        except Exception:
            pass
    from bcb.odata import IFDATA
    ifdata = IFDATA()
    ep = ifdata.get_endpoint("IfDataCadastro")
    try:
        df = ep.get(AnoMes=anomes)
        return df if df is not None else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=86400, show_spinner=False)
def find_latest_quarter(tipo: int = 1, relatorio: int = 1, tipos: list = None) -> int:
    """Find latest quarter. Tries local marker first, then probes API."""
    marker = DATA_DIR / "latest_quarter.txt"
    if marker.is_file():
        try:
            val = int(marker.read_text().strip())
            if val > 200000:
                return val
        except (ValueError, OSError):
            pass
    from bcb.odata import IFDATA
    ifdata = IFDATA()
    ep = ifdata.get_endpoint("IfDataValores")
    today = date.today()
    y, m = today.year, today.month
    candidates = []
    for _ in range(8):
        q_month = ((m - 1) // 3) * 3 + 3
        candidates.append(y * 100 + q_month)
        m -= 3
        if m <= 0:
            m += 12
            y -= 1
    tipos_to_try = tipos if tipos else [tipo]
    for anomes in candidates:
        for t in tipos_to_try:
            try:
                df = ep.get(AnoMes=anomes, TipoInstituicao=t, Relatorio=relatorio)
                if df is not None and not df.empty:
                    return anomes
            except Exception:
                continue
    return candidates[-1]


def get_data_source_info() -> dict:
    """Return info about current data source for display in UI."""
    import json
    manifest_path = DATA_DIR / "manifest.json"
    if manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text())
            return {
                "source": "cache",
                "generated_at": manifest.get("generated_at", ""),
                "n_files": len(manifest.get("files", [])),
                "latest_quarter": manifest.get("latest_quarter", 0),
            }
        except Exception:
            pass
    return {"source": "api", "generated_at": "", "n_files": 0, "latest_quarter": 0}


def classify_segment(row) -> str:
    tcb = str(row.get("Tcb", "") or "").strip().upper()
    if tcb in TCB_OVERRIDE:
        return tcb
    sr = str(row.get("Sr", "") or "").strip().upper()
    if sr in VALID_SR:
        return sr
    return "Outros"


def build_institution_table(anomes: int) -> pd.DataFrame:
    cad = fetch_cadastro(anomes)
    if cad.empty:
        return pd.DataFrame()
    cad["Segmento_Calculado"] = cad.apply(classify_segment, axis=1)
    cad = cad[cad["Segmento_Calculado"] != "Outros"].copy()
    cad = cad[cad["NomeInstituicao"].str.contains("PRUDENCIAL", case=False, na=False)].copy()
    if cad.empty:
        return pd.DataFrame()
    cad["NomeDisplay"] = (
        cad["NomeInstituicao"]
        .str.replace(r"\s*[-\u2013]\s*PRUDENCIAL", "", regex=True)
        .str.strip()
    )
    cad["NomeReduzido"] = cad["NomeDisplay"].apply(get_short_name)
    cad = cad.drop_duplicates(subset=["CodInst"])
    return cad[["CodInst", "NomeInstituicao", "NomeDisplay", "NomeReduzido", "Segmento_Calculado"]].copy()


def extract_variable(df, conta, institutions):
    if df.empty or institutions.empty:
        return pd.DataFrame()
    valid_codes = set(institutions["CodInst"].tolist())
    if isinstance(conta, list):
        records = {}
        for _, row in df.iterrows():
            cod = row.get("CodInst")
            if cod not in valid_codes:
                continue
            var_name = str(row.get("NomeColuna", ""))
            if var_name in conta:
                val = pd.to_numeric(row.get("Saldo"), errors="coerce")
                if pd.notna(val):
                    records[cod] = records.get(cod, 0) + val
        sub = pd.DataFrame([{"CodInst": cod, "Saldo": val} for cod, val in records.items()])
    else:
        mask = (df["NomeColuna"] == conta) & (df["CodInst"].isin(valid_codes))
        sub = df[mask][["CodInst", "Saldo"]].copy()
        sub["Saldo"] = pd.to_numeric(sub["Saldo"], errors="coerce")
    if sub.empty:
        return pd.DataFrame()
    sub["Saldo"] = pd.to_numeric(sub["Saldo"], errors="coerce")
    sub = sub.dropna(subset=["Saldo"])
    sub = sub[sub["Saldo"].abs() > 0].copy()
    sub = sub[~sub["Saldo"].isin([float("inf"), float("-inf")])].copy()
    return sub.merge(institutions, on="CodInst", how="inner")


def extract_variable_annualized(anomes_list, relatorio, conta, institutions):
    frames = []
    for anomes in anomes_list:
        df = fetch_valores(anomes, 1, relatorio)
        if not df.empty:
            extracted = extract_variable(df, conta, institutions)
            if not extracted.empty:
                frames.append(extracted[["CodInst", "Saldo"]])
    if not frames:
        return pd.DataFrame()
    combined = pd.concat(frames, ignore_index=True)
    summed = combined.groupby("CodInst")["Saldo"].sum().reset_index()
    return summed.merge(institutions, on="CodInst", how="inner")


def apply_materiality_filter(data, resumo_df, institutions):
    if data.empty:
        return data
    valid_codes = set(institutions["CodInst"].tolist())
    ativo_mask = (resumo_df["NomeColuna"] == "Ativo Total") & (resumo_df["CodInst"].isin(valid_codes))
    pl_mask = (resumo_df["NomeColuna"] == "Patrim\u00f4nio L\u00edquido") & (resumo_df["CodInst"].isin(valid_codes))
    valid_by_ativo = set()
    valid_by_pl = set()
    if ativo_mask.any():
        ativo = resumo_df[ativo_mask][["CodInst", "Saldo"]].copy()
        ativo["Saldo"] = pd.to_numeric(ativo["Saldo"], errors="coerce").fillna(0)
        valid_by_ativo = set(ativo[ativo["Saldo"] >= MIN_ATIVO_TOTAL]["CodInst"])
    if pl_mask.any():
        pl = resumo_df[pl_mask][["CodInst", "Saldo"]].copy()
        pl["Saldo"] = pd.to_numeric(pl["Saldo"], errors="coerce").fillna(0)
        valid_by_pl = set(pl[pl["Saldo"] >= MIN_PL]["CodInst"])
    if not valid_by_ativo and not valid_by_pl:
        return data[data["Saldo"] != 0].copy()
    valid_insts = valid_by_ativo & valid_by_pl
    return data[(data["CodInst"].isin(valid_insts)) & (data["Saldo"] != 0)].copy()


def get_last_n_quarters(anomes: int, n: int = 4) -> list:
    year = anomes // 100
    month = anomes % 100
    quarters = []
    for _ in range(n):
        quarters.append(year * 100 + month)
        month -= 3
        if month <= 0:
            month += 12
            year -= 1
    return quarters


def format_anomes(anomes: int) -> str:
    year = anomes // 100
    month = anomes % 100
    month_names = {3: "Mar", 6: "Jun", 9: "Set", 12: "Dez"}
    m = month_names.get(month, f"{month:02d}")
    return f"{m}/{year}"


def extract_credit_variable(df, grupo, institutions):
    if df.empty or institutions.empty:
        return pd.DataFrame()
    valid_codes = set(institutions["CodInst"].tolist())
    if "Total da Carteira" in grupo or "Total Exterior" in grupo:
        mask = (df["NomeColuna"] == grupo) & (df["CodInst"].isin(valid_codes))
    else:
        mask = (
            (df["Grupo"] == grupo) &
            (df["NomeColuna"] == "Total") &
            (df["CodInst"].isin(valid_codes))
        )
    sub = df[mask][["CodInst", "Saldo"]].copy()
    sub["Saldo"] = pd.to_numeric(sub["Saldo"], errors="coerce")
    sub = sub.dropna(subset=["Saldo"])
    sub = sub[sub["Saldo"].abs() > 0].copy()
    sub = sub[~sub["Saldo"].isin([float("inf"), float("-inf")])].copy()
    if sub.empty:
        return pd.DataFrame()
    return sub.merge(institutions, on="CodInst", how="inner")


def search_banks(institutions, query):
    if institutions.empty or not query:
        return pd.DataFrame()
    mask = (
        institutions["NomeDisplay"].str.contains(query, case=False, na=False) |
        institutions["NomeReduzido"].str.contains(query, case=False, na=False)
    )
    return institutions[mask]
