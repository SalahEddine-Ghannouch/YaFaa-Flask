import random
import pandas as pd
import duckdb
import plotly.graph_objects as go
import plotly.express as px

class yafaaSQL:
    def __init__(self, database=':memory:'):
        """
        Connects to the DuckDB database stored in memory.

        Args:
            database (str, optional): Path to the DuckDB database file. Defaults to in-memory database.
        """
        self.con = duckdb.connect(database=database)

    def select_by_season(self, dataframe, year):
        """
        Filters the given dataframe to rows with the specified season.

        Args:
            dataframe (pandas.DataFrame or duckdb.DuckDBDataFrame): The dataframe to filter.
            year (int): The season year to filter for.

        Returns:
            pandas.DataFrame: The filtered dataframe.
        """
        if isinstance(dataframe, pd.DataFrame):
            # Already loaded in DuckDB, use SQL query
            df = dataframe
            query = f"""
            SELECT *
            FROM df
            WHERE League_season = ?
            """
            parameters = (year,)
            return self.con.execute(query, parameters).fetchdf()
        else:
            # Not a Pandas or DuckDB dataframe, convert to Pandas and filter
            df = pd.DataFrame(dataframe)
            return self.select_by_season(dataframe=df, year=year)

    def filter_by_team(self, dataframe, team, home=True):
        """
        Filters a dataframe based on a team's participation as home or away.

        Args:
            dataframe (pandas.DataFrame or duckdb.DuckDBDataFrame): The dataframe to filter.
            team (int): The team ID to filter for.
            home (bool, optional): Whether to filter for home (True) or away (False) matches. Defaults to True.

        Returns:
            pandas.DataFrame: The filtered dataframe.
        """
        if isinstance(dataframe, pd.DataFrame):
            # Already loaded in DuckDB, use SQL query
            df = dataframe
            column = "teams_home_id" if home else "teams_away_id"
            query = f"""
                SELECT *
                FROM df
                WHERE {column} = ?
            """
            parameters = (team,)
            return self.con.execute(query, parameters).fetchdf()
        else:
            # Not a Pandas or DuckDB dataframe, convert to Pandas and filter
            df = pd.DataFrame(dataframe)
            return self.filter_by_team(dataframe=df, team=team, home=home)


    def team_goals_summary(self, dataframe):
        """
        Computes the total home_goals, away_goals, and total_goals for each team in the provided dataframe.

        Args:
            dataframe (pandas.DataFrame or duckdb.DuckDBDataFrame): The dataframe to compute team goals.

        Returns:
            pandas.DataFrame: A dataframe with team_id, team_name, home_goals, away_goals, and total_goals.
        """
        if isinstance(dataframe, pd.DataFrame):
            # Already loaded in Pandas, use Pandas DataFrame for the computations
            home_goals_df = dataframe.groupby(['teams_home_id', 'teams_home_name'])['score_fulltime_home'].sum().reset_index()
            home_goals_df.rename(columns={'teams_home_name': 'team_name', 'teams_home_id': 'team_id', 'score_fulltime_home': 'home_goals'}, inplace=True)

            away_goals_df = dataframe.groupby(['teams_away_id', 'teams_away_name'])['score_fulltime_away'].sum().reset_index()
            away_goals_df.rename(columns={'teams_away_name': 'team_name', 'teams_away_id': 'team_id', 'score_fulltime_away': 'away_goals'}, inplace=True)
        elif hasattr(dataframe, 'to_df'):  # Assuming there's a method to convert to a Pandas DataFrame
            # Convert DuckDB DataFrame to Pandas DataFrame
            df = dataframe.to_df()

            # Use Pandas DataFrame for the computations
            home_goals_df = df.groupby(['teams_home_id', 'teams_home_name'])['score_fulltime_home'].sum().reset_index()
            home_goals_df.rename(columns={'teams_home_name': 'team_name', 'teams_home_id': 'team_id', 'score_fulltime_home': 'home_goals'}, inplace=True)

            away_goals_df = df.groupby(['teams_away_id', 'teams_away_name'])['score_fulltime_away'].sum().reset_index()
            away_goals_df.rename(columns={'teams_away_name': 'team_name', 'teams_away_id': 'team_id', 'score_fulltime_away': 'away_goals'}, inplace=True)
        else:
            raise ValueError("Unsupported dataframe type")

        # Concatenate the DataFrames
        combined_df = pd.concat([home_goals_df, away_goals_df])

        # Group by 'team_name' and sum the 'home_goals' and 'away_goals'
        team_goals_by_season = combined_df.groupby('team_name')[['home_goals', 'away_goals']].sum().reset_index()
        # Calculate 'total_goals'
        team_goals_by_season['total_goals'] = team_goals_by_season['home_goals'] + team_goals_by_season['away_goals']

        return team_goals_by_season


    def aggregate_columns(self, dataframe, field_names, aggregation='sum'):
        """
        Computes the specified aggregation for the specified columns in the provided dataframe.

        Args:
            dataframe (pandas.DataFrame): The dataframe.
            field_names (list): The list of column names for which to compute the aggregation.
            aggregation (str, optional): The aggregation function to apply ('sum', 'var', 'median', 'max', 'min', 'mean').
                                         Defaults to 'sum'.

        Returns:
            pandas.DataFrame: A dataframe with a single row containing the result of the specified aggregation for each column.
        """
        if not isinstance(dataframe, pd.DataFrame):
            raise ValueError("Input must be a Pandas DataFrame")

        # Validate aggregation function
        valid_aggregations = ['sum', 'var', 'median', 'max', 'min', 'mean']
        if aggregation not in valid_aggregations:
            raise ValueError(f"Invalid aggregation function. Choose from {valid_aggregations}")

        # Apply the specified aggregation function to each specified column
        result_values = []
        for field_name in field_names:
            if aggregation == 'sum':
                result_values.append(dataframe[field_name].sum())
            elif aggregation == 'var':
                result_values.append(dataframe[field_name].var())
            elif aggregation == 'median':
                result_values.append(dataframe[field_name].median())
            elif aggregation == 'max':
                result_values.append(dataframe[field_name].max())
            elif aggregation == 'min':
                result_values.append(dataframe[field_name].min())
            elif aggregation == 'mean':
                result_values.append(dataframe[field_name].mean())

        # Create a new DataFrame with the results
        result_df = pd.DataFrame({f'{aggregation}_of_{field_name}': [result_value] for field_name, result_value in zip(field_names, result_values)})

        return result_df


