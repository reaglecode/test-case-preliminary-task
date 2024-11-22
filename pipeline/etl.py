import pandas as pd
import requests
from sqlalchemy import create_engine
from pydantic import TypeAdapter

from .const import API_URL
from .models import VantaaOpenApplications, OpenApplication
from .config import VantaaOpenApplications_colnames


class SimpleExtractor:
    def __init__(self) -> None:
        self.api_url = API_URL

    def fetch_data(self):
        """Testing API connection
        >>> extractor = SimpleExtractor()
        >>> response = extractor.fetch_data()
        >>> response.status_code == 200
        True
        """
        return requests.get(
            url=self.api_url,
            headers={"Content-Type": "application/json"},
        )

    def extract(self) -> pd.DataFrame:
        adapter = TypeAdapter(OpenApplication)
        
        response = self.fetch_data()
        response.raise_for_status()

        # validating the records data types:
        validated_items = [adapter.validate_python(x).model_dump() for x in response.json()]
        return pd.json_normalize(validated_items)

    def __call__(self) -> pd.DataFrame:
        return self.extract()


class SimpleTransformer:
    def __init__(self):
        self.rename_schema = VantaaOpenApplications_colnames

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        # Rename based on the defined schema and drop irrelevant fields
        return df.rename(columns=self.rename_schema)[self.rename_schema.values()]

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.pipe(self._rename_columns)# .pipe(self._transform_dates)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.transform(df=df)


class SimpleLoader:
    def __init__(self, conn_str: str) -> None:
        # Setup Engine
        # TODO: test the engine connection
        self.engine = create_engine(conn_str)

    def load(self, df: pd.DataFrame) -> None:
        with self.engine.connect() as conn:
            df.to_sql(
                name=VantaaOpenApplications.__name__,
                con=conn,
                if_exists="replace"  # this argument needs to be adjusted accordingly
                )
            conn.commit()

    def __call__(self, df: pd.DataFrame) -> None:
        self.load(df=df)


def run_etl(conn_str: str):
    # Initialise ETL parts
    extractor = SimpleExtractor()
    transformer = SimpleTransformer()
    loader = SimpleLoader(conn_str=conn_str)

    # Run parts
    df = extractor()
    df = transformer(df=df)
    loader(df=df)

    print("Data loaded to database succesfully")
