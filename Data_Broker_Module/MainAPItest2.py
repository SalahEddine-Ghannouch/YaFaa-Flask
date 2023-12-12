from APItest2_salah import FootballAPIClient as ftb
import pandas as pd



# Exemple d'utilisation
api_key = "aaa88b890fmsh2d5e556959f28f1p16f5f6jsn4e6244d68839"
football_api = ftb(api_key=api_key)


#-------------- Exemple pour obtenir les statistiques des fixtures
# fixtures_statistics = football_api.get_fixtures_statistics("37899")
# print("Statistiques des fixtures :", fixtures_statistics.columns)

# season = football_api.get_fixtures_statistics("37899")

"""
get_all_fixtures_statistics_in_season of league

"""
# fixt_id = football_api.get_fixtures_ids("2021","39")
# for index, row in fixt_id.iterrows():
#     match_id = row["FixtureID"]
#     print(football_api.get_fixtures_statistics(match_id))

football_api.get_all_fixtures_statistics_in_season("39","2021")


# # Exemple pour obtenir les événements des fixtures
# fixtures_events = football_api.get_fixtures_events("2022", "Premier League")
# print("Événements des fixtures :", fixtures_events)
