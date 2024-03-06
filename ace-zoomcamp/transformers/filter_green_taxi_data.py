if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    data = data.rename(columns={
        'VendorID': 'vendor_id', 
        'PULocationID': 'pu_location_id',
        'DOLocationID': 'do_location_id',
        'RatecodeID': 'ratecode_id'})

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]


@test
def test_output(output, *args) -> None:
    
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'
    assert 'vendor_id' in output.columns, 'No vendor_id column found'