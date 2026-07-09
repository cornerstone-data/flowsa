"""
Unit tests for assign_temporal_correlation year resolution.
"""
import pandas as pd
import pytest
from flowsa.flowbysector import FlowBySector


def _minimal_fbs(full_name, config, year=2015):
    """Build a minimal FlowBySector for temporal correlation tests."""
    df = pd.DataFrame({
        'Flowable': ['test'],
        'Class': ['Money'],
        'SectorProducedBy': ['111'],
        'SectorConsumedBy': [None],
        'SectorSourceName': ['NAICS_2017_Code'],
        'Context': ['emission/air'],
        'Location': ['00000'],
        'LocationSystem': ['FIPS_2015'],
        'FlowAmount': [1.0],
        'Unit': ['USD'],
        'FlowType': ['ELEMENTARY_FLOW'],
        'Year': [year],
        'MeasureofSpread': [None],
        'Spread': [None],
        'DistributionType': [None],
        'Min': [None],
        'Max': [None],
        'DataReliability': [1.0],
        'TemporalCorrelation': [1.0],
        'GeographicalCorrelation': [1.0],
        'TechnologicalCorrelation': [1.0],
        'DataCollection': [1.0],
        'MetaSources': ['test'],
        'FlowUUID': [None],
    })
    return FlowBySector(
        df,
        full_name=full_name,
        config=config,
        convert_df_to_flowby=True,
    )


def test_temporal_correlation_uses_year_from_method_name():
    fbs = _minimal_fbs('Employment_national_2023', {'year': 2019}, year=2020)
    result = fbs.assign_temporal_correlation()
    assert (result['Year'] == 2023).all()


def test_temporal_correlation_falls_back_to_config_year():
    """Methods like NIPA_FD_common have no year in the name."""
    fbs = _minimal_fbs('NIPA_FD_common', {'year': 2017}, year=2015)
    result = fbs.assign_temporal_correlation()
    assert (result['Year'] == 2017).all()


def test_temporal_correlation_explicit_target_year():
    fbs = _minimal_fbs('NIPA_FD_common', {}, year=2015)
    result = fbs.assign_temporal_correlation(target_year=2018)
    assert (result['Year'] == 2018).all()


def test_temporal_correlation_missing_year_raises():
    fbs = _minimal_fbs('NIPA_FD_common', {}, year=2015)
    with pytest.raises(ValueError, match='Unable to determine target year'):
        fbs.assign_temporal_correlation()
