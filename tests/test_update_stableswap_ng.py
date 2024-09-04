import boa
import pytest

import curve_dao


@pytest.fixture
def target():
    return curve_dao.addresses.DAO.OWNERSHIP


@pytest.fixture
def pool(etherscan_api_key):
    return boa.from_etherscan(
        "0xab96aa0ee764924f49fbb372f3b4db9c2cb24ea2",
        name="StableswapNG",
        api_key=etherscan_api_key,
    )


@pytest.fixture
def ramp_time_weeks():
    return 1


@pytest.fixture
def new_A():
    return 1000


@pytest.fixture
def new_fee_bps():
    return 1


@pytest.fixture
def new_offpeg_fee_multiplier():
    return 5


@pytest.fixture
def proposal_time_weeks():
    return 1


@pytest.fixture
def actions_and_description(
    pool,
    ramp_time_weeks,
    new_A,
    new_fee_bps,
    new_offpeg_fee_multiplier,
    proposal_time_weeks,
):
    actions, description = curve_dao.proposals.stableswap.update_parameters(
        pool,
        ramp_time_weeks,
        new_A,
        new_fee_bps,
        new_offpeg_fee_multiplier,
        proposal_time_weeks,
    )
    assert actions == [
        ("0xAb96AA0ee764924f49fbB372f3B4db9c2cB24Ea2", "ramp_A", 1000, 1726688231),
        (
            "0xAb96AA0ee764924f49fbB372f3B4db9c2cB24Ea2",
            "set_new_fee",
            1000000,
            50000000000,
        ),
    ]
    return actions, description


def test_simulate_success(
    pool, vote_creator, target, etherscan_api_key, pinata_token, actions_and_description
):
    actions, description = actions_and_description

    with boa.env.prank(vote_creator):
        vote_id = curve_dao.create_vote(
            target, actions, description, etherscan_api_key, pinata_token
        )

    assert curve_dao.simulate(vote_id, target, etherscan_api_key)

    boa.env.time_travel(
        seconds=60 * 60 * 24 * 8
    )  # sleep 7(+1) days for ramp to complete

    assert pool.A() == 1000
    assert pool.fee() == 1000000
    assert pool.offpeg_fee_multiplier() == 50000000000
