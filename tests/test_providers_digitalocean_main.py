import pytest
from cloudproxy.providers.digitalocean.main import do_deployment, do_start
from cloudproxy.providers.digitalocean.functions import list_droplets
from tests.test_providers_digitalocean_functions import test_create_proxy, test_delete_proxy, load_from_file


@pytest.fixture
def droplets(mocker):
    """Fixture for droplets data."""
    data = load_from_file('test_providers_digitalocean_functions_droplets_all.json')
    mocker.patch('cloudproxy.providers.digitalocean.functions.digitalocean.Manager.get_all_droplets',
                 return_value=data['droplets'])
    return data['droplets']


@pytest.fixture
def droplet_id():
    """Fixture for droplet ID."""
    return "DROPLET-ID"


def test_do_deployment(mocker, droplets, droplet_id):
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.list_droplets',
        return_value=droplets
    )
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.create_proxy',
        return_value=True
    )
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.delete_proxy',
        return_value=True
    )
    result = do_deployment(1)
    assert isinstance(result, int)
    assert result == 1


def test_initiatedo(mocker):
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.do_deployment',
        return_value=2
    )
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.do_check_alive',
        return_value=["192.1.1.1"]
    )
    mocker.patch(
        'cloudproxy.providers.digitalocean.main.do_check_delete',
        return_value=True
    )
    result = do_start()
    assert isinstance(result, list)
    assert result == ["192.1.1.1"]


def test_list_droplets(droplets):
    """Test listing droplets."""
    result = list_droplets()
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0]['id'] == 3164444  # Verify specific droplet data
    # Store the result in a module-level variable if needed by other tests
    global test_droplets
    test_droplets = result