class yaffaPLT:
    def __init__(self):
        pass

    def _update_layout(self, 
                       fig, 
                       paper_bgcolor="white", 
                       margin=dict(t=0, b=0), 
                       showlegend=False, 
                       plot_bgcolor="white", 
                       height=200, 
                       width=600):
        
        fig.update_layout(
            paper_bgcolor=paper_bgcolor,
            margin=margin,
            showlegend=showlegend,
            plot_bgcolor=plot_bgcolor,
            height=height,
            width=width,
        )


    def plot_metric(self, 
                    label, 
                    column_name, 
                    dataframe, 
                    index=0, 
                    prefix="", 
                    suffix="", 
                    show_graph=False, 
                    color_graph="", 
                    bold_label=False,
                    #The following options to update the layout, check the layout options abouve:
                    paper_bgcolor="white", 
                    margin=dict(t=50, b=0), 
                    showlegend=False, 
                    plot_bgcolor="white", 
                    height=200, width=600
                    ):
        # Perform the specified operation on the chosen index of the dataframe column
        value = int(dataframe[column_name].iloc[index])

        fig = go.Figure()

        if bold_label:
            label = f"<b>{label}</b>"

        fig.add_trace(
            go.Indicator(
                value=value,
                gauge={"axis": {"visible": False}},
                number={
                    "prefix": prefix,
                    "suffix": suffix,
                    "font.size": 60,
                    "font.color": "#ffaf00",
                },
                title={
                    "text": label,
                    "font": {
                        "size": 50,
                        "color": "#131116",
                    },
                },
            )
        )

        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(visible=False, fixedrange=True)
        self._update_layout(fig=fig, 
                            paper_bgcolor="white", 
                            margin=dict(t=50, b=0),
                            showlegend=False,
                            plot_bgcolor="white",
                            height=200, 
                            width=300)
        
        return fig.to_html(full_html=False)


#? EXAMPLE USAGE : 
# df = pd.read_csv ('test.csv')
# database = yafaaSQL()
# year_df = database.select_by_season(df, '2019')
# team_df = database.filter_by_team(year_df,team=54 ,home=False)
# teams_summary = database.team_goals_summary(year_df)
# aggregated_columns = database.aggregate_columns(teams_summary, ['total_goals', 'home_goals', 'away_goals'], aggregation='sum')

#* Plotting 
# plt_instance = yaffaPLT()

# fig = plt_instance.plot_metric(label="Total Goals Scored", column_name="sum_of_total_goals", dataframe=aggregated_columns, prefix="", suffix=" Goals", bold_label=True)
# fig