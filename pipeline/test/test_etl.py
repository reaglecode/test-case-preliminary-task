import pytest
from ..etl import SimpleExtractor, SimpleTransformer
from ..config import VantaaOpenApplications_colnames


class TestSimpleExtractor():
    # NOTE: API connection test is written in doctest form.
    def test_column_names(self):
        """This test makes sure that the column names in the dataframe
        received from API exist in the schema configuration.
        :return: None
        """
        df = SimpleExtractor()()
        assert set(df.columns).issubset(set(VantaaOpenApplications_colnames.keys()))


class TestSimpleTransformer():
    def test_rename_schema(self):
        """Checking if correct schema is selected.
        :return: None
        """
        df = SimpleTransformer()
        assert VantaaOpenApplications_colnames == df.rename_schema

    def test_column_renames(self):
        """This test is based on the assumption that column selection raises no errors,
        which means that the count of columns should be less than equal to the provided schema configuration.
        :return: None
        """
        df = SimpleExtractor()()
        df = SimpleTransformer()(df=df)
        assert len(df.columns) <= len(VantaaOpenApplications_colnames.values())
