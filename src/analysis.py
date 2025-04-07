import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Ruta a la carpeta de imágenes
images_path = Path(__file__).resolve().parent.parent / "images"
images_path.mkdir(parents=True, exist_ok=True)

def total_goals(df):
    total = df['Goals'].sum()
    print(f"⚽ Total de goles de Messi en la carrera: {total}")
    return total

def goals_by_year(df, save=False):
    df["Year"] = df["Date"].dt.year
    goles_por_año = df.groupby("Year")["Goals"].sum()
    print("\n📈 Goles por año:\n", goles_por_año)

    ax = goles_por_año.plot(kind="bar", title="Goles por Año de Leo Messi")
    plt.ylabel("Goles")
    plt.xlabel("Año")
    plt.tight_layout()
    if save:
        plt.savefig(images_path / "goles_por_año.png")
        print("🖼️ Guardado: goles_por_año.png")
    plt.show()

def goals_by_season(df, save=False):
    goles_por_temporada = df.groupby("Season")["Goals"].sum().sort_index()
    print("\n📅 Goles por temporada:\n", goles_por_temporada)

    goles_por_temporada.plot(kind='bar', title='Total de Goles por Temporada', xlabel='Temporada', ylabel='Goles')
    plt.tight_layout()
    if save:
        plt.savefig(images_path / "goles_por_temporada.png")
        print("🖼️ Guardado: goles_por_temporada.png")
    plt.show()

def goals_by_competition(df, save=False):
    goles_por_competicion = df.groupby('Competition')['Goals'].sum().sort_values(ascending=False)
    print("\n🏆 Goles por competición:\n", goles_por_competicion)

    goles_por_competicion.plot(kind='bar', title='Goles por Competición', xlabel='Competición', ylabel='Goles')
    plt.tight_layout()
    if save:
        plt.savefig(images_path / "goles_por_competicion.png")
        print("🖼️ Guardado: goles_por_competicion.png")
    plt.show()

def goals_per_minute(df):
    total_goals_ = df['Goals'].sum()
    total_minutes = pd.to_numeric(df['Minutes'], errors='coerce').sum()
    if total_goals_ > 0:
        promedio = total_minutes / total_goals_
        print(f"⏱️ Gol cada {promedio:.2f} minutos.")
    else:
        print("⏱️ No hay goles suficientes para calcular promedio.")

def average_goals_per_match(df):
    promedio = df['Goals'].mean()
    print(f"📊 Promedio de goles por partido: {promedio:.2f}")

def assists_total_and_by_season(df, save=False):
    total = df['Assists'].sum()
    print(f"🎯 Total de asistencias: {total}")

    asistencias_por_temporada = df.groupby('Season')['Assists'].sum().sort_values(ascending=False)
    print("\n📅 Asistencias por temporada:\n", asistencias_por_temporada)

    asistencias_por_temporada.plot(kind='bar', title='Total de Asistencias por Temporada', xlabel='Temporada', ylabel='Asistencias')
    plt.tight_layout()
    if save:
        plt.savefig(images_path / "asistencias_por_temporada.png")
        print("🖼️ Guardado: asistencias_por_temporada.png")
    plt.show()

def goals_by_month(df, save=False):
    df['Month'] = df['Date'].dt.month
    goles_por_mes = df.groupby('Month')['Goals'].sum()

    goles_por_mes.plot(kind='bar', title='Goles por Mes', xlabel='Mes', ylabel='Goles')
    plt.tight_layout()
    if save:
        plt.savefig(images_path / "goles_por_mes.png")
        print("🖼️ Guardado: goles_por_mes.png")
    plt.show()

def run_all_analyses(df, save=False):
    print("📊 Análisis completo de la carrera de Messi:\n")
    total_goals(df)
    goals_by_year(df, save=save)
    goals_by_season(df, save=save)
    goals_by_competition(df, save=save)
    goals_per_minute(df)
    average_goals_per_match(df)
    assists_total_and_by_season(df, save=save)
    goals_by_month(df, save=save)

