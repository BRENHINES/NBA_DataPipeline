import flet as ft


def main(page: ft.Page):
    page.title = "NBA Dashboard"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Onglets principaux
    def on_tab_change(e):
        current_tab = e.control.selected_index
        if current_tab == 0:
            content_container.controls = [overview_tab()]
        elif current_tab == 1:
            content_container.controls = [kpis_tab()]
        elif current_tab == 2:
            content_container.controls = [draft_predictions_tab()]
        elif current_tab == 3:
            content_container.controls = [playoff_tab()]
        elif current_tab == 4:
            content_container.controls = [lineup_tab()]
        page.update()

    tabs = ft.Tabs(
        selected_index=0,
        on_change=on_tab_change,
        tabs=[
            ft.Tab(text="Accueil"),
            ft.Tab(text="Statistiques et KPIs"),
            ft.Tab(text="Draft"),
            ft.Tab(text="Playoffs"),
            ft.Tab(text="Lineup"),
        ]
    )

    content_container = ft.Column(expand=True, controls=[])

    # Pages
    def overview_tab():
        return ft.Container(
            alignment=ft.alignment.center,
            padding=ft.Padding(160, 50, 160, 50),
            content=ft.Column([
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_100,
                    clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    content=ft.Image(
                        src="https://i.pinimg.com/736x/90/c1/c1/90c1c12aabaeab3130ebd2026af10ebf.jpg",
                        expand=True,
                        width=float('inf'),
                        height=500,
                        fit=ft.ImageFit.COVER
                    ),
                    border_radius=15,
                    alignment=ft.alignment.center,
                    margin=ft.margin.only(bottom=30)
                ),
                ft.Text("🏀 NBA DATA PIPELINE DASHBOARD", size=36, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Bienvenue sur ce tableau de bord interactif basé sur un projet de pipeline NBA complet.",
                        size=18, text_align=ft.TextAlign.CENTER),
                ft.Text(
                    "Ce projet combine l'orchestration de données, le machine learning, l'analyse statistique et la visualisation avancée pour fournir une plateforme d'analyse de la NBA complète.",
                    size=16),
                ft.Container(height=20),
                ft.Text("Objectifs du projet :", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("- Automatiser l'extraction des données NBA (matchs, joueurs, saisons, statistiques, drafts)."),
                ft.Text("- Nettoyer et enrichir les données avec des KPIs utiles à l’analyse décisionnelle."),
                ft.Text(
                    "- Implémenter des modèles de machine learning : flop draft, gagnant des playoffs, lineup optimal."),
                ft.Text("- Visualiser dynamiquement les données et recommandations via une interface moderne."),
                ft.Container(height=20),
                ft.Text("Technologies utilisées :", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("- Dagster pour l’orchestration du pipeline (assets, jobs, schedules, sensors)."),
                ft.Text("- Polars pour le traitement des données à haute performance."),
                ft.Text("- PostgreSQL pour le stockage relationnel.", size=16),
                ft.Text("- XGBoost, RandomForest pour les modèles de ML prédictifs."),
                ft.Text("- Flet pour une visualisation moderne et dynamique des résultats."),
                ft.Text("- GitHub Actions pour le CI/CD et les tests automatisés."),
                ft.Container(height=20),
                ft.Text("À explorer dans le tableau de bord :", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("• Statistiques & KPIs : performances joueurs par équipe/saison."),
                ft.Text("• Draft : prédiction des flops via ML et analyse des drafts passés."),
                ft.Text("• Playoffs : simulation des gagnants des séries à venir."),
                ft.Text("• Lineup : recommandation des meilleurs alignements par adversaire."),
                ft.Text("• Exploration libre : accès brut aux données filtrables par utilisateur."),
                ft.Container(height=20),
                ft.Text("📅 Dernière mise à jour du projet : Avril 2025", italic=True, size=14,
                        text_align=ft.TextAlign.CENTER),
                ft.Text("Auteur : Sereina YOPA • Projet scolaire – Soutenance technique", italic=True, size=14,
                        text_align=ft.TextAlign.CENTER)
            ])
        )

    def kpis_tab():
        return ft.Container(
            padding=ft.Padding(160, 50, 160, 50),
            content=ft.Column([
                ft.Text("🏀 Statistiques et KPIs des Joueurs", size=36, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                # Section 1 : Filtres et card joueur
                ft.Row([
                    ft.Column([
                        ft.Text("Filtres", size=20, weight=ft.FontWeight.BOLD),
                        ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                        ft.Dropdown(label="Équipe", options=[], width=200, border_color=ft.Colors.WHITE),
                        ft.Dropdown(label="Joueur", options=[], width=200, border_color=ft.Colors.WHITE)
                    ], spacing=10),
                    ft.Container(width=30),
                    ft.Container(
                        expand=True,
                        border_radius=10,
                        padding=15,
                        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE),
                        content=ft.Row([
                            ft.Container(width=40),
                            ft.Text("Nom du joueur", size=26, weight=ft.FontWeight.BOLD),
                            ft.Container(width=40),
                            ft.Column([
                                ft.Text("• Points par match : ..."),
                                ft.Text("• Assists : ..."),
                                ft.Text("• Rebounds : ..."),
                                ft.Text("• Efficiency : ..."),
                                ft.Text("• FG% : ..."),
                                ft.Text("• Minutes : ...")
                            ])
                        ])
                    )
                ]),
                ft.Divider(),
                # Section 2 : Line chart (placeholder)
                ft.Text("📈 Évolution de la saison", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=300,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Graphique ligne points + efficacité à intégrer]", italic=True)
                ),

                ft.Divider(),
                # Section 3 : Comparaison de joueurs avec radar chart
                ft.Text("🧠 Comparateur de Joueurs", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Dropdown(label="Joueur 1", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Joueur 2", options=[], width=200, border_color=ft.Colors.WHITE)
                ], spacing=20),
                ft.Row([
                    ft.Container(
                        expand=True,
                        content=ft.Text("Card Joueur 1", text_align=ft.TextAlign.CENTER)
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Text("Radar Chart", text_align=ft.TextAlign.CENTER)
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Text("Card Joueur 2", text_align=ft.TextAlign.CENTER)
                    )
                ], spacing=20),

                ft.Divider(),
                # Section 4 : Scatter plot équipes
                ft.Text("📉 Performance des Équipes", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Paramètre", options=[], width=200, border_color=ft.Colors.WHITE)
                ], spacing=20),
                ft.Container(
                    height=300,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Scatter plot à intégrer]", italic=True)
                ),

                ft.Divider(),
                # Section 5 : Visualisation des matchs
                ft.Text("🏟️ Matchs spécifiques", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Dropdown(label="Type de match",
                                options=[ft.dropdown.Option("Saison régulière"), ft.dropdown.Option("Playoffs")],
                                width=200,
                                border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Équipe à domicile", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Équipe à l'extérieur", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Date", options=[], width=200, border_color=ft.Colors.WHITE)
                ], spacing=20),
                ft.Container(
                    height=300,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Graphique par quarts à intégrer]", italic=True)
                )
            ], spacing = 40)
        )

    def draft_predictions_tab():
        sheet_ref = ft.Ref[ft.BottomSheet]()

        def show_modal(player_name, pick, team, prob_flop, is_flop):
            color = ft.Colors.RED_400 if is_flop else ft.Colors.GREEN_400
            status = "Flop prédit" if is_flop else "Bon choix"
            sheet_ref.current.content = ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Text(player_name, size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(f"🎯 Pick #{pick} - {team}"),
                    ft.Text(f"📉 Probabilité de flop : {prob_flop * 100:.2f} %"),
                    ft.Text(f"🧠 Statut : {status}", color=color),
                ])
            )
            sheet_ref.current.open = True
            sheet_ref.current.update()

        player_rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("Victor Wembanyama"),
                                on_tap=lambda e: show_modal("Victor Wembanyama", 1, "Spurs", 0.12, False)),
                    ft.DataCell(ft.Text("1")),
                    ft.DataCell(ft.Text("Spurs")),
                    ft.DataCell(ft.Text("12%")),
                    ft.DataCell(ft.Text("❌"))
                ]
            ),
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("John Doe"), on_tap=lambda e: show_modal("John Doe", 9, "Knicks", 0.78, True)),
                    ft.DataCell(ft.Text("9")),
                    ft.DataCell(ft.Text("Knicks")),
                    ft.DataCell(ft.Text("78%")),
                    ft.DataCell(ft.Text("✅"))
                ]
            )
        ]

        return ft.Container(
            padding=ft.Padding(160, 50, 160, 50),
            content=ft.Column([
            ft.Text("🔮 Prédictions de Flops à la Draft", size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([
                ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                ft.Switch(label="Afficher uniquement les flops", value=False)
            ], spacing=20),
            ft.Container(height=20),
            ft.DataTable(
                columns=[
                    ft.DataColumn(label=ft.Text("Joueur")),
                    ft.DataColumn(label=ft.Text("Pick")),
                    ft.DataColumn(label=ft.Text("Équipe")),
                    ft.DataColumn(label=ft.Text("Prob. Flop")),
                    ft.DataColumn(label=ft.Text("Est Flop ?")),
                ],
                rows=player_rows
            ),
            ft.BottomSheet(ref=sheet_ref, content=ft.Container(), open=False)
        ])
        )

    def playoff_tab():
        return ft.Container(
            padding=ft.Padding(50, 0, 50, 0),
            content=ft.Column([
                ft.Text("🏆 Prédictions Playoffs NBA", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                # 🎯 Filtres
                ft.Row([
                    ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Conférence", options=[
                        ft.dropdown.Option("Est"),
                        ft.dropdown.Option("Ouest")
                    ], width=200, border_color=ft.Colors.WHITE),
                    ft.Switch(label="Afficher uniquement les favoris", value=False)
                ], spacing=20),

                ft.Container(height=20),

                # 📋 Tableau des prédictions
                ft.Text("📋 Résultats Simulés", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=300,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Tableau avec probabilités par équipe à intégrer ici]", italic=True)
                ),

                ft.Container(height=30),

                # 🔮 Équipe favorite
                ft.Text("🔮 Équipe favorite prédite", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=200,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    padding=20,
                    content=ft.Column([
                        ft.Text("[Nom de l’équipe]", size=22, weight=ft.FontWeight.BOLD),
                        ft.Text("Probabilité de victoire : ..."),
                        ft.ProgressBar(width=400, value=0.72)
                    ])
                ),

                ft.Container(height=30),

                # 🧠 Focus équipe modale
                ft.Text("🧠 Focus sur une équipe", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=200,
                    bgcolor=ft.Colors.with_opacity(0.04, ft.Colors.WHITE),
                    border_radius=8,
                    padding=20,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Modal au clic d’une équipe]", italic=True)
                )
            ])
        )

    def lineup_tab():
        return ft.Container(
            padding=ft.Padding(50, 0, 50, 0),
            content=ft.Column([
                ft.Text("🧠 Recommandation de Lineup Optimal", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),

                # 🔹 Filtres tactiques
                ft.Row([
                    ft.Dropdown(label="Saison", options=[], width=200, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Équipe à optimiser", options=[], width=250, border_color=ft.Colors.WHITE),
                    ft.Dropdown(label="Équipe adverse", options=[], width=250, border_color=ft.Colors.WHITE)
                ], spacing=20),

                ft.Container(height=30),

                # 🧱 Lineup recommandé
                ft.Text("🧱 Lineup conseillé contre l'adversaire", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=10,
                    padding=20,
                    content=ft.Column([
                        ft.Text("🏀 PG: ..."),
                        ft.Text("🏀 SG: ..."),
                        ft.Text("🏀 SF: ..."),
                        ft.Text("🏀 PF: ..."),
                        ft.Text("🏀 C: ..."),
                    ])
                ),

                ft.Container(height=30),

                # 📊 Comparaison radar / bar
                ft.Text("📊 Comparaison des forces moyennes", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=300,
                    bgcolor=ft.Colors.with_opacity(0.03, ft.Colors.WHITE),
                    border_radius=8,
                    alignment=ft.alignment.center,
                    content=ft.Text("[Radar Chart ou Bar Chart à intégrer ici]", italic=True)
                ),

                ft.Container(height=30),

                # 💬 Analyse complémentaire
                ft.Text("💬 Analyse stratégique de l’alignement", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE),
                    border_radius=8,
                    padding=20,
                    content=ft.Text("[Résumé tactique automatique à intégrer]", italic=True)
                )
            ])
        )

    # Initialisation
    content_container.controls = [overview_tab()]
    page.add(tabs, content_container)

ft.app(target=main)
