import pytest

import curve_dao


def test_get_address():
    assert curve_dao.get_address("ownership") == curve_dao.get_address(
        curve_dao.addresses.DAO.OWNERSHIP
    )
    assert curve_dao.get_address("param") == curve_dao.get_address(
        curve_dao.addresses.DAO.PARAM
    )
    assert curve_dao.get_address("emergency") == curve_dao.get_address(
        curve_dao.addresses.DAO.EMERGENCY
    )

    with pytest.raises(ValueError):
        curve_dao.get_address(curve_dao.addresses.CURVE_DAO_OWNERSHIP)


@pytest.mark.parametrize(
    "target",
    [
        curve_dao.addresses.DAO.OWNERSHIP,
        "param",
        "0x467947EE34aF926cF1DCac093870f613C96B1E0c",
        "0x467947ee34aF926cF1DCAc093870f613c96b1e0c",  # Case-insensitive
    ],
)
def test_target(target, etherscan_api_key):
    curve_dao.prepare_evm_script(target, [], etherscan_api_key)
