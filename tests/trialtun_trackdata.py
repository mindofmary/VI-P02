import csv
import ast
from collections import defaultdict
from pathlib import Path


CSV_PATH = Path(__file__).parent.parent / "datasets" / "track_data_final.csv"


def organizar_por_decada(csv_path):
    """Lê o CSV e devolve as estatísticas de duração agrupadas por década."""
    musicas_por_decada = defaultdict(list)

    with csv_path.open(encoding="utf-8-sig", newline="") as ficheiro:
        leitor = csv.DictReader(ficheiro)

        for linha in leitor:
            ano = int(linha["album_release_date"][:4])
            duracao = int(linha["track_duration_ms"]) / 60000
            grupo = str(ano) if 2000 <= ano <= 2025 else f"{ano // 10 * 10}s"
            generos_texto = (linha["artist_genres"] or "").strip()
            generos = ast.literal_eval(generos_texto) if generos_texto else []

            musicas_por_decada[grupo].append(
                {
                    "nome": linha["track_name"],
                    "duracao": duracao,
                    "popularidade": int(linha["track_popularity"]),
                    "generos": [
                        genero.strip()
                        for genero in generos
                        if genero.strip() and genero.strip().upper() != "N/A"
                    ],
                }
            )

    return musicas_por_decada


def mostrar_estatisticas(musicas_por_decada):
    for grupo in sorted(musicas_por_decada):
        musicas = musicas_por_decada[grupo]
        mais_curta = min(musicas, key=lambda musica: musica["duracao"])
        mais_longa = max(musicas, key=lambda musica: musica["duracao"])
        top_20 = sorted(
            musicas,
            key=lambda musica: musica["popularidade"],
            reverse=True,
        )[:20]
        popularidade_por_genero = defaultdict(list)
        for musica in musicas:
            for genero in musica["generos"]:
                popularidade_por_genero[genero].append(musica["popularidade"])

        top_generos = sorted(
            popularidade_por_genero.items(),
            key=lambda item: sum(item[1]) / len(item[1]),
            reverse=True,
        )[:10]
        media = sum(musica["duracao"] for musica in musicas) / len(musicas)

        nome_grupo = grupo if grupo.isdigit() else f"década de {grupo}"
        print(f"\n{nome_grupo}")
        print(f"  Média de duração: {media:.2f} minutos")
        print(
            f"  Música mais curta: {mais_curta['nome']} "
            f"({mais_curta['duracao']:.2f} minutos)"
        )
        print(
            f"  Música mais longa: {mais_longa['nome']} "
            f"({mais_longa['duracao']:.2f} minutos)"
        )
        print("  Top 20 músicas mais populares:")
        for posicao, musica in enumerate(top_20, start=1):
            print(
                f"    {posicao}. {musica['nome']} "
                f"(popularidade: {musica['popularidade']}, "
                f"{musica['duracao']:.2f} minutos)"
            )
        print("  Géneros mais populares (por popularidade média):")
        for posicao, (genero, popularidades) in enumerate(top_generos, start=1):
            media_popularidade = sum(popularidades) / len(popularidades)
            print(
                f"    {posicao}. {genero} "
                f"(média: {media_popularidade:.2f}, "
                f"{len(popularidades)} músicas)"
            )


if __name__ == "__main__":
    estatisticas = organizar_por_decada(CSV_PATH)
    mostrar_estatisticas(estatisticas)