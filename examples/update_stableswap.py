import os

import boa
from rich import print

import curve_dao

# Load environment variables and fork the Ethereum mainnet
boa.env.fork(os.getenv("RPC_ETHEREUM"))

# Set up constants
VOTE_CREATOR_SIM = "0xE6DA683076b7eD6ce7eC972f21Eb8F91e9137a17"
POOL_ADDRESS = "0xab96aa0ee764924f49fbb372f3b4db9c2cb24ea2"
RAMP_TIME_WEEKS = 1
NEW_A = 1000
NEW_FEE_BPS = 1
NEW_OFFPEG_FEE_MULTIPLIER = 5
PROPOSAL_TIME_WEEKS = 1

# Load the StableswapNG contract
pool = boa.from_etherscan(
    POOL_ADDRESS, name="StableswapNG", api_key=os.getenv("ETHERSCAN_API_KEY")
)

# Generate proposal actions and description
actions, description = curve_dao.proposals.stableswap.update_parameters(
    pool,
    RAMP_TIME_WEEKS,
    NEW_A,
    NEW_FEE_BPS,
    NEW_OFFPEG_FEE_MULTIPLIER,
    PROPOSAL_TIME_WEEKS,
)

# Create and submit the proposal
with boa.env.prank(VOTE_CREATOR_SIM):
    vote_id = curve_dao.create_vote(
        curve_dao.get_address("ownership"),
        actions,
        description,
        os.getenv("ETHERSCAN_API_KEY"),
        os.getenv("PINATA_TOKEN"),
    )
print(f"Vote ID: {vote_id}")

# Simulate the proposal execution
curve_dao.simulate(
    vote_id, curve_dao.get_address("ownership"), os.getenv("ETHERSCAN_API_KEY")
)

# Time travel to after the ramp period
boa.env.time_travel(seconds=60 * 60 * 24 * 8)  # 8 days (7 days ramp + 1 day buffer)

# Verify the new parameters

assert pool.A() == NEW_A
assert pool.fee() == NEW_FEE_BPS * 1000000
assert pool.offpeg_fee_multiplier() == NEW_OFFPEG_FEE_MULTIPLIER * 10**10

print("All parameters updated successfully!")
